from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AlergiaCreate(BaseModel):
    sustancia: str = Field(min_length=1, max_length=255)
    severidad: Literal["leve", "moderada", "grave"] = Field(default="grave")
    reaccion: str | None = Field(default=None, max_length=255)

    @field_validator("sustancia")
    @classmethod
    def _strip_sustancia(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("La sustancia no puede estar vacía")
        return v


class AlergiaOut(BaseModel):
    id_alergia: int
    sustancia: str
    severidad: str
    reaccion: str | None = None
    fecha_registro: datetime

    model_config = {"from_attributes": True}
