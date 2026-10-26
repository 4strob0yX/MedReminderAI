from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.mongo import registrar_evento_mongo
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.recordatorio import HistorialToma, Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.auth import UsuarioOut
from app.schemas.recordatorio import EstadisticasOut, RecordatorioOut
from app.api.routers.cuidador import registrar_alerta_cuidador_db
from app.services.recordatorio_service import (
    asegurar_horizonte_recordatorios,
    calcular_estadisticas_usuario,
    esta_posponer_bloqueado,
)

router = APIRouter(prefix="/recordatorios", tags=["recordatorios"])

POSPONER_MINUTOS = 30  # decision del Tech Lead: valor fijo
MAX_POSPOSICIONES = 3  # al llegar el contador a 3 se omite automaticamente


def _cargar_recordatorio_y_med(
    db: Session, user: Usuario, id_recordatorio: int
) -> tuple[Recordatorio, Medicamento]:
    """Carga el recordatorio y su medicamento SOLO si pertenece al usuario del token
    y lo bloquea con FOR UPDATE."""
    stmt = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(
            Recordatorio.id_recordatorio == id_recordatorio,
            Medicamento.id_usuario == user.id_usuario,
        )
        .with_for_update(of=(Recordatorio, Medicamento))
    )
    row = db.execute(stmt).first()
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Recordatorio no encontrado")
    return row[0], row[1]


def _recordatorio_propio(
    db: Session, user: Usuario, id_recordatorio: int
) -> tuple[Recordatorio, Medicamento]:
    """404 si no existe o es ajeno; 409 si ya fue resuelto."""
    rec, med = _cargar_recordatorio_y_med(db, user, id_recordatorio)
    if rec.estado != "pendiente":
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail=f"El recordatorio ya esta '{rec.estado}'"
        )
    return rec, med


def _construir_out(
    rec: Recordatorio, med: Medicamento, castigo_bloquea_posponer: bool = False
) -> RecordatorioOut:
    permite_med = bool(med.permite_posponer and not med.es_critico)
    return RecordatorioOut(
        id_recordatorio=rec.id_recordatorio,
        id_tratamiento=rec.id_tratamiento,
        id_medicamento=med.id_medicamento,
        hora_programada=rec.hora_programada,
        estado=rec.estado,
        veces_pospuesto=rec.veces_pospuesto,
        permite_posponer=bool(permite_med and not castigo_bloquea_posponer),
        posponer_bloqueado_por_castigo=castigo_bloquea_posponer,
        es_critico=bool(med.es_critico or not med.permite_posponer),
        nombre_medicamento=med.nombre,
        dosis=med.dosis,
        forma_farmaceutica=med.forma_farmaceutica or "comprimidos",
        color_pastilla=med.color_pastilla or "blanco",
        instrucciones_toma=med.instrucciones_toma,
        proposito=med.proposito,
        cantidad_stock=med.cantidad_stock,
        stock_inicial=med.stock_inicial,
    )


def _log(db: Session, rec: Recordatorio, estado: str, notas: str | None = None) -> None:
    db.add(HistorialToma(id_recordatorio=rec.id_recordatorio, estado_final=estado, notas=notas))


