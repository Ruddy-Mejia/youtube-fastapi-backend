from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from security import decode_access_token
import models


# HTTPBearer extrae el token del header Authorization automáticamente
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o ausente",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = (
        db.query(models.User)
        .filter(
            models.User.id == int(user_id),
            models.User.deleted_at.is_(None),
        )
        .first()
    )
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Igual que get_current_user pero exige status=True."""
    if not current_user.status:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    return current_user