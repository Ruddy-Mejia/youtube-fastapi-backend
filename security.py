import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from jose import JWTError, jwt
from pwdlib import PasswordHash


load_dotenv()

# ---------- Configuración ----------
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

if not JWT_SECRET_KEY:
    raise RuntimeError("Falta JWT_SECRET_KEY en .env")

# ---------- Hash de contraseñas ----------
pwd_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------- JWT ----------
def create_access_token(user_id: int, expires_minutes: Optional[int] = None) -> str:
    """
    Genera un JWT con 'sub' (subject = user_id) y 'exp' (expiración).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or JWT_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),       # JWT exige que sub sea string
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Devuelve el payload si el token es válido, o None si no lo es.
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None