from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.recordatorio import Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.tratamiento import TratamientoCreate, TratamientoOut, TratamientoUpdate
from app.services.recordatorio_service import generar_recordatorios

router = APIRouter(prefix="/tratamientos", tags=["tratamientos"])


def _tratamientos_del_usuario(user: Usuario):
    """SELECT base: tratamiento unido a medicamento, filtrado por el dueno del token.
    Toda lectura de tratamientos debe partir de aqui."""
    return (
        select(Tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(Medicamento.id_usuario == user.id_usuario)
    )


@router.post("", response_model=TratamientoOut, status_code=status.HTTP_201_CREATED)
def crear_tratamiento(
    data: TratamientoCreate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # El medicamento debe pertenecer al usuario del token; si no, 404.
    med = db.scalars(
        select(Medicamento).where(
            Medicamento.id_medicamento == data.id_medicamento,
            Medicamento.id_usuario == user.id_usuario,
        )
    ).first()
    if med is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")

    campos = data.model_dump(exclude_none=True)  # fecha_inicio omitida -> default de MySQL
    trat = Tratamiento(**campos)
    db.add(trat)
    # flush + refresh: obtiene id_tratamiento y la fecha_inicio real (default de MySQL)
    # sin cerrar la transaccion; tratamiento y recordatorios se confirman juntos o ninguno.
    db.flush()
    db.refresh(trat)
    db.add_all(generar_recordatorios(trat))
    db.commit()
    db.refresh(trat)
    return trat


@router.get("", response_model=list[TratamientoOut])
def listar_tratamientos(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = _tratamientos_del_usuario(user).order_by(Tratamiento.id_tratamiento)
    return db.scalars(stmt).all()


@router.get("/{id_tratamiento}", response_model=TratamientoOut)
def obtener_tratamiento(
    id_tratamiento: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = _tratamientos_del_usuario(user).where(Tratamiento.id_tratamiento == id_tratamiento)
    trat = db.scalars(stmt).first()
    if trat is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tratamiento no encontrado")
    return trat


@router.patch("/{id_tratamiento}", response_model=TratamientoOut)
@router.put("/{id_tratamiento}", response_model=TratamientoOut)
def actualizar_tratamiento(
    id_tratamiento: int,
    data: TratamientoUpdate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Permite pausar/reanudar un tratamiento o cambiar su frecuencia horaria."""
    stmt = _tratamientos_del_usuario(user).where(Tratamiento.id_tratamiento == id_tratamiento)
    trat = db.scalars(stmt).first()
    if trat is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tratamiento no encontrado")

    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    cambios = data.model_dump(exclude_unset=True)
    recalcular_agenda = False

    if "frecuencia_horas" in cambios and cambios["frecuencia_horas"] is not None:
        if cambios["frecuencia_horas"] != trat.frecuencia_horas:
            trat.frecuencia_horas = cambios["frecuencia_horas"]
            recalcular_agenda = True

    if "fecha_inicio" in cambios and cambios["fecha_inicio"] is not None:
        trat.fecha_inicio = cambios["fecha_inicio"]
        recalcular_agenda = True

    if "fecha_fin" in cambios:
        trat.fecha_fin = cambios["fecha_fin"]
        recalcular_agenda = True

    if "estado" in cambios and cambios["estado"] is not None:
        if cambios["estado"] != trat.estado:
            trat.estado = cambios["estado"]
            recalcular_agenda = True
            if trat.estado == "activo" and trat.fecha_inicio < ahora:
                trat.fecha_inicio = ahora.replace(microsecond=0)

    if recalcular_agenda:
        # Eliminar recordatorios pendientes futuros para regenerar con la nueva configuración
        db.execute(
            delete(Recordatorio).where(
                Recordatorio.id_tratamiento == trat.id_tratamiento,
                Recordatorio.estado == "pendiente",
                Recordatorio.hora_programada >= ahora.replace(microsecond=0) - (ahora - ahora),
            )
        )
        db.flush()
        if trat.estado == "activo":
            db.add_all(generar_recordatorios(trat, ahora=ahora))

    db.commit()
    db.refresh(trat)
    return trat


@router.delete("/{id_tratamiento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tratamiento(
    id_tratamiento: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = _tratamientos_del_usuario(user).where(Tratamiento.id_tratamiento == id_tratamiento)
    trat = db.scalars(stmt).first()
    if trat is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tratamiento no encontrado")

    db.delete(trat)
    db.commit()
    return None
