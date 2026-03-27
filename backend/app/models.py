from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Text

from .db import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    industry = Column(Text, nullable=False)
    positioning = Column(Text, nullable=False)
    core_offer = Column(Text, nullable=False)
    sales_regions = Column(Text, nullable=False)
    status = Column(Text, default="active", nullable=False)


class ProductKnowledgeDoc(Base, TimestampMixin):
    __tablename__ = "product_knowledge_docs"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    doc_type = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(Text, default="[]", nullable=False)


class ProductAsset(Base, TimestampMixin):
    __tablename__ = "product_assets"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    asset_type = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    source_path = Column(Text, nullable=False, unique=True)
    relative_path = Column(Text, nullable=False)
    public_url = Column(Text, nullable=False)
    file_size = Column(Integer, default=0, nullable=False)


class ContentProject(Base, TimestampMixin):
    __tablename__ = "content_projects"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False, index=True)
    title = Column(Text, nullable=False)
    target_audience = Column(Text, nullable=False)
    topic_direction = Column(Text, nullable=False)
    material_constraints = Column(Text, default="", nullable=False)
    status = Column(Text, default="draft", nullable=False)
    script_json = Column(Text, default="{}", nullable=False)
    package_status = Column(Text, default="pending", nullable=False)


class PublishPackage(Base, TimestampMixin):
    __tablename__ = "publish_packages"

    id = Column(Integer, primary_key=True)
    content_project_id = Column(Integer, nullable=False, index=True)
    platform = Column(Text, default="douyin", nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    hashtags = Column(Text, default="[]", nullable=False)
    cover_text = Column(Text, default="", nullable=False)
    preview_url = Column(Text, default="", nullable=False)
    approval_status = Column(Text, default="pending_review", nullable=False)
    approved_by = Column(Text, default="", nullable=False)


class VideoAsset(Base, TimestampMixin):
    __tablename__ = "video_assets"

    id = Column(Integer, primary_key=True)
    publish_package_id = Column(Integer, nullable=True, index=True)
    platform = Column(Text, default="douyin", nullable=False)
    video_url = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    publish_status = Column(Text, default="draft", nullable=False)


class CaptureJob(Base, TimestampMixin):
    __tablename__ = "capture_jobs"

    id = Column(Integer, primary_key=True)
    source_links = Column(Text, nullable=False)
    trigger_mode = Column(Text, default="manual", nullable=False)
    status = Column(Text, default="queued", nullable=False)
    strategy_json = Column(Text, default="{}", nullable=False)
    error_message = Column(Text, default="", nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    platform = Column(Text, default="douyin", nullable=False)
    video_url = Column(Text, nullable=False, index=True)
    video_title = Column(Text, nullable=False)
    nickname = Column(Text, nullable=False)
    comment_text = Column(Text, nullable=False)
    comment_time = Column(Text, nullable=False)
    uid = Column(Text, default="", nullable=False)
    douyin_id = Column(Text, default="", nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    reply_count = Column(Integer, default=0, nullable=False)
    gender = Column(Text, default="未知", nullable=False)
    region = Column(Text, default="未知", nullable=False)
    raw_payload = Column(Text, default="{}", nullable=False)
    dedupe_key = Column(Text, nullable=False, index=True)


class Lead(Base, TimestampMixin):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, nullable=False, index=True)
    source_video_url = Column(Text, nullable=False)
    customer_name = Column(Text, nullable=False)
    status = Column(Text, default="新线索", nullable=False)
    score = Column(Float, default=0.0, nullable=False)
    tags = Column(Text, default="[]", nullable=False)
    sales_owner = Column(Text, default="未分配", nullable=False)
    summary = Column(Text, default="", nullable=False)


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, nullable=False, index=True)
    name = Column(Text, nullable=False)
    stage = Column(Text, default="新线索", nullable=False)
    channel = Column(Text, default="微信/企微", nullable=False)
    notes = Column(Text, default="", nullable=False)


class ConversationThread(Base, TimestampMixin):
    __tablename__ = "conversation_threads"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, nullable=False, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    channel = Column(Text, default="微信/企微", nullable=False)
    status = Column(Text, default="open", nullable=False)
    last_message = Column(Text, default="", nullable=False)


class MessageDraft(Base, TimestampMixin):
    __tablename__ = "message_drafts"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, nullable=False, index=True)
    thread_id = Column(Integer, nullable=False, index=True)
    content = Column(Text, nullable=False)
    approval_status = Column(Text, default="pending_review", nullable=False)
    approved = Column(Boolean, default=False, nullable=False)


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task_type = Column(Text, nullable=False)
    entity_type = Column(Text, nullable=False)
    entity_id = Column(Integer, nullable=False)
    status = Column(Text, default="queued", nullable=False)
    detail = Column(Text, default="", nullable=False)


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    entity_type = Column(Text, nullable=False)
    entity_id = Column(Integer, nullable=False)
    action = Column(Text, nullable=False)
    detail = Column(Text, default="", nullable=False)
