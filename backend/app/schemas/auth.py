from datetime import date, datetime

from pydantic import AliasChoices, BaseModel, EmailStr, Field, computed_field, field_validator


class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)
    fecha_nacimiento: date | None = None
    rol: str = "paciente"

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


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1)


class PasswordResetRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(
        min_length=8,
        validation_alias=AliasChoices("new_password", "password", "nueva_password"),
    )

    @field_validator("new_password")
    @classmethod
    def _bcrypt_limit(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("La contrasena no puede exceder 72 bytes")
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PasswordResetResponse(BaseModel):
    mensaje: str = "Contraseña actualizada correctamente"
    detail: str = "Contraseña actualizada correctamente"
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "bearer"


class UpdatePerfilEdadRequest(BaseModel):
    fecha_nacimiento: date
    rol: str | None = None


class UsuarioOut(BaseModel):
    id_usuario: int
    nombre_completo: str
    correo: EmailStr
    fecha_nacimiento: date | None = None
    rol: str | None = "paciente"
    fecha_registro: datetime

    @computed_field
    @property
    def nombre(self) -> str:
        return self.nombre_completo.split(" ")[0] if self.nombre_completo else "Paciente"

    @computed_field
    @property
    def email(self) -> str:
        return str(self.correo)

    @computed_field
    @property
    def edad(self) -> int:
        if self.fecha_nacimiento is None:
            return 68  # Por defecto en cuentas demo geriátricas sin fecha registrada
        hoy = date.today()
        years = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            years -= 1
        return max(1, min(120, years))

    @computed_field
    @property
    def es_adulto_mayor(self) -> bool:
        return self.edad >= 60

    @computed_field
    @property
    def rango_edad(self) -> str:
        if self.edad >= 60:
            return "adulto_mayor"
        if self.edad < 30:
            return "joven"
        return "adulto"

    model_config = {"from_attributes": True}
