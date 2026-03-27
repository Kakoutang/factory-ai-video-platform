from __future__ import annotations

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas
from .config import asset_root, cors_origins
from .course_knowledge import list_course_sources, parse_manual_sections, unique_course_titles
from .db import Base, engine, get_db
from .seed import seed_demo_data
from .services import (
    add_audit,
    add_task,
    ai_gateway,
    dumps,
    ensure_customer_thread,
    latest_audits,
    latest_tasks,
    loads,
    now,
    score_comment,
    serialize_capture_job,
    serialize_draft,
    serialize_asset,
    serialize_lead,
    serialize_package,
    serialize_project,
    sync_local_assets,
    extract_product_name,
)


app = FastAPI(title="工厂 AI 视频工厂", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_database():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_demo_data(db)
        sync_local_assets(db)
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    initialize_database()


initialize_database()

app.mount("/client-assets", StaticFiles(directory=str(asset_root())), name="client-assets")


@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/products", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id).all()


@app.get("/api/assets", response_model=list[schemas.ProductAssetOut])
def list_assets(
    asset_type: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.ProductAsset).order_by(models.ProductAsset.created_at.desc())
    if asset_type:
        query = query.filter(models.ProductAsset.asset_type == asset_type)
    if category:
        query = query.filter(models.ProductAsset.category == category)
    return [serialize_asset(item) for item in query.all()]


@app.get("/api/ops-manual", response_model=schemas.OperationsManualOut)
def operations_manual():
    sections = parse_manual_sections()
    sources = list_course_sources()
    return {
        "title": "工厂 AI 视频工厂运营手册",
        "version": "V1",
        "source_count": len(sources),
        "unique_course_count": len(unique_course_titles()),
        "sections": sections,
        "sources": sources,
    }


@app.post("/api/assets/sync-local")
def sync_assets(db: Session = Depends(get_db)):
    sync_local_assets(db)
    return {"synced": True, "assets": db.query(models.ProductAsset).count()}


@app.get("/api/content/projects", response_model=list[schemas.ContentProjectOut])
def list_content_projects(db: Session = Depends(get_db)):
    return [serialize_project(item) for item in db.query(models.ContentProject).order_by(models.ContentProject.created_at.desc())]


@app.post("/api/content/projects", response_model=schemas.ContentProjectOut)
def create_content_project(payload: schemas.ContentProjectCreate, db: Session = Depends(get_db)):
    project = models.ContentProject(**payload.model_dump(), status="draft", package_status="pending", script_json=dumps({}))
    db.add(project)
    db.flush()
    add_task(db, "content_project_create", "content_project", project.id, "completed", "已创建内容任务")
    add_audit(db, "content_project", project.id, "content_project.created", "创建内容任务")
    db.commit()
    db.refresh(project)
    return serialize_project(project)


@app.post("/api/content/projects/{project_id}/generate-script", response_model=schemas.GenerateScriptResponse)
def generate_script(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.ContentProject).filter(models.ContentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="content project not found")

    product = db.query(models.Product).filter(models.Product.id == project.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    custom_product_name = extract_product_name(project.material_constraints)
    script = ai_gateway(
        "generate_script",
        {
            "title": project.title,
            "target_audience": project.target_audience,
            "product_name": custom_product_name or product.name,
            "topic_direction": project.topic_direction,
            "material_constraints": project.material_constraints,
            "asset_titles": [
                item.title
                for item in db.query(models.ProductAsset)
                .filter(models.ProductAsset.product_id == product.id)
                .order_by(models.ProductAsset.id.asc())
                .limit(8)
                .all()
            ],
        },
        knowledge_refs=[product.positioning, product.core_offer],
        output_schema={},
    )
    project.script_json = dumps(script)
    project.status = "script_ready"
    add_task(db, "script_generation", "content_project", project.id, "completed", "AI 已生成脚本和分镜")
    add_audit(db, "content_project", project.id, "content_project.script_generated", "已生成脚本")
    db.commit()
    return {"project_id": project.id, "status": project.status, "script": script}


@app.get("/api/publish-packages", response_model=list[schemas.PublishPackageOut])
def list_publish_packages(db: Session = Depends(get_db)):
    return [serialize_package(item) for item in db.query(models.PublishPackage).order_by(models.PublishPackage.created_at.desc())]


@app.post("/api/content/projects/{project_id}/generate-package", response_model=schemas.PublishPackageOut)
def generate_publish_package(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.ContentProject).filter(models.ContentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="content project not found")

    product = db.query(models.Product).filter(models.Product.id == project.product_id).first()
    script = loads(project.script_json, {})
    if not script:
        raise HTTPException(status_code=400, detail="script must be generated first")

    preview_asset = (
        db.query(models.ProductAsset)
        .filter(models.ProductAsset.asset_type == "video")
        .order_by(models.ProductAsset.id.asc())
        .first()
    )

    package_payload = ai_gateway(
        "generate_publish_package",
        {
            "title": project.title,
            "product_name": product.name if product else "产品",
            "script": script,
            "preview_url": preview_asset.public_url if preview_asset else "",
        },
        knowledge_refs=[],
        output_schema={},
    )
    pkg = models.PublishPackage(
        content_project_id=project.id,
        platform="douyin",
        title=package_payload["title"],
        description=package_payload["description"],
        hashtags=dumps(package_payload["hashtags"]),
        cover_text=package_payload["cover_text"],
        preview_url=package_payload["preview_url"],
        approval_status="pending_review",
    )
    db.add(pkg)
    db.flush()

    video = models.VideoAsset(
        publish_package_id=pkg.id,
        platform="douyin",
        video_url=f"https://www.douyin.com/video/demo-{pkg.id}",
        title=pkg.title,
        publish_status="ready_for_publish",
    )
    db.add(video)

    project.package_status = "ready"
    add_task(db, "publish_package_generation", "publish_package", pkg.id, "completed", "已生成发布包和演示视频")
    add_audit(db, "publish_package", pkg.id, "publish_package.generated", "已生成发布包")
    db.commit()
    db.refresh(pkg)
    return serialize_package(pkg)


@app.post("/api/publish-packages/{package_id}/approve", response_model=schemas.PublishPackageOut)
def approve_publish_package(package_id: int, payload: schemas.ApproveRequest, db: Session = Depends(get_db)):
    pkg = db.query(models.PublishPackage).filter(models.PublishPackage.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="publish package not found")
    pkg.approval_status = "approved"
    pkg.approved_by = payload.approved_by
    add_audit(db, "publish_package", pkg.id, "publish_package.approved", f"审核人：{payload.approved_by}")
    add_task(db, "publish_package_approval", "publish_package", pkg.id, "completed", "发布包已审核通过")
    db.commit()
    return serialize_package(pkg)


@app.post("/api/capture/jobs", response_model=schemas.CaptureJobOut)
def create_capture_job(payload: schemas.CaptureJobCreate, db: Session = Depends(get_db)):
    job = models.CaptureJob(
        source_links=dumps(payload.source_links),
        trigger_mode=payload.trigger_mode,
        status="queued",
        strategy_json=dumps(payload.strategy),
    )
    db.add(job)
    db.flush()
    add_task(db, "capture_job_create", "capture_job", job.id, "queued", "等待 worker 采集评论")
    add_audit(db, "capture_job", job.id, "capture_job.created", "已创建评论采集任务")
    db.commit()
    return serialize_capture_job(job)


@app.get("/api/capture/jobs", response_model=list[schemas.CaptureJobOut])
def list_capture_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.CaptureJob).order_by(models.CaptureJob.created_at.desc()).all()
    return [serialize_capture_job(job) for job in jobs]


@app.post("/api/capture/imports/manual-json")
def import_manual_json(payload: schemas.ManualImportPayload, db: Session = Depends(get_db)):
    imported = 0
    lead_count = 0

    video = db.query(models.VideoAsset).filter(models.VideoAsset.video_url == payload.page.url).first()
    if not video:
        video = models.VideoAsset(
            publish_package_id=None,
            platform="douyin",
            video_url=payload.page.url,
            title=payload.page.title,
            publish_status="published_or_external",
        )
        db.add(video)
        db.flush()

    capture_job = models.CaptureJob(
        source_links=dumps([payload.page.url]),
        trigger_mode="manual_json_import",
        status="completed",
        strategy_json=dumps({"source": payload.source, "collectedAt": payload.collectedAt}),
        started_at=now(),
        finished_at=now(),
    )
    db.add(capture_job)
    db.flush()

    for item in payload.comments:
        dedupe_key = f"{payload.page.url}::{item.nickname}::{item.comment}::{item.time}"
        exists = db.query(models.Comment).filter(models.Comment.dedupe_key == dedupe_key).first()
        if exists:
            continue

        comment = models.Comment(
            platform="douyin",
            video_url=payload.page.url,
            video_title=payload.page.title,
            nickname=item.nickname,
            comment_text=item.comment,
            comment_time=item.time,
            uid=item.uid,
            douyin_id=item.douyinId,
            like_count=item.likeCount,
            reply_count=item.replyCount,
            gender=item.gender,
            region=item.region,
            raw_payload=dumps(item.model_dump()),
            dedupe_key=dedupe_key,
        )
        db.add(comment)
        db.flush()
        imported += 1

        score, tags, status, summary = score_comment(comment.comment_text, comment.like_count)
        lead = models.Lead(
            comment_id=comment.id,
            source_video_url=comment.video_url,
            customer_name=comment.nickname,
            status=status,
            score=score,
            tags=dumps(tags),
            sales_owner="待分配",
            summary=summary,
        )
        db.add(lead)
        db.flush()
        lead_count += 1

        customer, thread = ensure_customer_thread(db, lead)
        thread.last_message = comment.comment_text

        add_task(db, "lead_scoring", "lead", lead.id, "completed", summary)
        add_audit(db, "comment", comment.id, "comment.imported", f"来自 {payload.source}")
        add_audit(db, "lead", lead.id, "lead.created", "由手动导入评论生成线索")

    add_task(db, "capture_import", "capture_job", capture_job.id, "completed", f"导入评论 {imported} 条")
    add_audit(db, "capture_job", capture_job.id, "capture_job.imported", f"共导入 {imported} 条评论")
    db.commit()
    return {"imported_comments": imported, "created_leads": lead_count, "capture_job_id": capture_job.id}


@app.post("/api/leads/score")
def rescore_leads(payload: schemas.LeadScoreRequest, db: Session = Depends(get_db)):
    query = db.query(models.Lead)
    if payload.comment_ids:
        query = query.filter(models.Lead.comment_id.in_(payload.comment_ids))
    leads = query.all()
    updated = 0
    for lead in leads:
        comment = db.query(models.Comment).filter(models.Comment.id == lead.comment_id).first()
        if not comment:
            continue
        score, tags, status, summary = score_comment(comment.comment_text, comment.like_count)
        lead.score = score
        lead.tags = dumps(tags)
        lead.status = status
        lead.summary = summary
        updated += 1
    db.commit()
    return {"updated": updated}


@app.get("/api/leads", response_model=list[schemas.LeadOut])
def list_leads(
    region: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    min_like_count: int = Query(default=0),
    video_title: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    leads = db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()
    results = []
    for lead in leads:
        item = serialize_lead(db, lead)
        if region and region not in item["region"]:
            continue
        if keyword and keyword not in item["comment_text"]:
            continue
        if min_like_count and item["like_count"] < min_like_count:
            continue
        if video_title and video_title not in item["video_title"]:
            continue
        if status and status != item["status"]:
            continue
        results.append(item)
    return results


@app.get("/api/customers", response_model=list[schemas.CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).order_by(models.Customer.created_at.desc()).all()
    return customers


@app.get("/api/message-drafts", response_model=list[schemas.MessageDraftOut])
def list_message_drafts(db: Session = Depends(get_db)):
    drafts = db.query(models.MessageDraft).order_by(models.MessageDraft.created_at.desc()).all()
    return [serialize_draft(item) for item in drafts]


@app.post("/api/conversations/{lead_id}/draft-reply", response_model=schemas.ReplyDraftResponse)
def generate_reply_draft(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="lead not found")

    comment = db.query(models.Comment).filter(models.Comment.id == lead.comment_id).first()
    product = db.query(models.Product).order_by(models.Product.id).first()
    customer, thread = ensure_customer_thread(db, lead)

    reply = ai_gateway(
        "draft_reply",
        {
            "comment_text": comment.comment_text if comment else "",
            "product_name": product.name if product else "产品",
        },
        knowledge_refs=[],
        output_schema={},
    )
    draft = models.MessageDraft(
        lead_id=lead.id,
        thread_id=thread.id,
        content=reply["reply"],
        approval_status="pending_review",
        approved=False,
    )
    db.add(draft)
    add_task(db, "reply_draft_generation", "message_draft", lead.id, "completed", "已生成回复草稿")
    add_audit(db, "message_draft", lead.id, "message_draft.generated", f"客户：{customer.name}")
    db.commit()
    db.refresh(draft)
    return {"draft_id": draft.id, "thread_id": thread.id, "content": draft.content, "approval_status": draft.approval_status}


@app.post("/api/conversations/{lead_id}/next-action", response_model=schemas.NextActionResponse)
def generate_next_action(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="lead not found")
    action = ai_gateway(
        "next_action",
        {"score": lead.score},
        knowledge_refs=[],
        output_schema={},
    )
    lead.status = action["stage"]
    customer = db.query(models.Customer).filter(models.Customer.lead_id == lead.id).first()
    if customer:
        customer.stage = action["stage"]
        customer.notes = action["action"]
    add_task(db, "next_action_generation", "lead", lead.id, "completed", action["action"])
    add_audit(db, "lead", lead.id, "lead.next_action_generated", action["reason"])
    db.commit()
    return {"lead_id": lead.id, "stage": action["stage"], "action": action["action"], "reason": action["reason"]}


@app.post("/api/message-drafts/{draft_id}/approve", response_model=schemas.MessageDraftOut)
def approve_message_draft(draft_id: int, payload: schemas.ApproveRequest, db: Session = Depends(get_db)):
    draft = db.query(models.MessageDraft).filter(models.MessageDraft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="message draft not found")
    draft.approved = True
    draft.approval_status = "approved"
    add_task(db, "message_draft_approval", "message_draft", draft.id, "completed", f"审核人：{payload.approved_by}")
    add_audit(db, "message_draft", draft.id, "message_draft.approved", f"审核人：{payload.approved_by}")
    db.commit()
    return serialize_draft(draft)


@app.get("/api/tasks", response_model=list[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return latest_tasks(db)


@app.get("/api/audit-logs", response_model=list[schemas.AuditLogOut])
def list_audit_logs(db: Session = Depends(get_db)):
    return latest_audits(db)


@app.get("/api/system/summary", response_model=schemas.SummaryOut)
def system_summary(db: Session = Depends(get_db)):
    return {
        "content_projects": db.query(models.ContentProject).count(),
        "publish_packages": db.query(models.PublishPackage).count(),
        "comments": db.query(models.Comment).count(),
        "leads": db.query(models.Lead).count(),
        "customers": db.query(models.Customer).count(),
        "drafts_pending": db.query(models.MessageDraft).filter(models.MessageDraft.approval_status == "pending_review").count(),
        "asset_files": db.query(models.ProductAsset).count(),
        "local_images": db.query(models.ProductAsset).filter(models.ProductAsset.asset_type == "image").count(),
        "local_videos": db.query(models.ProductAsset).filter(models.ProductAsset.asset_type == "video").count(),
        "knowledge_docs": db.query(models.ProductKnowledgeDoc).count(),
        "course_sources": len(list_course_sources()),
    }
