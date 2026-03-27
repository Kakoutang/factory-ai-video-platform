from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models
from .config import asset_root
from .course_knowledge import manual_bundle, unique_course_titles


HIGH_INTENT_KEYWORDS = ["价格", "怎么卖", "联系方式", "联系", "代理", "加盟", "报价", "现货", "合作"]
MEDIUM_INTENT_KEYWORDS = ["配置", "案例", "支持", "发我", "方案", "功能", "活动", "介绍"]
ASSET_EXTENSIONS = {
    "image": {".jpg", ".jpeg", ".png", ".webp"},
    "video": {".mp4", ".mov"},
    "document": {".doc", ".docx", ".ppt", ".pptx", ".pdf"},
    "spreadsheet": {".xls", ".xlsx", ".csv"},
}


def extract_product_name(material_constraints: str | None):
    if not material_constraints:
        return None
    for line in material_constraints.splitlines():
        stripped = line.strip()
        if stripped.startswith("产品名称："):
            value = stripped.split("：", 1)[1].strip()
            if value:
                return value
        if stripped.startswith("产品名称:"):
            value = stripped.split(":", 1)[1].strip()
            if value:
                return value
    return None


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def loads(value: str | None, fallback: Any):
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def add_audit(db: Session, entity_type: str, entity_id: int, action: str, detail: str):
    db.add(models.AuditLog(entity_type=entity_type, entity_id=entity_id, action=action, detail=detail))


def add_task(db: Session, task_type: str, entity_type: str, entity_id: int, status: str, detail: str):
    db.add(
        models.Task(
            task_type=task_type,
            entity_type=entity_type,
            entity_id=entity_id,
            status=status,
            detail=detail,
        )
    )


