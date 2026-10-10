from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class TratamientoCreate(BaseModel):
    id_medicamento: int = Field(gt=0)
    frecuencia_horas: int = Field(gt=0, le=168)
    # Si se omite, MySQL usa CURRENT_TIMESTAMP (UTC).
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    estado: Literal["activo", "inactivo"] = "activo"

    @field_validator("fecha_inicio", "fecha_fin")
    @classmethod
    def _a_utc_naive(cls, v: datetime | None) -> datetime | None:
        # Con zona horaria -> convertir a UTC; sin zona -> se asume UTC.
        if v is not None and v.tzinfo is not None:
            return v.astimezone(timezone.utc).replace(tzinfo=None)
        return v

    @model_validator(mode="after")
    def _rango_fechas(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin <= self.fecha_inicio:
            raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return self


class TratamientoOut(BaseModel):
    id_tratamiento: int
    id_medicamento: int
    frecuencia_horas: int
    fecha_inicio: datetime
    fecha_fin: datetime | None
    estado: Literal["activo", "inactivo"]

    model_config = {"from_attributes": True}
