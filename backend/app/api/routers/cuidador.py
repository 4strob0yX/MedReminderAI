from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.alerta_cuidador import AlertaCuidador
from app.models.contacto import ContactoApoyo
from app.models.medicamento import Medicamento
from app.models.recordatorio import Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.auth import UsuarioOut
from app.schemas.cuidador import (
    AlertaCuidadorCreate,
    AlertaCuidadorOut,
    CuidadorPanelResponse,
    TomaSupervisadaItem,
)

router = APIRouter(prefix="/cuidador", tags=["cuidador"])


def registrar_alerta_cuidador_db(
    db: Session,
    user: Usuario,
    tipo_alerta: str,
    accion_origen: str,
    nombre_medicamento: str,
    dosis: str,
    es_critico: bool,
    mensaje_custom: str | None = None,
) -> AlertaCuidador:
    contacto = db.scalars(
        select(ContactoApoyo)
        .where(ContactoApoyo.id_usuario == user.id_usuario)
        .order_by(ContactoApoyo.es_principal.desc(), ContactoApoyo.id_contacto.asc())
    ).first()

    nombre_cuid = contacto.nombre_completo if contacto else "Familiar / Cuidador Principal"
    tel_cuid = contacto.telefono if contacto else "555-019-2834"
    paciente_nombre = user.nombre_completo.split(" ")[0] if user.nombre_completo else "Paciente"

    if mensaje_custom:
        msg = mensaje_custom
    elif es_critico or tipo_alerta == "critica_automatica":
        msg = (
            f"🚨 ALERTA CRÍTICA AUTOMÁTICA: {paciente_nombre} intentó {accion_origen} su medicamento "
            f"crítico '{nombre_medicamento} ({dosis})'. Se requiere intervención inmediata del cuidador ({nombre_cuid})."
        )
        tipo_alerta = "critica_automatica"
    else:
        msg = (
            f"⚠️ Aviso de Supervisión: {paciente_nombre} acaba de {accion_origen} '{nombre_medicamento} ({dosis})'. "
            f"Se notificó preventivamente al cuidador ({nombre_cuid})."
        )

    alerta = AlertaCuidador(
        id_usuario=user.id_usuario,
        tipo_alerta=tipo_alerta,
        accion_origen=accion_origen,
        nombre_medicamento=nombre_medicamento,
        dosis=dosis,
        es_critico=es_critico,
        mensaje=msg[:500],
        nombre_cuidador=nombre_cuid,
        telefono_cuidador=tel_cuid,
        atendida=False,
    )
    db.add(alerta)
    db.commit()
    db.refresh(alerta)
    return alerta


@router.get("/panel", response_model=CuidadorPanelResponse)
def obtener_panel_cuidador(
    tz_offset_minutes: int = Query(default=-360),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    u_out = UsuarioOut.model_validate(user)
    edad = u_out.edad
    es_mayor = u_out.es_adulto_mayor
    rango_label = (
        f"Adulto Mayor Supervisado ({edad} años)"
        if es_mayor
        else f"Joven / Adulto ({edad} años · Modo Racha y Honor)"
    )

    contacto = db.scalars(
        select(ContactoApoyo)
        .where(ContactoApoyo.id_usuario == user.id_usuario)
        .order_by(ContactoApoyo.es_principal.desc(), ContactoApoyo.id_contacto.asc())
    ).first()
    nombre_cuid = contacto.nombre_completo if contacto else "Laura Mendoza (Hija / Cuidadora)"
    tel_cuid = contacto.telefono if contacto else "+52 55 4829 1034"
    parentesco_cuid = contacto.parentesco if contacto else "Hija / Cuidadora Principal"

    hoy_local = (datetime.utcnow() + timedelta(minutes=tz_offset_minutes)).date()
    inicio_utc = datetime.combine(hoy_local, time.min) - timedelta(minutes=tz_offset_minutes)
    fin_utc = inicio_utc + timedelta(days=1)

    stmt = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(
            Medicamento.id_usuario == user.id_usuario,
            Recordatorio.hora_programada >= inicio_utc,
            Recordatorio.hora_programada < fin_utc,
        )
        .order_by(Recordatorio.hora_programada.asc())
    )
    rows = db.execute(stmt).all()

    tomas_hoy = [
        TomaSupervisadaItem(
            id_recordatorio=rec.id_recordatorio,
            nombre_medicamento=med.nombre,
            dosis=med.dosis,
            hora_programada=rec.hora_programada,
            estado=rec.estado,
            es_critico=bool(med.es_critico or not med.permite_posponer),
            veces_pospuesto=rec.veces_pospuesto,
        )
        for rec, med in rows
    ]

    completadas = sum(1 for t in tomas_hoy if t.estado == "tomado")
    pendientes = sum(1 for t in tomas_hoy if t.estado == "pendiente")
    omitidas = sum(1 for t in tomas_hoy if t.estado == "omitido")
    total = len(tomas_hoy)
    adherencia_pct = int(round((completadas / total) * 100)) if total > 0 else 100

    alertas = list(
        db.scalars(
            select(AlertaCuidador)
            .where(AlertaCuidador.id_usuario == user.id_usuario)
            .order_by(AlertaCuidador.id_alerta.desc())
            .limit(25)
        ).all()
    )
    no_atendidas = sum(1 for a in alertas if not a.atendida)
    hay_critica = any(a.es_critico and not a.atendida for a in alertas)

    estado_riesgo = (
        "Alerta Crítica Activa"
        if hay_critica
        else ("Atención Requerida" if (no_atendidas > 0 or omitidas > 0) else "Paciente Estable")
    )

    return CuidadorPanelResponse(
        paciente_nombre=user.nombre_completo,
        paciente_edad=edad,
        es_adulto_mayor=es_mayor,
        rango_edad_label=rango_label,
        adherencia_hoy_pct=adherencia_pct,
        tomas_completadas_hoy=completadas,
        tomas_pendientes_hoy=pendientes,
        tomas_omitidas_hoy=omitidas,
        estado_riesgo=estado_riesgo,
        nombre_cuidador=nombre_cuid,
        telefono_cuidador=tel_cuid,
        parentesco_cuidador=parentesco_cuid,
        alertas_no_atendidas=no_atendidas,
        alertas=[AlertaCuidadorOut.model_validate(a) for a in alertas],
        tomas_hoy=tomas_hoy,
    )


@router.post("/alertas", response_model=AlertaCuidadorOut)
def disparar_alerta_cuidador(
    body: AlertaCuidadorCreate,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alerta = registrar_alerta_cuidador_db(
        db=db,
        user=user,
        tipo_alerta=body.tipo_alerta,
        accion_origen=body.accion_origen,
        nombre_medicamento=body.nombre_medicamento,
        dosis=body.dosis,
        es_critico=body.es_critico,
        mensaje_custom=body.mensaje,
    )
    return AlertaCuidadorOut.model_validate(alerta)


@router.patch("/alertas/{id_alerta}/atender", response_model=AlertaCuidadorOut)
def marcar_alerta_atendida(
    id_alerta: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alerta = db.scalar(
        select(AlertaCuidador).where(
            AlertaCuidador.id_alerta == id_alerta,
            AlertaCuidador.id_usuario == user.id_usuario,
        )
    )
    if alerta is None:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    alerta.atendida = True
    db.commit()
    db.refresh(alerta)
    return AlertaCuidadorOut.model_validate(alerta)
