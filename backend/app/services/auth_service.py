import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select, update
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
from app.models.password_reset import PasswordResetCode
from app.models.usuario import Usuario
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    PasswordResetRequest,
    PasswordResetResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UpdatePerfilRequest,
)


class EmailAlreadyRegistered(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidResetCode(Exception):
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


def request_password_reset(db: Session, data: ForgotPasswordRequest) -> ForgotPasswordResponse:
    correo = data.email.lower()
    user = db.scalar(select(Usuario).where(Usuario.correo == correo))
    demo_code: str | None = None
    exp_minutes = 15

    if user is not None:
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)
        db.execute(
            update(PasswordResetCode)
            .where(
                PasswordResetCode.id_usuario == user.id_usuario,
                PasswordResetCode.usado.is_(False),
            )
            .values(usado=True)
        )
        code = f"{secrets.randbelow(900000) + 100000}"
        reset_entry = PasswordResetCode(
            id_usuario=user.id_usuario,
            codigo_hash=hash_password(code),
            expira_en=ahora + timedelta(minutes=exp_minutes),
            usado=False,
        )
        db.add(reset_entry)
        db.commit()
        if os.environ.get("EXPOSE_RESET_CODE_DEMO", "true").lower() == "true":
            demo_code = code

    msg = (
        "Si tu correo está registrado, generamos un código de verificación "
        f"válido por {exp_minutes} minutos."
    )
    return ForgotPasswordResponse(
        mensaje=msg,
        detail=msg,
        expira_en_minutos=exp_minutes,
        demo_code=demo_code,
    )


def reset_password(db: Session, data: PasswordResetRequest) -> PasswordResetResponse:
    correo = data.email.lower()
    user = db.scalar(select(Usuario).where(Usuario.correo == correo))
    if user is None:
        raise InvalidResetCode()

    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    codigos_activos = db.scalars(
        select(PasswordResetCode)
        .where(
            PasswordResetCode.id_usuario == user.id_usuario,
            PasswordResetCode.usado.is_(False),
            PasswordResetCode.expira_en >= ahora,
        )
        .order_by(PasswordResetCode.id_reset.desc())
        .limit(3)
    ).all()

    codigo_limpio = data.codigo.strip()
    matched = next(
        (c for c in codigos_activos if verify_password(codigo_limpio, c.codigo_hash)),
        None,
    )
    if matched is None:
        raise InvalidResetCode()

    matched.usado = True
    user.password_hash = hash_password(data.new_password)
    db.commit()
    tokens = _tokens_for(user)
    return PasswordResetResponse(
        mensaje="Contraseña actualizada correctamente",
        detail="Contraseña actualizada correctamente",
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


def change_password(db: Session, user: Usuario, data: ChangePasswordRequest) -> None:
    if not verify_password(data.current_password, user.password_hash):
        raise InvalidCredentials()
    user.password_hash = hash_password(data.new_password)
    db.commit()


def update_perfil(db: Session, user: Usuario, data: UpdatePerfilRequest) -> Usuario:
    if data.nombre_completo is not None:
        user.nombre_completo = data.nombre_completo
    if data.fecha_nacimiento is not None:
        user.fecha_nacimiento = data.fecha_nacimiento
    if data.rol in ("paciente", "cuidador"):
        user.rol = data.rol
    db.commit()
    db.refresh(user)
    return user
