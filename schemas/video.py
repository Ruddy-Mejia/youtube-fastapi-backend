from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time

from schemas.user import UserShort
from schemas.category import CategoryShort


# ============================================================
# BASE
# ============================================================

class VideoBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    thumbnail_path: str = Field(..., max_length=255)
    duration: time
    is_published: bool = False
    status: bool = False


# ============================================================
# CREATE
# ============================================================

class VideoCreate(VideoBase):
    pass


# ============================================================
# UPDATE
# ============================================================

class VideoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    thumbnail_path: Optional[str] = Field(None, max_length=255)
    duration: Optional[time] = None
    is_published: Optional[bool] = None
    status: Optional[bool] = None


# ============================================================
# OUT
# ============================================================

class VideoOut(VideoBase):
    id: int
    user_id: int
    views: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VideoWithUser(VideoOut):
    owner: UserShort
    categories: List[CategoryShort] = []

    model_config = {"from_attributes": True}
    