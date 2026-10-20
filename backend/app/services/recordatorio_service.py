from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.mongo import registrar_evento_mongo
from app.models.contacto import ContactoApoyo
from app.models.medicamento import Medicamento
from app.models.recordatorio import HistorialToma, Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.recordatorio import (
    AdherenciaDiaOut,
    AdherenciaMedicamentoOut,
    BloqueMapaCalorOut,
    DiaMapaCalorOut,
    EstadisticasOut,
)

HORIZONTE_DIAS = 7  # Proyección continua de 7 días
VENTANA_TOLERANCIA_HORAS = 2  # Vencimiento automático de pendientes tras 2 horas

DIAS_SEMANA_ESP = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
FRANJAS_MAPA_CALOR = [
    "Mañana (6-11h)",
    "Mediodía (12-15h)",
    "Tarde (16-19h)",
    "Noche (20-23h)",
]


def generar_recordatorios(
    trat: Tratamiento, ahora: datetime | None = None
) -> list[Recordatorio]:
    """Calcula los recordatorios de un tratamiento en el rango
    [fecha_inicio, fecha_inicio + 7 dias), cada `frecuencia_horas`, sin pasar de
    `fecha_fin` si existe. Todas las horas son UTC naive (convencion de la BD).
    Corrige el truncamiento de microsegundos de MySQL restando 2 minutos al umbral
    `ahora.replace(microsecond=0)` para que la primera dosis nunca se omita al crear."""
    if trat.estado != "activo" or trat.frecuencia_horas <= 0:
        return []

    if ahora is None:
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)

    umbral = ahora.replace(microsecond=0) - timedelta(minutes=2)
    paso = timedelta(hours=trat.frecuencia_horas)
    limite: datetime = max(trat.fecha_inicio, ahora.replace(microsecond=0)) + timedelta(
        days=HORIZONTE_DIAS
    )
    if trat.fecha_fin is not None:
        limite = min(limite, trat.fecha_fin)

    recordatorios: list[Recordatorio] = []
    hora = trat.fecha_inicio
    while hora < limite:
        if hora >= umbral:
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


