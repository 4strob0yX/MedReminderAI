from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.mongo import registrar_evento_mongo
from app.db.session import get_db
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.schemas.medicamento import (
    MedicamentoCatalogoItem,
    MedicamentoCreate,
    MedicamentoOut,
    MedicamentoStockUpdate,
    MedicamentoUpdate,
    VerificarAlergiasIn,
    VerificarAlergiasOut,
)
from app.services.catalogo_service import (
    buscar_en_catalogo,
    verificar_alergias_paciente,
)

router = APIRouter(prefix="/medicamentos", tags=["medicamentos"])


def _obtener_med_propio(db: Session, user_id: int, id_medicamento: int) -> Medicamento:
    stmt = select(Medicamento).where(
        Medicamento.id_medicamento == id_medicamento,
        Medicamento.id_usuario == user_id,
    )
    med = db.scalars(stmt).first()
    if med is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    return med


@router.get("/catalogo", response_model=list[MedicamentoCatalogoItem])
def catalogo_medicamentos(
    q: str | None = Query(default=None, description="Término de búsqueda para autocompletado"),
):
    """Devuelve sugerencias clínicas de medicamentos para autocompletado."""
    return buscar_en_catalogo(q)


@router.post("/verificar-alergias", response_model=VerificarAlergiasOut)
@router.post("/verificar-interacciones", response_model=VerificarAlergiasOut)
def verificar_alergias_endpoint(
    data: VerificarAlergiasIn,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Evalúa si el medicamento ingresado o seleccionado choca con alergias registradas
    del paciente o presenta interacciones con otros medicamentos de su botiquín."""
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
    registrar_evento_mongo(
        evento="medicamento_creado",
        id_usuario=user.id_usuario,
        detalle={
            "id_medicamento": med.id_medicamento,
            "nombre": med.nombre,
            "dosis": med.dosis,
            "forma_farmaceutica": med.forma_farmaceutica,
            "color_pastilla": med.color_pastilla,
            "es_critico": med.es_critico,
        },
    )
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
    return _obtener_med_propio(db, user.id_usuario, id_medicamento)


@router.put("/{id_medicamento}", response_model=MedicamentoOut)
def actualizar_medicamento(
    id_medicamento: int,
    data: MedicamentoUpdate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    med = _obtener_med_propio(db, user.id_usuario, id_medicamento)
    cambios = data.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        if valor is not None or campo in ("principio_activo", "contraindicaciones", "instrucciones_toma", "proposito"):
            setattr(med, campo, valor)

    if med.cantidad_stock > med.stock_inicial:
        med.stock_inicial = med.cantidad_stock

    db.commit()
    db.refresh(med)
    return med


@router.patch("/{id_medicamento}/stock", response_model=MedicamentoOut)
@router.post("/{id_medicamento}/reabastecer", response_model=MedicamentoOut)
def reabastecer_stock_medicamento(
    id_medicamento: int,
    data: MedicamentoStockUpdate | None = Body(default=None),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Reabastece la caja del medicamento, actualizando `cantidad_stock` y `stock_inicial`."""
    med = _obtener_med_propio(db, user.id_usuario, id_medicamento)

    if data is None:
        # Si no se envía body, rellena a la capacidad de referencia de la caja (mínimo 30)
        nueva_caja = max(med.stock_inicial, 30)
        med.cantidad_stock = nueva_caja
        med.stock_inicial = nueva_caja
    elif data.cantidad_agregar is not None:
        med.cantidad_stock += data.cantidad_agregar
        med.stock_inicial = max(med.stock_inicial, med.cantidad_stock)
    else:
        nuevo_stock = (
            data.cantidad_stock
            if data.cantidad_stock is not None
            else data.stock_actual
        )
        if nuevo_stock is not None:
            med.cantidad_stock = nuevo_stock
            med.stock_inicial = (
                data.stock_inicial
                if data.stock_inicial is not None
                else max(med.stock_inicial, nuevo_stock, 1)
            )
        elif data.stock_inicial is not None:
            med.stock_inicial = max(data.stock_inicial, 1)
            med.cantidad_stock = data.stock_inicial
        else:
            nueva_caja = max(med.stock_inicial, 30)
            med.cantidad_stock = nueva_caja
            med.stock_inicial = nueva_caja

    db.commit()
    db.refresh(med)
    return med


@router.delete("/{id_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_medicamento(
    id_medicamento: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    med = _obtener_med_propio(db, user.id_usuario, id_medicamento)
    db.delete(med)
    db.commit()
    return None
