from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.tratamiento import TratamientoCreate, TratamientoOut

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
