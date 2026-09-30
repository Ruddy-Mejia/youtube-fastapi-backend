from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from security import pwd_context
from dependencies.auth import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    exists = (
        db.query(models.User)
        .filter(models.User.channel_name == user.channel_name)
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Nombre de canal ya registrado")

    data = user.model_dump()
    data["password"] = pwd_context.hash(data["password"])

    new_user = models.User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("", response_model=List[schemas.UserOut])
def list_users(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(models.User)
        .filter(models.User.deleted_at.is_(None))
        .all()
    )


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(
            models.User.id == user_id,
            models.User.deleted_at.is_(None),
        )
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    data: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(
            models.User.id == user_id,
            models.User.deleted_at.is_(None),
        )
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(
            models.User.id == user_id,
            models.User.deleted_at.is_(None),
        )
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.deleted_at = datetime.utcnow()
    db.commit()