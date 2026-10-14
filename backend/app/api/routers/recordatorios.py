from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.recordatorio import HistorialToma, Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.recordatorio import RecordatorioOut

router = APIRouter(prefix="/recordatorios", tags=["recordatorios"])

POSPONER_MINUTOS = 30  # decision del Tech Lead: valor fijo
MAX_POSPOSICIONES = 3  # al llegar el contador a 3 se omite automaticamente


def _recordatorio_propio(
    db: Session, user: Usuario, id_recordatorio: int
) -> tuple[Recordatorio, Medicamento]:
    """Carga el recordatorio y su medicamento SOLO si pertenece al usuario del token
    y lo bloquea con FOR UPDATE.
    404 si no existe o es ajeno; 409 si ya fue resuelto."""
    stmt = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(
            Recordatorio.id_recordatorio == id_recordatorio,
            Medicamento.id_usuario == user.id_usuario,
        )
        .with_for_update(of=Recordatorio)
    )
    row = db.execute(stmt).first()
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Recordatorio no encontrado")
    rec, med = row[0], row[1]
    if rec.estado != "pendiente":
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail=f"El recordatorio ya esta '{rec.estado}'"
        )
    return rec, med


def _construir_out(rec: Recordatorio, med: Medicamento) -> RecordatorioOut:
    return RecordatorioOut(
        id_recordatorio=rec.id_recordatorio,
        id_tratamiento=rec.id_tratamiento,
        hora_programada=rec.hora_programada,
        estado=rec.estado,
        veces_pospuesto=rec.veces_pospuesto,
        permite_posponer=bool(med.permite_posponer and not med.es_critico),
        es_critico=bool(med.es_critico or not med.permite_posponer),
        nombre_medicamento=med.nombre,
        dosis=med.dosis,
    )


def _log(db: Session, rec: Recordatorio, estado: str, notas: str | None = None) -> None:
    db.add(HistorialToma(id_recordatorio=rec.id_recordatorio, estado_final=estado, notas=notas))


@router.get("", response_model=list[RecordatorioOut])
@router.get("/", response_model=list[RecordatorioOut], include_in_schema=False)
def listar_recordatorios(
    fecha: date | None = Query(
        default=None, description="YYYY-MM-DD evaluado en UTC: ventana de 24 h de ese dia"
    ),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(Medicamento.id_usuario == user.id_usuario)
    )
    if fecha is not None:
        inicio = datetime.combine(fecha, time.min)  # 00:00 UTC (naive, convencion de la BD)
        stmt = stmt.where(
            Recordatorio.hora_programada >= inicio,
            Recordatorio.hora_programada < inicio + timedelta(days=1),
        )
    stmt = stmt.order_by(Recordatorio.hora_programada, Recordatorio.id_recordatorio)
    rows = db.execute(stmt).all()
    return [_construir_out(rec, med) for rec, med in rows]


@router.post("/{id_recordatorio}/tomar", response_model=RecordatorioOut)
def tomar(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rec, med = _recordatorio_propio(db, user, id_recordatorio)
    rec.estado = "tomado"
    _log(db, rec, "tomado")
    db.commit()
    db.refresh(rec)
    return _construir_out(rec, med)


@router.post("/{id_recordatorio}/omitir", response_model=RecordatorioOut)
def omitir(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rec, med = _recordatorio_propio(db, user, id_recordatorio)
    rec.estado = "omitido"
    _log(db, rec, "omitido")
    db.commit()
    db.refresh(rec)
    return _construir_out(rec, med)


@router.post("/{id_recordatorio}/posponer", response_model=RecordatorioOut)
def posponer(
    id_recordatorio: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rec, med = _recordatorio_propio(db, user, id_recordatorio)

    # Validar si el medicamento es crítico o tiene prohibido posponerse
    if not med.permite_posponer or med.es_critico:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El medicamento '{med.nombre}' es de dosis crítica y NO puede posponerse. Debe tomarse de inmediato o registrarse como omitido.",
        )

    rec.veces_pospuesto += 1
    _log(db, rec, "pospuesto")

    if rec.veces_pospuesto >= MAX_POSPOSICIONES:
        # Tercera peticion: no se reprograma, el backend lo omite (timeout automatico).
        rec.estado = "omitido"
        _log(db, rec, "omitido", "Omitido automaticamente: limite de pospuestos alcanzado")
    else:
        rec.hora_programada = rec.hora_programada + timedelta(minutes=POSPONER_MINUTOS)
        rec.estado = "pendiente"

    db.commit()
    db.refresh(rec)
    return _construir_out(rec, med)
