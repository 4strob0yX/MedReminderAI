import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.usuario import Usuario
from app.schemas.auth import (
    LoginRequest,
    PasswordResetRequest,
    PasswordResetResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)


class EmailAlreadyRegistered(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class UserNotFound(Exception):
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

    rol_clean = (data.rol or "paciente").strip().lower()
    if rol_clean not in ("paciente", "cuidador"):
        rol_clean = "paciente"

    user = Usuario(
        nombre_completo=data.nombre,
        correo=correo,
        password_hash=hash_password(data.password),
        fecha_nacimiento=data.fecha_nacimiento,
        rol=rol_clean,
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


def refresh(db: Session, data: RefreshRequest) -> TokenResponse:
    try:
        user_id = decode_token(data.refresh_token, REFRESH)
    except (jwt.PyJWTError, ValueError):
        raise InvalidCredentials()

    user = db.get(Usuario, user_id)
    if user is None:
        raise InvalidCredentials()
    return _tokens_for(user)


def reset_password(db: Session, data: PasswordResetRequest) -> PasswordResetResponse:
    correo = data.email.lower()
    user = db.scalar(select(Usuario).where(Usuario.correo == correo))
    if user is None:
        raise UserNotFound()

    user.password_hash = hash_password(data.new_password)
    db.commit()
    tokens = _tokens_for(user)
    return PasswordResetResponse(
        mensaje="Contraseña actualizada correctamente",
        detail="Contraseña actualizada correctamente",
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