@router.get("/estadisticas", response_model=EstadisticasOut)
def obtener_estadisticas(
    tz_offset_minutes: int = Query(
        default=0,
        description="Desfase horario local respecto a UTC en minutos (ej. -360 para UTC-6)",
    ),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Devuelve estadísticas reales de adherencia, racha con fuego evolutivo,
    escudos, XP/Rango de Honor, modo castigo, alerta al cuidador y mapa de calor."""
    return calcular_estadisticas_usuario(
        db=db, user=user, tz_offset_minutes=tz_offset_minutes
    )


@router.get("", response_model=list[RecordatorioOut])
@router.get("/", response_model=list[RecordatorioOut], include_in_schema=False)
def listar_recordatorios(
    fecha: date | None = Query(
        default=None,
        description="YYYY-MM-DD: ventana de 24 h de ese día (ajustada con tz_offset_minutes)",
    ),
    tz_offset_minutes: int = Query(
        default=0,
        description="Desfase horario local respecto a UTC en minutos (ej. -360 para UTC-6)",
    ),
    desde_utc: datetime | None = Query(default=None),
    hasta_utc: datetime | None = Query(default=None),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    asegurar_horizonte_recordatorios(db, user.id_usuario)
    bloqueado_castigo = esta_posponer_bloqueado(
        db, user.id_usuario, tz_offset_minutes=tz_offset_minutes
    )

    stmt = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(Medicamento.id_usuario == user.id_usuario)
    )
    if desde_utc is not None:
        stmt = stmt.where(Recordatorio.hora_programada >= desde_utc)
    if hasta_utc is not None:
        stmt = stmt.where(Recordatorio.hora_programada < hasta_utc)
    elif fecha is not None and desde_utc is None:
        # Convertir las 00:00 locales del día solicitado a UTC restando tz_offset_minutes
        inicio_utc = datetime.combine(fecha, time.min) - timedelta(
            minutes=tz_offset_minutes
        )
        stmt = stmt.where(
            Recordatorio.hora_programada >= inicio_utc,
            Recordatorio.hora_programada < inicio_utc + timedelta(days=1),
        )
    stmt = stmt.order_by(Recordatorio.hora_programada, Recordatorio.id_recordatorio)
    rows = db.execute(stmt).all()
    return [
        _construir_out(rec, med, castigo_bloquea_posponer=bloqueado_castigo)
        for rec, med in rows
    ]


@router.post("/{id_recordatorio}/tomar", response_model=RecordatorioOut)
def tomar(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rec, med = _recordatorio_propio(db, user, id_recordatorio)
    rec.estado = "tomado"
    if med.cantidad_stock > 0:
        med.cantidad_stock -= 1
    _log(db, rec, "tomado")
    db.commit()
    db.refresh(rec)
    registrar_evento_mongo(
        evento="toma_confirmada",
        id_usuario=user.id_usuario,
        detalle={
            "id_recordatorio": rec.id_recordatorio,
            "medicamento": med.nombre,
            "stock_restante": med.cantidad_stock,
        },
    )
    bloqueado_castigo = esta_posponer_bloqueado(db, user.id_usuario)
    return _construir_out(rec, med, castigo_bloquea_posponer=bloqueado_castigo)


@router.post("/{id_recordatorio}/omitir", response_model=RecordatorioOut)
def omitir(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rec, med = _recordatorio_propio(db, user, id_recordatorio)

    if med.es_critico:
        registrar_alerta_cuidador_db(
            db=db,
            user=user,
            tipo_alerta="critica_automatica",
            accion_origen="omitir",
            nombre_medicamento=med.nombre,
            dosis=med.dosis,
            es_critico=True,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"🚨 Alerta enviada automáticamente a tu cuidador: El medicamento '{med.nombre}' es crítico y no debe omitirse.",
        )

    rec.estado = "omitido"
    _log(db, rec, "omitido")
    db.commit()
    db.refresh(rec)
    if UsuarioOut.model_validate(user).es_adulto_mayor:
        registrar_alerta_cuidador_db(
            db=db,
            user=user,
            tipo_alerta="advertencia_normal",
            accion_origen="omitir",
            nombre_medicamento=med.nombre,
            dosis=med.dosis,
            es_critico=False,
        )
    registrar_evento_mongo(
        evento="toma_omitida",
        id_usuario=user.id_usuario,
        detalle={
            "id_recordatorio": rec.id_recordatorio,
            "medicamento": med.nombre,
            "es_critico": med.es_critico,
            "motivo": "manual",
        },
    )
    bloqueado_castigo = esta_posponer_bloqueado(db, user.id_usuario)
    if bloqueado_castigo:
        registrar_evento_mongo(
            evento="castigo_activado",
            id_usuario=user.id_usuario,
            detalle={
                "id_recordatorio": rec.id_recordatorio,
                "medicamento": med.nombre,
                "motivo": "bajo_honor_omision",
            },
        )
    return _construir_out(rec, med, castigo_bloquea_posponer=bloqueado_castigo)


@router.post("/{id_recordatorio}/posponer", response_model=RecordatorioOut)
def posponer(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rec, med = _recordatorio_propio(db, user, id_recordatorio)

    # 1. Validar si el medicamento es crítico o tiene prohibido posponerse
    if not med.permite_posponer or med.es_critico:
        registrar_alerta_cuidador_db(
            db=db,
            user=user,
            tipo_alerta="critica_automatica",
            accion_origen="posponer",
            nombre_medicamento=med.nombre,
            dosis=med.dosis,
            es_critico=True,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"🚨 Alerta enviada automáticamente a tu cuidador: El medicamento '{med.nombre}' es crítico y NO puede posponerse.",
        )

    # 2. Validar si el usuario tiene bloqueado el botón Posponer por Modo Castigo (bajo Honor)
    if esta_posponer_bloqueado(db, user.id_usuario):
        registrar_evento_mongo(
            evento="castigo_activado",
            id_usuario=user.id_usuario,
            detalle={
                "id_recordatorio": rec.id_recordatorio,
                "medicamento": med.nombre,
                "accion_bloqueada": "posponer",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Modo Castigo activo por bajo Honor: el botón 'Posponer 30 min' está bloqueado hasta cumplir 3 días seguidos sin omisiones.",
        )

    rec.veces_pospuesto += 1

    if rec.veces_pospuesto >= MAX_POSPOSICIONES:
        # Tercera petición: no se reprograma y se registra SOLO 'omitido' (sin doble log)
        rec.estado = "omitido"
        _log(db, rec, "omitido", "Omitido automaticamente: limite de pospuestos alcanzado")
        evento_mongo = "toma_omitida"
    else:
        rec.hora_programada = rec.hora_programada + timedelta(minutes=POSPONER_MINUTOS)
        rec.estado = "pendiente"
        _log(db, rec, "pospuesto")
        evento_mongo = "toma_pospuesta"

    db.commit()
    db.refresh(rec)
    if UsuarioOut.model_validate(user).es_adulto_mayor:
        registrar_alerta_cuidador_db(
            db=db,
            user=user,
            tipo_alerta="advertencia_normal",
            accion_origen="posponer",
            nombre_medicamento=med.nombre,
            dosis=med.dosis,
            es_critico=False,
        )
    registrar_evento_mongo(
        evento=evento_mongo,
        id_usuario=user.id_usuario,
        detalle={
            "id_recordatorio": rec.id_recordatorio,
            "medicamento": med.nombre,
            "veces_pospuesto": rec.veces_pospuesto,
        },
    )
    bloqueado_castigo = esta_posponer_bloqueado(db, user.id_usuario)
    return _construir_out(rec, med, castigo_bloquea_posponer=bloqueado_castigo)


@router.post("/{id_recordatorio}/revertir", response_model=RecordatorioOut)
def revertir(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revierte (Undo) un recordatorio recientemente marcado como `tomado` u `omitido`
    de vuelta a `pendiente`, restaurando +1 de stock si había sido `tomado`."""
    rec, med = _cargar_recordatorio_y_med(db, user, id_recordatorio)
    if rec.estado == "pendiente":
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="El recordatorio ya se encuentra 'pendiente'"
        )
    if rec.estado not in ("tomado", "omitido"):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"No se puede revertir el estado '{rec.estado}'",
        )

    estado_anterior = rec.estado
    if estado_anterior == "tomado":
        med.cantidad_stock += 1
        if med.cantidad_stock > med.stock_inicial:
            med.stock_inicial = med.cantidad_stock
    elif estado_anterior == "omitido" and rec.veces_pospuesto >= MAX_POSPOSICIONES:
        rec.veces_pospuesto = max(0, MAX_POSPOSICIONES - 1)

    # Eliminar el último registro de historial_toma correspondiente para deshacer penalización/XP
    ultimo_hist = db.scalars(
        select(HistorialToma)
        .where(
            HistorialToma.id_recordatorio == rec.id_recordatorio,
            HistorialToma.estado_final == estado_anterior,
        )
        .order_by(HistorialToma.id_historial.desc())
    ).first()
    if ultimo_hist is not None:
        db.delete(ultimo_hist)

    rec.estado = "pendiente"
    db.commit()
    db.refresh(rec)
    bloqueado_castigo = esta_posponer_bloqueado(db, user.id_usuario)
    return _construir_out(rec, med, castigo_bloquea_posponer=bloqueado_castigo)