def ai_gateway(task_type: str, business_context: dict[str, Any], knowledge_refs: list[str], output_schema: dict[str, Any]):
    if task_type == "generate_script":
        title = business_context["title"]
        audience = business_context["target_audience"]
        product = business_context["product_name"]
        asset_titles = business_context.get("asset_titles", [])
        topic_direction = business_context.get("topic_direction", "")
        material_constraints = business_context.get("material_constraints", "")
        manual_sections = manual_bundle(
            [
                "内容定位",
                "对标调研规则",
                "选题规划规则",
                "脚本规划规则",
                "标题封面规则",
                "视频制作规则",
                "平台合规规则",
            ]
        )
        title_options = [
            f"{product} 怎么拍才更容易让 {audience} 愿意咨询？",
            f"{title}：先看工厂实力，再看产品细节和落地方案",
            f"不用纯靠外包团队，{product} 也能稳定做出工厂视频",
        ]
        hook_options = [
            f"{audience} 最怕的不是看不到产品，而是看完还不知道这家工厂靠不靠谱。",
            f"如果你正在找 {product} 相关方案，先别急着问价格，先看这三个工厂细节。",
            f"同样是 {product}，为什么有的工厂视频能带咨询，有的只是在展示图片？",
        ]
        cover_options = [
            f"{product} 工厂视频怎么拍",
            f"{product} 真实案例拆解",
            f"{product} 工厂实力与工艺细节",
        ]
        return {
            "topic": title,
            "audience": audience,
            "positioning": f"围绕“{topic_direction or title}”展开，先圈定 {audience}，再用真实工厂素材建立信任。",
            "planning_basis": {
                "topic_direction": topic_direction,
                "material_constraints": material_constraints,
                "knowledge_refs": knowledge_refs,
                "manual_sections": manual_sections,
                "source_course_count": len(unique_course_titles()),
            },
            "hook": hook_options[0],
            "hook_options": hook_options,
            "title_options": title_options,
            "cover_options": cover_options,
            "script_formula": [
                "先圈人群，再点痛点，再给工厂证据，再讲解决方案，最后给明确 CTA。",
                "前 3 秒必须出现强信息，不能慢热开场。",
                "镜头负责证明，文案负责解释，不要让文案单独承担全部说服力。",
            ],
            "content_angles": [
                f"从 {audience} 的采购/选厂顾虑切入，而不是从工厂自我介绍切入。",
                f"把 {product} 的工艺、材质、交付和案例变成镜头证据。",
                "优先做“工厂实力 + 产品细节 + 方案说明 + 行动指引”型视频。",
            ],
            "scenes": [
                {
                    "scene": 1,
                    "duration": "0-5秒",
                    "goal": "痛点钩子",
                    "shot": "用工厂环境、机器开机或产品近景开场，快速抛出采购顾虑。",
                    "voiceover": hook_options[0],
                },
                {
                    "scene": 2,
                    "duration": "5-18秒",
                    "goal": "工厂证据",
                    "shot": "展示工厂环境、生产设备、工艺细节和真实产品图。",
                    "voiceover": f"先别急着看低价，{product} 这类内容更应该先看工厂稳定性、工艺细节和交付能力。",
                },
                {
                    "scene": 3,
                    "duration": "18-35秒",
                    "goal": "产品与场景",
                    "shot": "切产品细节、应用场景、案例效果或材质特写。",
                    "voiceover": f"把 {product} 放进真实应用场景里讲，客户更容易理解它能解决什么问题。",
                },
                {
                    "scene": 4,
                    "duration": "35-50秒",
                    "goal": "方案说明",
                    "shot": "用数字人或字幕总结适合人群、方案逻辑和关键优势。",
                    "voiceover": f"这条视频不是单纯展示图片，而是要让 {audience} 知道这家工厂为什么值得进一步咨询。",
                },
                {
                    "scene": 5,
                    "duration": "50-60秒",
                    "goal": "行动指引",
                    "shot": "镜头回到产品或工厂画面，给出清晰 CTA。",
                    "voiceover": "想看案例、材质说明或报价思路，留言关键词或私信拿完整资料。",
                },
            ],
            "asset_plan": {
                "must_use": asset_titles[:6],
                "priority_mix": ["工厂图", "产品细节图", "案例图", "数字人口播", "视频样片"],
            },
            "caption": f"{product} 用真实工厂和产品素材快速生成企业视频，降低对外包视频团队的依赖。",
            "hashtags": ["AI视频生成", "工厂短视频", "制造业数字化"],
            "recommended_assets": asset_titles[:6],
            "publishing_checklist": [
                "确认参数、材质、规格、交期说法准确。",
                "确认标题、封面和正文表达一致。",
                "确认 CTA 清晰，能引导客户索取案例、方案或报价。",
            ],
            "compliance_checklist": [
                "避免绝对化承诺和夸张对比。",
                "避免把平台外导流写成默认显性表达。",
                "发布前保留人工审核。",
            ],
        }

    if task_type == "generate_publish_package":
        script = business_context["script"]
        title = business_context["title"]
        return {
            "title": f"{title}｜工厂 AI 视频样片",
            "description": f"{script.get('hook', '')} 支持直接导出成片、封面和发布文案。",
            "hashtags": script.get("hashtags", []),
            "cover_text": "工厂 AI 视频",
            "preview_url": business_context.get("preview_url", ""),
        }

    if task_type == "draft_reply":
        comment_text = business_context["comment_text"]
        product_name = business_context["product_name"]
        return {
            "reply": f"收到，关于“{comment_text}”这块我先给你一个简版说明。{product_name} 支持按你的业务场景做方案，我可以先发你案例和配置思路，你更关注价格、效果还是交付周期？"
        }

    if task_type == "next_action":
        score = business_context["score"]
        if score >= 80:
            stage = "高意向"
            action = "优先由销售在 10 分钟内跟进，并发送案例包与报价入口。"
        elif score >= 55:
            stage = "意向中"
            action = "发送产品资料与案例，确认客户最关注的需求点。"
        else:
            stage = "待培育"
            action = "先发送基础介绍，观察是否继续互动。"
        return {"stage": stage, "action": action, "reason": "基于评论意图关键词和互动强度评分。"}

    return output_schema


def score_comment(comment_text: str, like_count: int):
    score = 20 + min(like_count, 20)
    tags: list[str] = []

    for keyword in HIGH_INTENT_KEYWORDS:
        if keyword in comment_text:
            score += 35
            tags.append(f"高意向:{keyword}")

    for keyword in MEDIUM_INTENT_KEYWORDS:
        if keyword in comment_text:
            score += 15
            tags.append(f"关注点:{keyword}")

    if not tags:
        tags.append("待观察")

    if score >= 80:
        status = "高意向"
    elif score >= 55:
        status = "意向中"
    else:
        status = "新线索"

    summary = f"评论意图为 {status}，关键词标签：{'、'.join(tags)}。"
    return min(score, 100), tags, status, summary


