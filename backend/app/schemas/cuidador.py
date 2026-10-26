from datetime import datetime

from pydantic import BaseModel, Field


class AlertaCuidadorCreate(BaseModel):
    tipo_alerta: str = Field(default="advertencia_normal")  # "critica_automatica" | "advertencia_normal"
    accion_origen: str = Field(default="posponer")  # "omitir" | "posponer" | "alarma_vencida"
    nombre_medicamento: str
    dosis: str = ""
    es_critico: bool = False
    mensaje: str | None = None


class AlertaCuidadorOut(BaseModel):
    id_alerta: int
    tipo_alerta: str
    accion_origen: str
    nombre_medicamento: str
    dosis: str
    es_critico: bool
    mensaje: str
    nombre_cuidador: str
    telefono_cuidador: str
    atendida: bool
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class TomaSupervisadaItem(BaseModel):
    id_recordatorio: int
    nombre_medicamento: str
    dosis: str
    hora_programada: datetime
    estado: str
    es_critico: bool
    veces_pospuesto: int


class CuidadorPanelResponse(BaseModel):
    paciente_nombre: str
    paciente_edad: int
    es_adulto_mayor: bool
    rango_edad_label: str
    adherencia_hoy_pct: int
    tomas_completadas_hoy: int
    tomas_pendientes_hoy: int
    tomas_omitidas_hoy: int
    estado_riesgo: str
    nombre_cuidador: str
    telefono_cuidador: str
    parentesco_cuidador: str
    alertas_no_atendidas: int
    alertas: list[AlertaCuidadorOut]
    tomas_hoy: list[TomaSupervisadaItem]
