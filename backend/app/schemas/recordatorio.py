from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RecordatorioOut(BaseModel):
    id_recordatorio: int
    id_tratamiento: int
    id_medicamento: int | None = None
    hora_programada: datetime  # UTC
    estado: Literal["pendiente", "tomado", "pospuesto", "omitido"]
    veces_pospuesto: int
    permite_posponer: bool = True
    posponer_bloqueado_por_castigo: bool = False
    es_critico: bool = False
    nombre_medicamento: str | None = None
    dosis: str | None = None
    forma_farmaceutica: str = "comprimidos"
    color_pastilla: str = "blanco"
    instrucciones_toma: str | None = None
    proposito: str | None = None
    cantidad_stock: int | None = None
    stock_inicial: int | None = None

    model_config = {"from_attributes": True}


class AdherenciaDiaOut(BaseModel):
    dia: str
    fecha: str
    tomadas: int
    programadas: int
    omitidas: int
    pospuestas: int
    porcentaje: float


class AdherenciaMedicamentoOut(BaseModel):
    id_medicamento: int
    nombre: str
    tomadas: int
    total: int
    porcentaje: float


class DiaMapaCalorOut(BaseModel):
    dia: str
    omisiones: int
    tomadas: int = 0
    total: int = 0


class BloqueMapaCalorOut(BaseModel):
    franja: str
    dias: list[DiaMapaCalorOut] = Field(default_factory=list)
    valores: list[int] = Field(default_factory=list)
    total_omisiones: int = 0


class EstadisticasOut(BaseModel):
    racha_dias: int
    color_fuego: Literal["gris", "naranja", "azul", "morado_dorado"]
    escudos_racha: int
    xp_honor: int
    xp_siguiente_rango: int = 100
    rango_honor: Literal["Hierro", "Bronce", "Plata", "Oro", "Diamante"]
    emblema_agrietado: bool
    posponer_bloqueado: bool
    dias_limpios_recuperacion: int
    requiere_alerta_cuidador: bool
    mensaje_alerta_cuidador: str | None = None
    contacto_principal_nombre: str | None = None
    contacto_principal_telefono: str | None = None
    porcentaje_global: float = 100.0
    total_tomadas: int = 0
    total_omitidas: int = 0
    total_pospuestas: int = 0
    adherencia_semanal: list[AdherenciaDiaOut]
    adherencia_por_medicamento: list[AdherenciaMedicamentoOut]
    mapa_calor: list[BloqueMapaCalorOut]
    insight_debilidad: str