def asegurar_horizonte_recordatorios(
    db: Session, id_usuario: int, ahora: datetime | None = None
) -> None:
    """1) Marca como `omitido` los recordatorios `pendiente` cuya ventana de horario
       ya venció (`hora_programada < ahora - 2h`) y registra en `historial_toma`.
    2) Extiende el horizonte móvil de 7 días para todos los tratamientos activos del usuario."""
    if ahora is None:
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)

    hubo_cambios = False

    # 1. Timeout automático de recordatorios vencidos
    corte_vencimiento = ahora - timedelta(hours=VENTANA_TOLERANCIA_HORAS)
    stmt_vencidos = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(
            Medicamento.id_usuario == id_usuario,
            Recordatorio.estado == "pendiente",
            Recordatorio.hora_programada < corte_vencimiento,
        )
    )
    vencidos = db.execute(stmt_vencidos).all()
    for rec, med in vencidos:
        rec.estado = "omitido"
        db.add(
            HistorialToma(
                id_recordatorio=rec.id_recordatorio,
                estado_final="omitido",
                notas="Omitido automáticamente por vencimiento de ventana de horario",
            )
        )
        registrar_evento_mongo(
            evento="toma_omitida",
            id_usuario=id_usuario,
            detalle={
                "id_recordatorio": rec.id_recordatorio,
                "medicamento": med.nombre,
                "es_critico": med.es_critico,
                "motivo": "timeout_ventana",
            },
        )
        hubo_cambios = True

    # 2. Extensión de horizonte móvil de 7 días para tratamientos activos
    stmt_trats = (
        select(Tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(
            Medicamento.id_usuario == id_usuario,
            Tratamiento.estado == "activo",
        )
    )
    tratamientos = db.scalars(stmt_trats).all()
    umbral_ahora = ahora.replace(microsecond=0) - timedelta(minutes=2)

    for trat in tratamientos:
        if trat.frecuencia_horas <= 0:
            continue
        limite = ahora + timedelta(days=HORIZONTE_DIAS)
        if trat.fecha_fin is not None:
            limite = min(limite, trat.fecha_fin)
        if limite <= umbral_ahora:
            continue

        max_existente: datetime | None = db.scalar(
            select(func.max(Recordatorio.hora_programada)).where(
                Recordatorio.id_tratamiento == trat.id_tratamiento
            )
        )

        paso = timedelta(hours=trat.frecuencia_horas)
        hora = trat.fecha_inicio

        # Si fecha_inicio quedó muy atrás en el pasado, saltar múltiplos de `paso` hasta alcanzar `umbral_ahora`
        if hora < umbral_ahora:
            segundos_diff = (umbral_ahora - hora).total_seconds()
            paso_segundos = paso.total_seconds()
            saltos = int(segundos_diff // paso_segundos)
            if saltos > 0:
                hora = hora + timedelta(seconds=saltos * paso_segundos)
            while hora < umbral_ahora:
                hora += paso

        # Margen de 90 min sobre el último recordatorio existente por si fue pospuesto hasta 2 veces
        corte_existente = (
            max_existente + timedelta(minutes=90) if max_existente is not None else None
        )

        nuevos: list[Recordatorio] = []
        while hora < limite:
            if hora >= umbral_ahora and (corte_existente is None or hora > corte_existente):
                nuevos.append(
                    Recordatorio(
                        id_tratamiento=trat.id_tratamiento,
                        hora_programada=hora,
                        estado="pendiente",
                        veces_pospuesto=0,
                    )
                )
            hora += paso

        if nuevos:
            db.add_all(nuevos)
            hubo_cambios = True

    if hubo_cambios:
        db.commit()


def _calcular_rango_honor(
    xp: int,
) -> tuple[str, int]:
    """Devuelve `(rango_honor, xp_siguiente_rango)`."""
    if xp < 100:
        return "Hierro", 100
    if xp < 250:
        return "Bronce", 250
    if xp < 500:
        return "Plata", 500
    if xp < 900:
        return "Oro", 900
    return "Diamante", 1500


def _indice_franja_horaria(hora_24: int) -> int:
    """Mapea una hora local (0..23) a uno de los 4 bloques del mapa de calor."""
    if 6 <= hora_24 <= 11:
        return 0  # Mañana (6-11h)
    if 12 <= hora_24 <= 15:
        return 1  # Mediodía (12-15h)
    if 16 <= hora_24 <= 19:
        return 2  # Tarde (16-19h)
    return 3  # Noche (20-23h y madrugada)


def _calcular_racha_y_castigo(
    recs_meds: list[tuple[Recordatorio, Medicamento]],
    hist_meds: list[tuple[HistorialToma, Recordatorio, Medicamento]],
    ahora_utc: datetime,
    tz_offset_minutes: int,
) -> tuple[int, str, int, int, int, str, bool, bool, int, bool, str | None]:
    """Calcula métricas de racha, fuego evolutivo, XP, Rango de Honor y estado de castigo."""
    delta_tz = timedelta(minutes=tz_offset_minutes)
    hoy_local: date = (ahora_utc + delta_tz).date()

    # Agrupar recordatorios por fecha local
    por_fecha: dict[date, list[tuple[Recordatorio, Medicamento]]] = {}
    for rec, med in recs_meds:
        f_local = (rec.hora_programada + delta_tz).date()
        por_fecha.setdefault(f_local, []).append((rec, med))

    # Calcular racha_dias consecutivos hacia atrás desde hoy_local
    racha_dias = 0
    recs_hoy = por_fecha.get(hoy_local, [])
    omitidas_hoy = sum(1 for r, _ in recs_hoy if r.estado == "omitido")
    tomadas_hoy = sum(1 for r, _ in recs_hoy if r.estado == "tomado")

    if omitidas_hoy > 0:
        racha_dias = 0
    else:
        if tomadas_hoy > 0:
            racha_dias += 1
        dia_cursor = hoy_local - timedelta(days=1)
        while True:
            items_dia = por_fecha.get(dia_cursor, [])
            if not items_dia:
                break
            omit_dia = sum(1 for r, _ in items_dia if r.estado == "omitido")
            tom_dia = sum(1 for r, _ in items_dia if r.estado == "tomado")
            if omit_dia == 0 and tom_dia > 0:
                racha_dias += 1
                dia_cursor -= timedelta(days=1)
            else:
                break

    if racha_dias <= 0:
        color_fuego = "gris"
    elif racha_dias <= 6:
        color_fuego = "naranja"
    elif racha_dias <= 29:
        color_fuego = "azul"
    else:
        color_fuego = "morado_dorado"

    escudos_racha = min(3, racha_dias // 7)

    # Calcular XP de Honor desde historial_toma (o desde el estado del recordatorio si no hubiera fila)
    xp_raw = 0
    if hist_meds:
        for h, _rec, med in hist_meds:
            if h.estado_final == "tomado":
                xp_raw += 25
            elif h.estado_final == "pospuesto":
                xp_raw += 5
            elif h.estado_final == "omitido":
                xp_raw -= 80 if med.es_critico else 40
    else:
        for rec, med in recs_meds:
            if rec.estado == "tomado":
                xp_raw += 25
            elif rec.estado == "omitido":
                xp_raw -= 80 if med.es_critico else 40
            xp_raw += rec.veces_pospuesto * 5

    xp_honor = max(0, xp_raw)
    rango_honor, xp_siguiente = _calcular_rango_honor(xp_honor)

    # Evaluar omisiones recientes (últimas 48h y últimos 3 días)
    hace_48h = ahora_utc - timedelta(hours=48)
    hace_3d = ahora_utc - timedelta(days=3)

    omisiones_48h = 0
    omisiones_3d = 0
    critico_omitido_nombre: str | None = None
    ultima_fecha_omision_local: date | None = None

    for rec, med in recs_meds:
        if rec.estado == "omitido":
            if rec.hora_programada >= hace_48h:
                omisiones_48h += 1
                if med.es_critico and critico_omitido_nombre is None:
                    critico_omitido_nombre = med.nombre
            if rec.hora_programada >= hace_3d:
                omisiones_3d += 1
            f_loc = (rec.hora_programada + delta_tz).date()
            if ultima_fecha_omision_local is None or f_loc > ultima_fecha_omision_local:
                ultima_fecha_omision_local = f_loc

    # También revisar eventos recientes de omisión en historial_toma (por si hora_programada era anterior pero se omitió hoy)
    for h, rec, med in hist_meds:
        if h.estado_final == "omitido":
            ts = h.fecha_accion or rec.hora_programada
            if ts >= hace_48h:
                omisiones_48h = max(omisiones_48h, 1)
                if med.es_critico and critico_omitido_nombre is None:
                    critico_omitido_nombre = med.nombre
            if ts >= hace_3d:
                omisiones_3d = max(omisiones_3d, 1)
            f_loc = (ts + delta_tz).date()
            if ultima_fecha_omision_local is None or f_loc > ultima_fecha_omision_local:
                ultima_fecha_omision_local = f_loc

    if omisiones_3d > 0:
        dias_limpios_recuperacion = min(3, racha_dias)
    else:
        dias_limpios_recuperacion = 3

    bajo_honor = rango_honor in ("Hierro", "Bronce")
    posponer_bloqueado = bool(
        omisiones_3d > 0 and dias_limpios_recuperacion < 3 and bajo_honor
    )
    emblema_agrietado = bool(omisiones_48h > 0 or (bajo_honor and omisiones_3d > 0))
    requiere_alerta_cuidador = bool(
        critico_omitido_nombre is not None or posponer_bloqueado or omisiones_48h >= 2
    )

    return (
        racha_dias,
        color_fuego,
        escudos_racha,
        xp_honor,
        xp_siguiente,
        rango_honor,
        emblema_agrietado,
        posponer_bloqueado,
        dias_limpios_recuperacion,
        requiere_alerta_cuidador,
        critico_omitido_nombre,
    )


def esta_posponer_bloqueado(
    db: Session,
    id_usuario: int,
    tz_offset_minutes: int = 0,
    ahora: datetime | None = None,
) -> bool:
    """Devuelve True si el usuario tiene bloqueado el botón 'Posponer 30 min' por Modo Castigo."""
    if ahora is None:
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)

    recs_meds = (
        db.execute(
            select(Recordatorio, Medicamento)
            .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
            .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
            .where(Medicamento.id_usuario == id_usuario)
        )
        .tuples()
        .all()
    )
    hist_meds = (
        db.execute(
            select(HistorialToma, Recordatorio, Medicamento)
            .join(Recordatorio, Recordatorio.id_recordatorio == HistorialToma.id_recordatorio)
            .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
            .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
            .where(Medicamento.id_usuario == id_usuario)
        )
        .tuples()
        .all()
    )
    (
        _racha,
        _fuego,
        _escudos,
        _xp,
        _xp_sig,
        _rango,
        _agrietado,
        posponer_bloqueado,
        _dias_rec,
        _alerta,
        _crit_med,
    ) = _calcular_racha_y_castigo(
        list(recs_meds), list(hist_meds), ahora, tz_offset_minutes
    )
    return posponer_bloqueado


def calcular_estadisticas_usuario(
    db: Session,
    user: Usuario,
    tz_offset_minutes: int = 0,
    ahora: datetime | None = None,
) -> EstadisticasOut:
    """Calcula todas las métricas de gamificación (racha, fuego evolutivo, escudos,
    XP y Rango de Honor), estado de castigo, alerta al cuidador, adherencia semanal,
    adherencia por medicamento y mapa de calor de omisiones."""
    if ahora is None:
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)

    asegurar_horizonte_recordatorios(db, user.id_usuario, ahora=ahora)

    recs_meds = list(
        db.execute(
            select(Recordatorio, Medicamento)
            .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
            .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
            .where(Medicamento.id_usuario == user.id_usuario)
            .order_by(Recordatorio.hora_programada)
        )
        .tuples()
        .all()
    )

    hist_meds = list(
        db.execute(
            select(HistorialToma, Recordatorio, Medicamento)
            .join(Recordatorio, Recordatorio.id_recordatorio == HistorialToma.id_recordatorio)
            .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
            .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
            .where(Medicamento.id_usuario == user.id_usuario)
            .order_by(HistorialToma.fecha_accion)
        )
        .tuples()
        .all()
    )

    (
        racha_dias,
        color_fuego,
        escudos_racha,
        xp_honor,
        xp_siguiente_rango,
        rango_honor,
        emblema_agrietado,
        posponer_bloqueado,
        dias_limpios_recuperacion,
        requiere_alerta_cuidador,
        critico_omitido_nombre,
    ) = _calcular_racha_y_castigo(recs_meds, hist_meds, ahora, tz_offset_minutes)

    # Contacto de apoyo principal para alerta al cuidador
    contacto_principal = db.scalars(
        select(ContactoApoyo)
        .where(ContactoApoyo.id_usuario == user.id_usuario)
        .order_by(ContactoApoyo.es_principal.desc(), ContactoApoyo.id_contacto.asc())
    ).first()

    nombre_cuidador = (
        contacto_principal.nombre_completo if contacto_principal else "tu contacto de apoyo"
    )
    telefono_cuidador = contacto_principal.telefono if contacto_principal else None

    mensaje_alerta_cuidador: str | None = None
    if requiere_alerta_cuidador:
        if critico_omitido_nombre:
            mensaje_alerta_cuidador = (
                f"Alerta para {nombre_cuidador}: {user.nombre_completo} omitió una dosis "
                f"crítica de {critico_omitido_nombre}. Se recomienda verificar su estado de inmediato."
            )
        else:
            mensaje_alerta_cuidador = (
                f"Aviso para {nombre_cuidador}: {user.nombre_completo} entró en Modo Castigo "
                f"(Rango {rango_honor}) tras omitir dosis recientes. Requiere 3 días limpios para recuperar su racha."
            )

    # Adherencia semanal (últimos 7 días locales incluyendo hoy)
    delta_tz = timedelta(minutes=tz_offset_minutes)
    hoy_local: date = (ahora + delta_tz).date()

    por_fecha_local: dict[date, list[Recordatorio]] = {}
    for rec, _med in recs_meds:
        f_local = (rec.hora_programada + delta_tz).date()
        por_fecha_local.setdefault(f_local, []).append(rec)

    adherencia_semanal: list[AdherenciaDiaOut] = []
    for offset in range(6, -1, -1):
        d = hoy_local - timedelta(days=offset)
        items = por_fecha_local.get(d, [])
        tomadas = sum(1 for r in items if r.estado == "tomado")
        omitidas = sum(1 for r in items if r.estado == "omitido")
        pospuestas = sum(1 for r in items if r.veces_pospuesto > 0 or r.estado == "pospuesto")
        programadas = len(items)
        porcentaje = round((tomadas / programadas) * 100.0, 1) if programadas > 0 else 0.0
        adherencia_semanal.append(
            AdherenciaDiaOut(
                dia=DIAS_SEMANA_ESP[d.weekday()],
                fecha=d.isoformat(),
                tomadas=tomadas,
                programadas=programadas,
                omitidas=omitidas,
                pospuestas=pospuestas,
                porcentaje=porcentaje,
            )
        )

    # Adherencia por medicamento
    todos_meds = db.scalars(
        select(Medicamento)
        .where(Medicamento.id_usuario == user.id_usuario)
        .order_by(Medicamento.id_medicamento)
    ).all()

    recs_por_med: dict[int, list[Recordatorio]] = {}
    for rec, med in recs_meds:
        recs_por_med.setdefault(med.id_medicamento, []).append(rec)

    adherencia_por_medicamento: list[AdherenciaMedicamentoOut] = []
    for med in todos_meds:
        lista_r = recs_por_med.get(med.id_medicamento, [])
        evaluables = [
            r
            for r in lista_r
            if r.estado in ("tomado", "omitido") or r.hora_programada <= ahora
        ]
        tom_med = sum(1 for r in evaluables if r.estado == "tomado")
        tot_med = len(evaluables)
        pct_med = round((tom_med / tot_med) * 100.0, 1) if tot_med > 0 else 100.0
        adherencia_por_medicamento.append(
            AdherenciaMedicamentoOut(
                id_medicamento=med.id_medicamento,
                nombre=med.nombre,
                tomadas=tom_med,
                total=tot_med,
                porcentaje=pct_med,
            )
        )

    # Mapa de calor: 4 franjas horarias x 7 días de la semana (Lun..Dom)
    matriz_omisiones = [[0 for _ in range(7)] for _ in range(4)]
    matriz_tomadas = [[0 for _ in range(7)] for _ in range(4)]
    matriz_totales = [[0 for _ in range(7)] for _ in range(4)]

    for rec, _med in recs_meds:
        dt_local = rec.hora_programada + delta_tz
        idx_franja = _indice_franja_horaria(dt_local.hour)
        idx_dia = dt_local.weekday()  # 0=Lun .. 6=Dom

        if rec.estado in ("tomado", "omitido") or rec.hora_programada <= ahora:
            matriz_totales[idx_franja][idx_dia] += 1
        if rec.estado == "tomado":
            matriz_tomadas[idx_franja][idx_dia] += 1
        elif rec.estado == "omitido":
            matriz_omisiones[idx_franja][idx_dia] += 1

    mapa_calor: list[BloqueMapaCalorOut] = []
    peor_franja = ""
    peor_dia = ""
    max_celda_omisiones = 0
    peor_franja_total = ""
    max_franja_omisiones = 0

    for f_idx, nombre_franja in enumerate(FRANJAS_MAPA_CALOR):
        dias_out: list[DiaMapaCalorOut] = []
        valores_fila: list[int] = []
        suma_fila = 0
        for d_idx, nombre_dia in enumerate(DIAS_SEMANA_ESP):
            om = matriz_omisiones[f_idx][d_idx]
            tm = matriz_tomadas[f_idx][d_idx]
            tt = matriz_totales[f_idx][d_idx]
            dias_out.append(
                DiaMapaCalorOut(
                    dia=nombre_dia,
                    omisiones=om,
                    tomadas=tm,
                    total=tt,
                )
            )
            valores_fila.append(om)
            suma_fila += om
            if om > max_celda_omisiones:
                max_celda_omisiones = om
                peor_franja = nombre_franja
                peor_dia = nombre_dia

        if suma_fila > max_franja_omisiones:
            max_franja_omisiones = suma_fila
            peor_franja_total = nombre_franja

        mapa_calor.append(
            BloqueMapaCalorOut(
                franja=nombre_franja,
                dias=dias_out,
                valores=valores_fila,
                total_omisiones=suma_fila,
            )
        )

    if max_franja_omisiones == 0:
        insight_debilidad = (
            "¡Excelente disciplina! No registras omisiones en ninguna franja horaria."
        )
    else:
        insight_debilidad = (
            f"Mayor vulnerabilidad detectada en '{peor_franja_total}' "
            f"(pico los {peor_dia} con {max_celda_omisiones} omisión(es)). "
            f"Sugerencia: vincula esta toma a un hábito fijo diario."
        )

    total_tomadas = sum(1 for r, _ in recs_meds if r.estado == "tomado")
    total_omitidas = sum(1 for r, _ in recs_meds if r.estado == "omitido")
    total_pospuestas = sum(1 for r, _ in recs_meds if r.veces_pospuesto > 0)
    total_resueltas = total_tomadas + total_omitidas
    porcentaje_global = (
        round((total_tomadas / total_resueltas) * 100.0, 1)
        if total_resueltas > 0
        else 100.0
    )

    return EstadisticasOut(
        racha_dias=racha_dias,
        color_fuego=color_fuego,
        escudos_racha=escudos_racha,
        xp_honor=xp_honor,
        xp_siguiente_rango=xp_siguiente_rango,
        rango_honor=rango_honor,
        emblema_agrietado=emblema_agrietado,
        posponer_bloqueado=posponer_bloqueado,
        dias_limpios_recuperacion=dias_limpios_recuperacion,
        requiere_alerta_cuidador=requiere_alerta_cuidador,
        mensaje_alerta_cuidador=mensaje_alerta_cuidador,
        contacto_principal_nombre=contacto_principal.nombre_completo
        if contacto_principal
        else None,
        contacto_principal_telefono=telefono_cuidador,
        porcentaje_global=porcentaje_global,
        total_tomadas=total_tomadas,
        total_omitidas=total_omitidas,
        total_pospuestas=total_pospuestas,
        adherencia_semanal=adherencia_semanal,
        adherencia_por_medicamento=adherencia_por_medicamento,
        mapa_calor=mapa_calor,
        insight_debilidad=insight_debilidad,
    )
