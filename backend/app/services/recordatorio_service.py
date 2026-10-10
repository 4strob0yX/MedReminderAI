from datetime import datetime, timedelta, timezone

from app.models.recordatorio import Recordatorio
from app.models.tratamiento import Tratamiento

HORIZONTE_DIAS = 7  # MVP: no proyectar mas alla de una semana.


def generar_recordatorios(
    trat: Tratamiento, ahora: datetime | None = None
) -> list[Recordatorio]:
    """Calcula los recordatorios de un tratamiento en el rango
    [fecha_inicio, fecha_inicio + 7 dias), cada `frecuencia_horas`, sin pasar de
    `fecha_fin` si existe. Todas las horas son UTC naive (convencion de la BD).
    Se itera todo el rango para conservar la cadencia de los ciclos, pero solo se
    crean los recordatorios con hora_programada >= UTC_NOW (nada nace caducado).
    Un tratamiento inactivo no genera nada. No toca la sesion: solo construye objetos."""
    if trat.estado != "activo":
        return []

    if ahora is None:
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)

    paso = timedelta(hours=trat.frecuencia_horas)
    limite: datetime = trat.fecha_inicio + timedelta(days=HORIZONTE_DIAS)
    if trat.fecha_fin is not None:
        limite = min(limite, trat.fecha_fin)

    recordatorios: list[Recordatorio] = []
    hora = trat.fecha_inicio
    while hora < limite:
        if hora >= ahora:
            recordatorios.append(
                Recordatorio(
                    id_tratamiento=trat.id_tratamiento,
                    hora_programada=hora,
                    estado="pendiente",
                    veces_pospuesto=0,
                )
            )
        hora += paso
    return recordatorios
