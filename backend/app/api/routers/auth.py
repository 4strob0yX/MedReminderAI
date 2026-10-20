from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import (
    LoginRequest,
    PasswordResetRequest,
    PasswordResetResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UsuarioOut,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.register(db, data)
    except auth_service.EmailAlreadyRegistered:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="El correo ya esta registrado")


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, data)
    except auth_service.InvalidCredentials:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contrasena incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.refresh(db, data)
    except auth_service.InvalidCredentials:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/reset-password", response_model=PasswordResetResponse)
def reset_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.reset_password(db, data)
    except auth_service.UserNotFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="No encontramos una cuenta registrada con ese correo electrónico",
        )


@router.get("/me", response_model=UsuarioOut)
def me(user: Usuario = Depends(get_current_user)):
    return user
