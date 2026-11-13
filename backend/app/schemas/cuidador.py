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


class CodigoVinculacionOut(BaseModel):
    id_vinculacion: int
    codigo_vinculacion: str
    estado: str
    expira_en: datetime


class VincularPacienteRequest(BaseModel):
    codigo_vinculacion: str = Field(min_length=4, max_length=20)
    parentesco: str | None = Field(default=None, max_length=100)


class PacienteVinculadoItem(BaseModel):
    id_vinculacion: int
    id_paciente: int
    nombre_paciente: str
    correo_paciente: str
    edad_paciente: int
    parentesco: str | None = None
    estado_riesgo: str
    alertas_no_atendidas: int
    fecha_vinculacion: datetime | None = None


class CuidadorVinculadoItem(BaseModel):
    id_vinculacion: int
    id_cuidador: int
    nombre_cuidador: str
    correo_cuidador: str
    parentesco: str | None = None
    fecha_vinculacion: datetime | None = None


class VinculacionesResumenOut(BaseModel):
    como_cuidador: list[PacienteVinculadoItem] = Field(default_factory=list)
    cuidadores_vinculados: list[CuidadorVinculadoItem] = Field(default_factory=list)
    codigo_activo: CodigoVinculacionOut | None = None


class CuidadorPanelResponse(BaseModel):
    id_paciente: int
    paciente_nombre: str
    correo_paciente: str | None = None
    paciente_edad: int
    es_adulto_mayor: bool
    rango_edad_label: str
    adherencia_hoy_pct: int
    tomas_totales_hoy: int
    tomas_completadas_hoy: int
    tomas_pendientes_hoy: int
    tomas_omitidas_hoy: int
    tomas_criticas_omitidas_hoy: int = 0
    estado_riesgo: str
    estado_riesgo_label: str
    nombre_cuidador: str
    telefono_cuidador: str
    parentesco_cuidador: str
    alertas_no_atendidas: int
    paciente_vinculado: bool = True
    alertas: list[AlertaCuidadorOut]
    tomas_hoy: list[TomaSupervisadaItem]
