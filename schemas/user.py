from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================================
# BASE
# ============================================================

class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    channel_name: str = Field(..., max_length=255)


# ============================================================
# CREATE
# ============================================================

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)
    photo_path: Optional[str] = Field(None, max_length=255)


# ============================================================
# UPDATE
# ============================================================

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    channel_name: Optional[str] = Field(None, max_length=255)
    photo_path: Optional[str] = Field(None, max_length=255)
    status: Optional[bool] = None


# ============================================================
# OUT
# ============================================================
class UserOut(UserBase):
    id: int
    photo_path: Optional[str] = None
    status: bool
    email_verified_at: Optional[datetime] = None
    created_at: datetime
    video_count: int = 0   # ← habría que calcularlo en el endpoint

    model_config = {"from_attributes": True}


class UserShort(BaseModel):
    id: int
    name: str
    channel_name: str
    photo_path: Optional[str] = None

    model_config = {"from_attributes": True}