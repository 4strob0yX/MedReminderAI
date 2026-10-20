from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS = "access"
REFRESH = "refresh"


def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    if not plain or not hashed:
        return False
    try:
        return _pwd_context.verify(plain, hashed)
    except (ValueError, TypeError):
        return False


def _create_token(user_id: int, token_type: str, expires: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),  # PyJWT >= 2.10 exige que sub sea str
        "type": token_type,
        "iat": now,
        "exp": now + expires,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int) -> str:
    return _create_token(user_id, ACCESS, timedelta(minutes=settings.access_token_minutes))


def create_refresh_token(user_id: int) -> str:
    return _create_token(user_id, REFRESH, timedelta(days=settings.refresh_token_days))


def decode_token(token: str, expected_type: str) -> int:
    """Devuelve el id de usuario. Lanza jwt.PyJWTError si es invalido, expirado o de tipo incorrecto."""
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["exp", "sub", "type"]},
    )
    if payload["type"] != expected_type:
        raise jwt.InvalidTokenError("Tipo de token incorrecto")
    return int(payload["sub"])
