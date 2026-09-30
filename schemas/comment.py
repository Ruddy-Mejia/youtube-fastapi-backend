from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from schemas.user import UserShort


# ============================================================
# BASE
# ============================================================

class CommentBase(BaseModel):
    body: str = Field(..., min_length=1)


# ============================================================
# CREATE
# ============================================================

class CommentCreate(CommentBase):
    user_id: int
    video_id: Optional[int] = None
    comment_id: Optional[int] = None   # si responde a otro comentario


# ============================================================
# UPDATE
# ============================================================

class CommentUpdate(BaseModel):
    body: Optional[str] = Field(None, min_length=1)


# ============================================================
# OUT
# ============================================================

class CommentOut(CommentBase):
    id: int
    user_id: int
    video_id: Optional[int] = None
    comment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CommentWithUser(CommentOut):
    user: UserShort

    model_config = {"from_attributes": True}


class CommentWithReplies(CommentWithUser):
    replies: List["CommentWithReplies"] = []

    model_config = {"from_attributes": True}


# Necesario para que Pydantic resuelva la autoreferencia
CommentWithReplies.model_rebuild()