def ensure_customer_thread(db: Session, lead: models.Lead):
    customer = db.query(models.Customer).filter(models.Customer.lead_id == lead.id).first()
    if not customer:
        customer = models.Customer(
            lead_id=lead.id,
            name=lead.customer_name,
            stage=lead.status,
            channel="微信/企微",
            notes=f"来源视频：{lead.source_video_url}",
        )
        db.add(customer)
        db.flush()
        add_audit(db, "customer", customer.id, "customer.created", "由 lead 自动创建客户档案")

    thread = db.query(models.ConversationThread).filter(models.ConversationThread.lead_id == lead.id).first()
    if not thread:
        thread = models.ConversationThread(
            lead_id=lead.id,
            customer_id=customer.id,
            channel="微信/企微",
            status="open",
            last_message="",
        )
        db.add(thread)
        db.flush()
        add_audit(db, "conversation_thread", thread.id, "thread.created", "自动创建跟进线程")

    return customer, thread


def serialize_project(project: models.ContentProject):
    return {
        "id": project.id,
        "product_id": project.product_id,
        "title": project.title,
        "target_audience": project.target_audience,
        "topic_direction": project.topic_direction,
        "status": project.status,
        "package_status": project.package_status,
        "script_json": loads(project.script_json, {}),
    }


def serialize_package(pkg: models.PublishPackage):
    return {
        "id": pkg.id,
        "content_project_id": pkg.content_project_id,
        "platform": pkg.platform,
        "title": pkg.title,
        "description": pkg.description,
        "hashtags": loads(pkg.hashtags, []),
        "cover_text": pkg.cover_text,
        "preview_url": pkg.preview_url,
        "approval_status": pkg.approval_status,
    }


def classify_asset(path: Path):
    suffix = path.suffix.lower()
    for asset_type, suffixes in ASSET_EXTENSIONS.items():
        if suffix in suffixes:
            return asset_type
    return None


def asset_category(path: Path):
    parts = path.parts
    if "产品图" in parts:
        return "产品图"
    if "数字人" in parts:
        return "数字人"
    if "AI视频" in parts:
        return "AI视频"
    return "资料文档"


def asset_public_url(relative_path: str):
    return f"/client-assets/{quote(relative_path, safe='/')}"


def serialize_asset(asset: models.ProductAsset):
    return {
        "id": asset.id,
        "product_id": asset.product_id,
        "title": asset.title,
        "asset_type": asset.asset_type,
        "category": asset.category,
        "source_path": asset.source_path,
        "relative_path": asset.relative_path,
        "public_url": asset.public_url,
        "file_size": asset.file_size,
    }


