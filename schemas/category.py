from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============================================================
# BASE
# ============================================================

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)


# ============================================================
# CREATE
# ============================================================

class CategoryCreate(CategoryBase):
    pass


# ============================================================
# UPDATE
# ============================================================

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)


# ============================================================
# OUT
# ============================================================

class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CategoryShort(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}