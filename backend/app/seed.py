from __future__ import annotations

from . import models
from .services import add_audit, add_task, dumps, now, score_comment


def seed_demo_data(db):
    if db.query(models.Product).count() > 0:
        return

    product = models.Product(
        name="全铝家居 AI 视频生产系统",
        industry="家居制造",
        positioning="帮助工厂内部低门槛生成产品视频、工厂视频和发布包。",
        core_offer="资料管理、脚本分镜、视频生成、发布包输出",
        sales_regions="华南、华东、华中",
    )
    db.add(product)
    db.flush()

    docs = [
        models.ProductKnowledgeDoc(
            product_id=product.id,
            title="核心卖点",
            doc_type="faq",
            content="支持工厂实拍、产品图、数字人、案例图统一进入视频生产流程。",
            tags=dumps(["卖点", "产品"]),
        ),
        models.ProductKnowledgeDoc(
            product_id=product.id,
            title="视频生产 SOP",
            doc_type="workflow",
            content="先导入资料，再生成脚本和分镜，再导出视频发布包。",
            tags=dumps(["视频", "流程"]),
        ),
    ]
    db.add_all(docs)

    project = models.ContentProject(
        product_id=product.id,
        title="全铝家居工厂 AI 视频样片",
        target_audience="经销商、工程客户、定制家居客户",
        topic_direction="用真实工厂和产品图生成工厂展示视频",
        material_constraints="优先使用真实工厂和案例素材",
        status="script_ready",
        package_status="ready",
        script_json=dumps(
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
        ),
    )
    db.add(project)
    db.flush()

    pkg = models.PublishPackage(
        content_project_id=project.id,
        platform="douyin",
        title="全铝家居工厂 AI 视频样片｜产品展示版",
        description="基于真实产品图、工厂图和数字人素材生成工厂视频发布包。",
        hashtags=dumps(["AI视频生成", "全铝家居", "工厂展示"]),
        cover_text="工厂 AI 视频",
        preview_url="",
        approval_status="pending_review",
    )
    db.add(pkg)
    db.flush()

    video = models.VideoAsset(
        publish_package_id=pkg.id,
        platform="douyin",
        video_url="https://www.douyin.com/video/7411000000000000001",
        title=pkg.title,
        publish_status="ready_for_publish",
    )
    db.add(video)
    db.flush()

    capture_job = models.CaptureJob(
        source_links=dumps([video.video_url]),
        trigger_mode="manual_import",
        status="completed",
        strategy_json=dumps({"mode": "manual-json"}),
        started_at=now(),
        finished_at=now(),
    )
    db.add(capture_job)
    db.flush()

    comment_inputs = [
        {
            "nickname": "大东",
            "comment_text": "这款怎么卖？可以发报价吗？",
            "comment_time": "2026-03-27 10:18",
            "uid": "702",
            "douyin_id": "dadong88",
            "like_count": 18,
            "reply_count": 2,
            "gender": "男",
            "region": "重庆",
        },
        {
            "nickname": "安居思潮",
            "comment_text": "可以发个配置单吗？",
            "comment_time": "2026-03-27 10:26",
            "uid": "620",
            "douyin_id": "sale178",
            "like_count": 8,
            "reply_count": 1,
            "gender": "女",
            "region": "广东",
        },
        {
            "nickname": "外贸小王",
            "comment_text": "有重庆本地现货吗？",
            "comment_time": "2026-03-27 10:41",
            "uid": "617",
            "douyin_id": "lead570",
            "like_count": 5,
            "reply_count": 0,
            "gender": "男",
            "region": "重庆",
        },
    ]

    for item in comment_inputs:
        comment = models.Comment(
            platform="douyin",
            video_url=video.video_url,
            video_title=video.title,
            nickname=item["nickname"],
            comment_text=item["comment_text"],
            comment_time=item["comment_time"],
            uid=item["uid"],
            douyin_id=item["douyin_id"],
            like_count=item["like_count"],
            reply_count=item["reply_count"],
            gender=item["gender"],
            region=item["region"],
            raw_payload=dumps(item),
            dedupe_key=f"{video.video_url}::{item['nickname']}::{item['comment_text']}::{item['comment_time']}",
        )
        db.add(comment)
        db.flush()

        score, tags, status, summary = score_comment(comment.comment_text, comment.like_count)
        lead = models.Lead(
            comment_id=comment.id,
            source_video_url=video.video_url,
            customer_name=comment.nickname,
            status=status,
            score=score,
            tags=dumps(tags),
            sales_owner="销售一组",
            summary=summary,
        )
        db.add(lead)
        db.flush()

        customer = models.Customer(
            lead_id=lead.id,
            name=lead.customer_name,
            stage=lead.status,
            channel="微信/企微",
            notes=f"来源评论：{comment.comment_text}",
        )
        db.add(customer)
        db.flush()

        thread = models.ConversationThread(
            lead_id=lead.id,
            customer_id=customer.id,
            channel="微信/企微",
            status="open",
            last_message=comment.comment_text,
        )
        db.add(thread)
        db.flush()

        draft = models.MessageDraft(
            lead_id=lead.id,
            thread_id=thread.id,
            content=f"收到，关于“{comment.comment_text}”这块我先发你一个简版方案和案例。",
            approval_status="pending_review",
            approved=False,
        )
        db.add(draft)

        add_task(db, "lead_scoring", "lead", lead.id, "completed", summary)
        add_audit(db, "lead", lead.id, "lead.created", "由示例评论自动生成线索")

    add_task(db, "script_generation", "content_project", project.id, "completed", "已生成脚本与分镜")
    add_task(db, "publish_package_generation", "publish_package", pkg.id, "completed", "已生成发布包")
    add_task(db, "capture_import", "capture_job", capture_job.id, "completed", "已导入演示评论")
    add_audit(db, "content_project", project.id, "project.seeded", "已加载演示内容任务")
    add_audit(db, "publish_package", pkg.id, "package.seeded", "已加载演示发布包")

    db.commit()
