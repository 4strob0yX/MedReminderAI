from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.contacto import ContactoApoyo
from app.models.usuario import Usuario
from app.schemas.contacto import ContactoCreate, ContactoOut

router = APIRouter(prefix="/contactos-apoyo", tags=["contactos-apoyo"])


@router.get("", response_model=list[ContactoOut])
def listar_contactos(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtiene los contactos de apoyo o emergencia del paciente."""
    stmt = (
        select(ContactoApoyo)
        .where(ContactoApoyo.id_usuario == user.id_usuario)
        .order_by(ContactoApoyo.es_principal.desc(), ContactoApoyo.id_contacto.asc())
    )
    return db.scalars(stmt).all()


@router.post("", response_model=ContactoOut, status_code=status.HTTP_201_CREATED)
def agregar_contacto(
    data: ContactoCreate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Registra un nuevo cuidador o contacto de apoyo."""
    # Si este nuevo contacto es principal, desmarcar los anteriores como principal
    if data.es_principal:
        anteriores = db.scalars(
            select(ContactoApoyo).where(
                ContactoApoyo.id_usuario == user.id_usuario, ContactoApoyo.es_principal == True
            )
        ).all()
        for c in anteriores:
            c.es_principal = False

    nuevo = ContactoApoyo(id_usuario=user.id_usuario, **data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id_contacto}", response_model=ContactoOut)
def actualizar_contacto(
    id_contacto: int,
    data: ContactoCreate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Actualiza la información de un contacto de apoyo existente."""
    contacto = db.scalars(
        select(ContactoApoyo).where(
            ContactoApoyo.id_contacto == id_contacto,
            ContactoApoyo.id_usuario == user.id_usuario,
        )
    ).first()
    if contacto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")

    if data.es_principal and not contacto.es_principal:
        anteriores = db.scalars(
            select(ContactoApoyo).where(
                ContactoApoyo.id_usuario == user.id_usuario, ContactoApoyo.es_principal == True
            )
        ).all()
        for c in anteriores:
            c.es_principal = False

    contacto.nombre_completo = data.nombre_completo
    contacto.telefono = data.telefono
    contacto.parentesco = data.parentesco
    contacto.correo = data.correo
    contacto.es_principal = data.es_principal

    db.commit()
    db.refresh(contacto)
    return contacto


@router.delete("/{id_contacto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contacto(
    id_contacto: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Elimina un contacto de apoyo."""
    contacto = db.scalars(
        select(ContactoApoyo).where(
            ContactoApoyo.id_contacto == id_contacto,
            ContactoApoyo.id_usuario == user.id_usuario,
        )
    ).first()
    if contacto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado")

    db.delete(contacto)
    db.commit()
    return None
