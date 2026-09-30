from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
import models
import schemas
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=schemas.CommentOut, status_code=201)
def create_comment(
    data: schemas.CommentCreate,
    db: Session = Depends(get_db),
):
    # Validar usuario
    user = (
        db.query(models.User)
        .filter(
            models.User.id == data.user_id,
            models.User.deleted_at.is_(None),
        )
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    # Validar video (si se especificó)
    if data.video_id is not None:
        video = (
            db.query(models.Video)
            .filter(
                models.Video.id == data.video_id,
                models.Video.deleted_at.is_(None),
            )
            .first()
        )
        if not video:
            raise HTTPException(status_code=404, detail="Video no existe")

    # Validar comentario padre (si es respuesta)
    if data.comment_id is not None:
        parent = (
            db.query(models.Comment)
            .filter(
                models.Comment.id == data.comment_id,
                models.Comment.deleted_at.is_(None),
            )
            .first()
        )
        if not parent:
            raise HTTPException(status_code=404, detail="Comentario padre no existe")

    # Regla: al menos uno de video_id o comment_id debe estar presente
    if data.video_id is None and data.comment_id is None:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar video_id o comment_id",
        )

    new_comment = models.Comment(**data.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("", response_model=List[schemas.CommentWithUser])
def list_comments(
    video_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
):
    q = (
        db.query(models.Comment)
        .options(joinedload(models.Comment.user))
        .filter(models.Comment.deleted_at.is_(None))
    )
    if video_id is not None:
        q = q.filter(models.Comment.video_id == video_id)
    if user_id is not None:
        q = q.filter(models.Comment.user_id == user_id)
    return q.all()


@router.get("/{comment_id}", response_model=schemas.CommentWithReplies)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = (
        db.query(models.Comment)
        .options(
            joinedload(models.Comment.user),
            joinedload(models.Comment.replies).joinedload(models.Comment.user),
        )
        .filter(
            models.Comment.id == comment_id,
            models.Comment.deleted_at.is_(None),
        )
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comment


@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(
    comment_id: int,
    data: schemas.CommentUpdate,
    db: Session = Depends(get_db),
):
    comment = (
        db.query(models.Comment)
        .filter(
            models.Comment.id == comment_id,
            models.Comment.deleted_at.is_(None),
        )
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(comment, field, value)

    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = (
        db.query(models.Comment)
        .filter(
            models.Comment.id == comment_id,
            models.Comment.deleted_at.is_(None),
        )
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")

    comment.deleted_at = datetime.utcnow()
    db.commit()