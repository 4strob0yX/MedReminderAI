from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.schemas.medicamento import MedicamentoCreate, MedicamentoOut

router = APIRouter(prefix="/medicamentos", tags=["medicamentos"])


@router.post("", response_model=MedicamentoOut, status_code=status.HTTP_201_CREATED)
def crear_medicamento(
    data: MedicamentoCreate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # El dueno SIEMPRE viene del token, nunca del body.
    med = Medicamento(id_usuario=user.id_usuario, **data.model_dump())
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.get("", response_model=list[MedicamentoOut])
def listar_medicamentos(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Medicamento)
        .where(Medicamento.id_usuario == user.id_usuario)
        .order_by(Medicamento.id_medicamento)
    )
    return db.scalars(stmt).all()


@router.get("/{id_medicamento}", response_model=MedicamentoOut)
def obtener_medicamento(
    id_medicamento: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Medicamento).where(
        Medicamento.id_medicamento == id_medicamento,
        Medicamento.id_usuario == user.id_usuario,
    )
    med = db.scalars(stmt).first()
    if med is None:
        # 404 (no 403) para no revelar si el recurso existe para otro paciente.
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    return med
