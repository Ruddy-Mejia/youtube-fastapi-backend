from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies.auth import get_current_user

from database import get_db
from security import verify_password, create_access_token
import models
import schemas


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    user = (
        db.query(models.User)
        .filter(
            models.User.email == data.email,
            models.User.deleted_at.is_(None),
        )
        .first()
    )

    # Mensaje genérico: no reveles si el email existe o no
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    token = create_access_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user