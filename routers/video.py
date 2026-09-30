from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from dependencies.auth import get_current_user


router = APIRouter(prefix="/videos", tags=["videos"])

@router.post("", response_model=schemas.VideoOut, status_code=201)
def create_video(
    video: schemas.VideoCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = video.model_dump()
    data["user_id"] = current_user.id   # ← el user_id viene del token

    new_video = models.Video(**data)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video


@router.get("", response_model=List[schemas.VideoWithUser])
def list_videos(
    published_only: bool = False,
    db: Session = Depends(get_db),
):
    q = db.query(models.Video).filter(models.Video.deleted_at.is_(None))
    if published_only:
        q = q.filter(models.Video.is_published.is_(True))
    return q.all()


@router.get("/{video_id}", response_model=schemas.VideoWithUser)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = (
        db.query(models.Video)
        .filter(
            models.Video.id == video_id,
            models.Video.deleted_at.is_(None),
        )
        .first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return video


@router.put("/{video_id}", response_model=schemas.VideoOut)
def update_video(
    video_id: int,
    data: schemas.VideoUpdate,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    video = (
        db.query(models.Video)
        .filter(
            models.Video.id == video_id,
            models.Video.deleted_at.is_(None),
        )
        .first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(video, field, value)

    db.commit()
    db.refresh(video)
    return video


@router.delete("/{video_id}", status_code=204)
def delete_video(video_id: int,  current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    video = (
        db.query(models.Video)
        .filter(
            models.Video.id == video_id,
            models.Video.deleted_at.is_(None),
        )
        .first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")

    video.deleted_at = datetime.utcnow()
    db.commit()