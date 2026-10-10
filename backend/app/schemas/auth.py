from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("nombre")
    @classmethod
    def _strip_nombre(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacio")
        return v

    @field_validator("password")
    @classmethod
    def _bcrypt_limit(cls, v: str) -> str:
        # bcrypt solo procesa 72 bytes; rechazar en vez de truncar en silencio.
        if len(v.encode("utf-8")) > 72:
            raise ValueError("La contrasena no puede exceder 72 bytes")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UsuarioOut(BaseModel):
    id_usuario: int
    nombre_completo: str
    correo: EmailStr
    fecha_registro: datetime

    model_config = {"from_attributes": True}
