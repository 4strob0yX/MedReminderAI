from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.schemas.medicamento import (
    MedicamentoCatalogoItem,
    MedicamentoCreate,
    MedicamentoOut,
    VerificarAlergiasIn,
    VerificarAlergiasOut,
)
from app.services.catalogo_service import (
    buscar_en_catalogo,
    verificar_alergias_paciente,
)

router = APIRouter(prefix="/medicamentos", tags=["medicamentos"])


@router.get("/catalogo", response_model=list[MedicamentoCatalogoItem])
def catalogo_medicamentos(
    q: str | None = Query(default=None, description="Término de búsqueda para autocompletado"),
):
    """Devuelve sugerencias clínicas de medicamentos para autocompletado."""
    return buscar_en_catalogo(q)


@router.post("/verificar-alergias", response_model=VerificarAlergiasOut)
def verificar_alergias_endpoint(
    data: VerificarAlergiasIn,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Evalúa si el medicamento ingresado o seleccionado choca con alergias registradas del paciente."""
    return verificar_alergias_paciente(
        db=db,
        id_usuario=user.id_usuario,
        nombre=data.nombre,
        principio_activo=data.principio_activo,
    )


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
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    return med
