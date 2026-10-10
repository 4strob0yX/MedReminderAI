import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import ACCESS, decode_token
from app.db.session import get_db
from app.models.usuario import Usuario

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas o sesion expirada",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if creds is None:
        raise unauthorized
    try:
        user_id = decode_token(creds.credentials, ACCESS)
    except jwt.PyJWTError:
        raise unauthorized
    user = db.get(Usuario, user_id)
    if user is None:
        raise unauthorized
    return user
