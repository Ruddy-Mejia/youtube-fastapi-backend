from pydantic import BaseModel
from datetime import datetime

from models.like import LikeType


# ============================================================
# CREATE
# ============================================================

class LikeCreate(BaseModel):
    video_id: int
    type: LikeType = LikeType.like


# ============================================================
# UPDATE
# ============================================================

class LikeUpdate(BaseModel):
    type: LikeType


# ============================================================
# OUT
# ============================================================

class LikeOut(BaseModel):
    id: int
    user_id: int
    video_id: int
    type: LikeType
    created_at: datetime

    model_config = {"from_attributes": True}
    
class LikeToggleResponse(BaseModel):
    action: str            # "created" | "updated" | "removed"
    like: LikeOut | None = None