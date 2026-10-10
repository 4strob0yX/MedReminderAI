from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class EmailAlreadyRegistered(Exception):
    pass


class InvalidCredentials(Exception):
    pass


def _tokens_for(user: Usuario) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id_usuario),
        refresh_token=create_refresh_token(user.id_usuario),
    )


def register(db: Session, data: RegisterRequest) -> TokenResponse:
    correo = data.email.lower()
    if db.scalar(select(Usuario.id_usuario).where(Usuario.correo == correo)):
        raise EmailAlreadyRegistered()

    user = Usuario(
        nombre_completo=data.nombre,
        correo=correo,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # carrera entre dos registros simultaneos (UNIQUE correo)
        db.rollback()
        raise EmailAlreadyRegistered()
    return _tokens_for(user)


def login(db: Session, data: LoginRequest) -> TokenResponse:
    user = db.scalar(select(Usuario).where(Usuario.correo == data.email.lower()))
    # Mensaje unico para correo inexistente o password erronea (no revelar cuentas).
    if user is None or not verify_password(data.password, user.password_hash):
        raise InvalidCredentials()
    return _tokens_for(user)
