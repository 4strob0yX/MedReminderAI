from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class TratamientoCreate(BaseModel):
    id_medicamento: int = Field(gt=0)
    frecuencia_horas: int = Field(gt=0, le=168)
    # Si se omite, MySQL usa CURRENT_TIMESTAMP (UTC).
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    estado: Literal["activo", "inactivo"] = "activo"

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
