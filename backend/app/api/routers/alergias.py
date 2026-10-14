from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.alergia import AlergiaUsuario
from app.models.usuario import Usuario
from app.schemas.alergia import AlergiaCreate, AlergiaOut

router = APIRouter(prefix="/alergias", tags=["alergias"])


@router.get("", response_model=list[AlergiaOut])
def listar_alergias(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtiene todas las alergias registradas para el paciente actual."""
    stmt = (
        select(AlergiaUsuario)
        .where(AlergiaUsuario.id_usuario == user.id_usuario)
        .order_by(AlergiaUsuario.id_alergia.desc())
    )
    return db.scalars(stmt).all()


@router.post("", response_model=AlergiaOut, status_code=status.HTTP_201_CREATED)
def agregar_alergia(
    data: AlergiaCreate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Registra una nueva alergia médica (ej. Penicilinas, AINEs, Sulfas)."""
    # Evitar duplicados para el mismo paciente y sustancia
    existente = db.scalars(
        select(AlergiaUsuario).where(
            AlergiaUsuario.id_usuario == user.id_usuario,
            AlergiaUsuario.sustancia.ilike(data.sustancia),
        )
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La alergia a '{data.sustancia}' ya está registrada.",
        )

    nueva = AlergiaUsuario(id_usuario=user.id_usuario, **data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.delete("/{id_alergia}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alergia(
    id_alergia: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Elimina una alergia del historial del paciente."""
    alergia = db.scalars(
        select(AlergiaUsuario).where(
            AlergiaUsuario.id_alergia == id_alergia,
            AlergiaUsuario.id_usuario == user.id_usuario,
        )
    ).first()
    if alergia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alergia no encontrada")

    db.delete(alergia)
    db.commit()
    return None
