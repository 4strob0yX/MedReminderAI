from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ContactoCreate(BaseModel):
    nombre_completo: str = Field(min_length=1, max_length=255)
    telefono: str = Field(min_length=5, max_length=50)
    parentesco: str = Field(min_length=1, max_length=100)
    correo: str | None = Field(default=None, max_length=255)
    es_principal: bool = Field(default=True)

    @field_validator("nombre_completo", "telefono", "parentesco")
    @classmethod
    def _strip_fields(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El campo no puede estar vacío")
        return v


class ContactoOut(BaseModel):
    id_contacto: int
    nombre_completo: str
    telefono: str
    parentesco: str
    correo: str | None = None
    es_principal: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}
