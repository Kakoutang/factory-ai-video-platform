from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ProductOut(BaseModel):
    id: int
    name: str
    industry: str
    positioning: str
    core_offer: str

    class Config:
        from_attributes = True


class ContentProjectCreate(BaseModel):
    product_id: int
    title: str
    target_audience: str
    topic_direction: str
    material_constraints: str = ""


class ContentProjectOut(BaseModel):
    id: int
    product_id: int
    title: str
    target_audience: str
    topic_direction: str
    status: str
    package_status: str
    script_json: dict[str, Any]


class GenerateScriptResponse(BaseModel):
    project_id: int
    status: str
    script: dict[str, Any]


class OperationsManualSectionOut(BaseModel):
    title: str
    body: str
    summary: str


class CourseSourceOut(BaseModel):
    filename: str
    source_type: str
    title: str
    path: str


class OperationsManualOut(BaseModel):
    title: str
    version: str
    source_count: int
    unique_course_count: int
    sections: List[OperationsManualSectionOut]
    sources: List[CourseSourceOut]


class PublishPackageOut(BaseModel):
    id: int
    content_project_id: int
    platform: str
    title: str
    description: str
    hashtags: List[str]
    cover_text: str
    preview_url: str
    approval_status: str


class ApproveRequest(BaseModel):
    approved_by: str = "系统管理员"


class ProductAssetOut(BaseModel):
    id: int
    product_id: int
    title: str
    asset_type: str
    category: str
    source_path: str
    relative_path: str
    public_url: str
    file_size: int


class CaptureJobCreate(BaseModel):
    source_links: List[str]
    trigger_mode: str = "manual"
    strategy: dict[str, Any] = Field(default_factory=dict)


class CaptureJobOut(BaseModel):
    id: int
    source_links: List[str]
    trigger_mode: str
    status: str
    strategy: dict[str, Any]
    error_message: str


class ImportedComment(BaseModel):
    nickname: str
    comment: str
    time: str
    uid: str = ""
    douyinId: str = ""
    gender: str = "未知"
    region: str = "未知"
    likeCount: int = 0
    replyCount: int = 0


class ManualImportPage(BaseModel):
    url: str
    title: str


class ManualImportPayload(BaseModel):
    source: str = "manual-browser-collector"
    collectedAt: str
    page: ManualImportPage
    comments: List[ImportedComment]


class LeadScoreRequest(BaseModel):
    comment_ids: Optional[List[int]] = None


class LeadOut(BaseModel):
    id: int
    comment_id: int
    source_video_url: str
    customer_name: str
    status: str
    score: float
    tags: List[str]
    sales_owner: str
    summary: str
    comment_text: str
    video_title: str
    like_count: int
    region: str


class ReplyDraftResponse(BaseModel):
    draft_id: int
    thread_id: int
    content: str
    approval_status: str


class NextActionResponse(BaseModel):
    lead_id: int
    stage: str
    action: str
    reason: str


class MessageDraftOut(BaseModel):
    id: int
    lead_id: int
    thread_id: int
    content: str
    approval_status: str
    approved: bool


class CustomerOut(BaseModel):
    id: int
    lead_id: int
    name: str
    stage: str
    channel: str
    notes: str


class TaskOut(BaseModel):
    id: int
    task_type: str
    entity_type: str
    entity_id: int
    status: str
    detail: str


class AuditLogOut(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    action: str
    detail: str


class SummaryOut(BaseModel):
    content_projects: int
    publish_packages: int
    comments: int
    leads: int
    customers: int
    drafts_pending: int
    asset_files: int
    local_images: int
    local_videos: int
    knowledge_docs: int
    course_sources: int
