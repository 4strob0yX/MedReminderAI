from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class RecordatorioOut(BaseModel):
    id_recordatorio: int
    id_tratamiento: int
    hora_programada: datetime  # UTC
    estado: Literal["pendiente", "tomado", "pospuesto", "omitido"]
    veces_pospuesto: int

    model_config = {"from_attributes": True}
