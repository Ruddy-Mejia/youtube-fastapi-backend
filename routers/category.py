from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from dependencies.auth import get_current_user


router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=schemas.CategoryOut, status_code=201)
def create_category(
    data: schemas.CategoryCreate,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    exists = (
        db.query(models.Category)
        .filter(models.Category.slug == data.slug)
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Slug ya registrado")

    new_category = models.Category(**data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("", response_model=List[schemas.CategoryOut])
def list_categories(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@router.get("/{category_id}", response_model=schemas.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    data: schemas.CategoryUpdate,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int,  current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(category)   # hard delete (no tiene softDeletes)
    db.commit()