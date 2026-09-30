from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=schemas.LikeToggleResponse, status_code=200)
def toggle_like(
    data: schemas.LikeCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Toggle de like/dislike:
    - No existe       → crea el like/dislike
    - Existe igual    → lo elimina
    - Existe distinto → lo actualiza al nuevo type
    """

    # Validar que el video existe
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

    # Buscar like existente del usuario autenticado
    existing = (
        db.query(models.Like)
        .filter(
            models.Like.user_id == current_user.id,   # ← del token
            models.Like.video_id == data.video_id,
        )
        .first()
    )

    # Caso 1: no existe → crear
    if existing is None:
        new_like = models.Like(
            user_id=current_user.id,                   # ← del token
            video_id=data.video_id,
            type=data.type,
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {"action": "created", "like": new_like}

    # Caso 2: existe con el mismo type → eliminar (toggle off)
    if existing.type == data.type:
        db.delete(existing)
        db.commit()
        return {"action": "removed", "like": None}

    # Caso 3: existe con type distinto → actualizar
    existing.type = data.type
    db.commit()
    db.refresh(existing)
    return {"action": "updated", "like": existing}


@router.get("", response_model=List[schemas.LikeOut])
def list_likes(
    video_id: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Lista de likes. Público (no requiere login).
    Filtra por video con ?video_id=X.
    """
    q = db.query(models.Like)
    if video_id is not None:
        q = q.filter(models.Like.video_id == video_id)
    return q.all()


@router.get("/me", response_model=List[schemas.LikeOut])
def my_likes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Likes del usuario autenticado."""
    return (
        db.query(models.Like)
        .filter(models.Like.user_id == current_user.id)
        .all()
    )


@router.put("/{like_id}", response_model=schemas.LikeOut)
def update_like(
    like_id: int,
    data: schemas.LikeUpdate,
    db: Session = Depends(get_db),
):
    like = db.query(models.Like).get(like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like no encontrado")

    like.type = data.type
    db.commit()
    db.refresh(like)
    return like


@router.delete("/{like_id}", status_code=204)
def delete_like(like_id: int, db: Session = Depends(get_db)):
    like = db.query(models.Like).get(like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like no encontrado")

    db.delete(like)
    db.commit()