def sync_local_assets(db: Session):
    client_asset_root = asset_root()
    if not client_asset_root.exists():
        return

    product = db.query(models.Product).order_by(models.Product.id).first()
    if not product:
        product = models.Product(
            name="全铝家居 AI 视频生产系统",
            industry="家居制造",
            positioning="帮助工厂内部低门槛生成产品视频、工厂视频和发布包。",
            core_offer="资料管理、脚本分镜、视频生成、发布包输出",
            sales_regions="全国",
        )
        db.add(product)
        db.flush()
    else:
        product.name = "全铝家居 AI 视频生产系统"
        product.positioning = "帮助工厂内部低门槛生成产品视频、工厂视频和发布包。"
        product.core_offer = "资料管理、脚本分镜、视频生成、发布包输出"

    for file_path in client_asset_root.rglob("*"):
        if not file_path.is_file():
            continue
        asset_type = classify_asset(file_path)
        if not asset_type:
            continue
        relative_path = file_path.relative_to(client_asset_root).as_posix()
        title = file_path.stem.replace("_", " ").replace("-", " ")
        asset = db.query(models.ProductAsset).filter(models.ProductAsset.source_path == str(file_path)).first()
        if not asset:
            asset = models.ProductAsset(
                product_id=product.id,
                title=title,
                asset_type=asset_type,
                category=asset_category(file_path),
                source_path=str(file_path),
                relative_path=relative_path,
                public_url=asset_public_url(relative_path),
                file_size=file_path.stat().st_size,
            )
            db.add(asset)
        else:
            asset.title = title
            asset.asset_type = asset_type
            asset.category = asset_category(file_path)
            asset.relative_path = relative_path
            asset.public_url = asset_public_url(relative_path)
            asset.file_size = file_path.stat().st_size

        if asset_type in {"document", "spreadsheet"}:
            doc = (
                db.query(models.ProductKnowledgeDoc)
                .filter(models.ProductKnowledgeDoc.product_id == product.id, models.ProductKnowledgeDoc.title == title)
                .first()
            )
            if not doc:
                db.add(
                    models.ProductKnowledgeDoc(
                        product_id=product.id,
                        title=title,
                        doc_type=asset_type,
                        content=f"来源文件：{relative_path}。该资料已接入 AI 视频系统，可用于脚本和发布包生成。",
                        tags=dumps([asset_category(file_path), asset_type]),
                    )
                )

    first_video_asset = (
        db.query(models.ProductAsset)
        .filter(models.ProductAsset.asset_type == "video")
        .order_by(models.ProductAsset.id.asc())
        .first()
    )
    if first_video_asset:
        for pkg in db.query(models.PublishPackage).all():
            if not pkg.preview_url or "example.com" in pkg.preview_url:
                pkg.preview_url = first_video_asset.public_url
            if "获客" in pkg.title or "案例拆解" in pkg.title:
                pkg.title = pkg.title.replace("门店如何用 AI 做短视频获客", "工厂 AI 视频样片").replace("｜案例拆解", "｜产品展示版")
                pkg.description = "基于真实产品图、工厂图和数字人素材生成工厂视频发布包。"
                pkg.cover_text = "工厂 AI 视频"
                pkg.hashtags = dumps(["AI视频生成", "全铝家居", "工厂展示"])

    for project in db.query(models.ContentProject).all():
        script_json = loads(project.script_json, {})
        if (
            "获客" in project.title
            or project.title == "新建内容任务"
            or "获客" in script_json.get("hook", "")
        ):
            project.title = "全铝家居工厂 AI 视频样片"
            project.target_audience = "经销商、工程客户、定制家居客户"
            project.topic_direction = "用真实工厂和产品图生成工厂展示视频"
            project.material_constraints = "优先使用真实工厂和案例素材"
            project.script_json = dumps(
                {
                    "topic": "全铝家居工厂 AI 视频样片",
                    "hook": "不用再完全依赖外包视频团队，工厂内部也能快速出片。",
                    "scenes": [
                        {"scene": 1, "goal": "工厂实力", "shot": "展示工厂、设备和生产环境"},
                        {"scene": 2, "goal": "产品细节", "shot": "展示产品图、工艺、材质、案例"},
                        {"scene": 3, "goal": "引导咨询", "shot": "输出报价/案例/定制方案引导"},
                    ],
                    "hashtags": ["AI视频生成", "全铝家居", "工厂展示"],
                }
            )

    for pkg in db.query(models.PublishPackage).all():
        if "获客" in pkg.title or pkg.title.startswith("新建内容任务"):
            pkg.title = "全铝家居工厂 AI 视频样片｜产品展示版"
            pkg.description = "基于真实产品图、工厂图和数字人素材生成工厂视频发布包。"
            pkg.cover_text = "工厂 AI 视频"
            pkg.hashtags = dumps(["AI视频生成", "全铝家居", "工厂展示"])

    db.commit()


def serialize_capture_job(job: models.CaptureJob):
    return {
        "id": job.id,
        "source_links": loads(job.source_links, []),
        "trigger_mode": job.trigger_mode,
        "status": job.status,
        "strategy": loads(job.strategy_json, {}),
        "error_message": job.error_message,
    }


def serialize_lead(db: Session, lead: models.Lead):
    comment = db.query(models.Comment).filter(models.Comment.id == lead.comment_id).first()
    return {
        "id": lead.id,
        "comment_id": lead.comment_id,
        "source_video_url": lead.source_video_url,
        "customer_name": lead.customer_name,
        "status": lead.status,
        "score": lead.score,
        "tags": loads(lead.tags, []),
        "sales_owner": lead.sales_owner,
        "summary": lead.summary,
        "comment_text": comment.comment_text if comment else "",
        "video_title": comment.video_title if comment else "",
        "like_count": comment.like_count if comment else 0,
        "region": comment.region if comment else "未知",
    }


def serialize_draft(draft: models.MessageDraft):
    return {
        "id": draft.id,
        "lead_id": draft.lead_id,
        "thread_id": draft.thread_id,
        "content": draft.content,
        "approval_status": draft.approval_status,
        "approved": draft.approved,
    }


def latest_tasks(db: Session, limit: int = 20):
    return db.query(models.Task).order_by(desc(models.Task.created_at)).limit(limit).all()


def latest_audits(db: Session, limit: int = 20):
    return db.query(models.AuditLog).order_by(desc(models.AuditLog.created_at)).limit(limit).all()


def now():
    return datetime.utcnow()
