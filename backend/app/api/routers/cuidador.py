import secrets
from datetime import datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.alerta_cuidador import AlertaCuidador
from app.models.contacto import ContactoApoyo
from app.models.medicamento import Medicamento
from app.models.recordatorio import Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.models.vinculacion_cuidador import VinculacionCuidador
from app.schemas.auth import UsuarioOut
from app.schemas.cuidador import (
    AlertaCuidadorCreate,
    AlertaCuidadorOut,
    CodigoVinculacionOut,
    CuidadorPanelResponse,
    CuidadorVinculadoItem,
    PacienteVinculadoItem,
    TomaSupervisadaItem,
    VinculacionesResumenOut,
    VincularPacienteRequest,
)

router = APIRouter(prefix="/cuidador", tags=["cuidador"])

_ALFABETO_CODIGO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _generar_codigo_unico(db: Session) -> str:
    for _ in range(10):
        sufijo = "".join(secrets.choice(_ALFABETO_CODIGO) for _ in range(6))
        code = f"MED-{sufijo}"
        existe = db.scalar(
            select(VinculacionCuidador.id_vinculacion).where(
                VinculacionCuidador.codigo_vinculacion == code
            )
        )
        if existe is None:
            return code
    return f"MED-{secrets.token_hex(3).upper()}"


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
    tel_cuid = contacto.telefono if contacto else ""
    if contacto is None:
        vinc = db.scalar(
            select(VinculacionCuidador)
            .where(
                VinculacionCuidador.id_paciente == user.id_usuario,
                VinculacionCuidador.estado == "activa",
            )
            .order_by(VinculacionCuidador.id_vinculacion.asc())
        )
        if vinc and vinc.id_cuidador:
            cuidador_usr = db.get(Usuario, vinc.id_cuidador)
            if cuidador_usr:
                nombre_cuid = cuidador_usr.nombre_completo
                tel_cuid = cuidador_usr.correo

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


def _cargar_metricas_panel_paciente(
    db: Session,
    target_patient: Usuario,
    tz_offset_minutes: int,
) -> dict:
    ahora_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    hoy_local = (ahora_utc + timedelta(minutes=tz_offset_minutes)).date()
    inicio_utc = datetime.combine(hoy_local, time.min) - timedelta(minutes=tz_offset_minutes)
    fin_utc = inicio_utc + timedelta(days=1)

    stmt = (
        select(Recordatorio, Medicamento)
        .join(Tratamiento, Tratamiento.id_tratamiento == Recordatorio.id_tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .where(
            Medicamento.id_usuario == target_patient.id_usuario,
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
    criticas_omitidas = sum(1 for t in tomas_hoy if t.estado == "omitido" and t.es_critico)
    total = len(tomas_hoy)
    adherencia_pct = int(round((completadas / total) * 100)) if total > 0 else 100

    alertas = list(
        db.scalars(
            select(AlertaCuidador)
            .where(AlertaCuidador.id_usuario == target_patient.id_usuario)
            .order_by(AlertaCuidador.id_alerta.desc())
            .limit(25)
        ).all()
    )
    no_atendidas = sum(1 for a in alertas if not a.atendida)
    hay_critica = criticas_omitidas > 0 or any(a.es_critico and not a.atendida for a in alertas)

    if hay_critica:
        estado_riesgo = "alerta_critica"
        estado_riesgo_label = "Alerta Crítica Activa"
    elif no_atendidas > 0 or omitidas > 0:
        estado_riesgo = "atencion_requerida"
        estado_riesgo_label = "Atención Requerida"
    else:
        estado_riesgo = "estable"
        estado_riesgo_label = "Paciente Estable"

    return {
        "tomas_hoy": tomas_hoy,
        "completadas": completadas,
        "pendientes": pendientes,
        "omitidas": omitidas,
        "criticas_omitidas": criticas_omitidas,
        "total": total,
        "adherencia_pct": adherencia_pct,
        "alertas": alertas,
        "no_atendidas": no_atendidas,
        "estado_riesgo": estado_riesgo,
        "estado_riesgo_label": estado_riesgo_label,
    }


def _tiene_vinculacion_activa(db: Session, id_paciente: int, id_cuidador: int) -> bool:
    vinc = db.scalar(
        select(VinculacionCuidador.id_vinculacion).where(
            VinculacionCuidador.id_paciente == id_paciente,
            VinculacionCuidador.id_cuidador == id_cuidador,
            VinculacionCuidador.estado == "activa",
        )
    )
    return vinc is not None


@router.get("/panel", response_model=CuidadorPanelResponse)
def obtener_panel_cuidador(
    id_paciente: int | None = Query(default=None),
    tz_offset_minutes: int = Query(default=-360),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    paciente_vinculado = True
    target_patient = user

    if id_paciente is not None and id_paciente != user.id_usuario:
        if not _tiene_vinculacion_activa(db, id_paciente=id_paciente, id_cuidador=user.id_usuario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No estás vinculado activamente a este paciente",
            )
        p = db.get(Usuario, id_paciente)
        if p is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
        target_patient = p
    elif id_paciente is None and (user.rol or "").lower() == "cuidador":
        primera_vinc = db.scalar(
            select(VinculacionCuidador)
            .where(
                VinculacionCuidador.id_cuidador == user.id_usuario,
                VinculacionCuidador.estado == "activa",
            )
            .order_by(VinculacionCuidador.id_vinculacion.asc())
        )
        if primera_vinc is not None:
            p = db.get(Usuario, primera_vinc.id_paciente)
            if p is not None:
                target_patient = p
            else:
                paciente_vinculado = False
        else:
            paciente_vinculado = False

    u_out = UsuarioOut.model_validate(target_patient)
    edad = u_out.edad
    es_mayor = u_out.es_adulto_mayor
    rango_label = (
        f"Adulto Mayor Supervisado ({edad} años)"
        if es_mayor
        else f"Joven / Adulto ({edad} años · Modo Racha y Honor)"
    )

    contacto = db.scalars(
        select(ContactoApoyo)
        .where(ContactoApoyo.id_usuario == target_patient.id_usuario)
        .order_by(ContactoApoyo.es_principal.desc(), ContactoApoyo.id_contacto.asc())
    ).first()

    if contacto is not None:
        nombre_cuid = contacto.nombre_completo
        tel_cuid = contacto.telefono
        parentesco_cuid = contacto.parentesco
    elif target_patient.id_usuario != user.id_usuario:
        nombre_cuid = user.nombre_completo
        tel_cuid = user.correo
        parentesco_cuid = "Cuidador Vinculado"
    else:
        nombre_cuid = "Sin contacto principal"
        tel_cuid = ""
        parentesco_cuid = "Cuidador"

    metricas = _cargar_metricas_panel_paciente(db, target_patient, tz_offset_minutes)

    return CuidadorPanelResponse(
        id_paciente=target_patient.id_usuario,
        paciente_nombre=target_patient.nombre_completo,
        correo_paciente=target_patient.correo,
        paciente_edad=edad,
        es_adulto_mayor=es_mayor,
        rango_edad_label=rango_label,
        adherencia_hoy_pct=metricas["adherencia_pct"],
        tomas_totales_hoy=metricas["total"],
        tomas_completadas_hoy=metricas["completadas"],
        tomas_pendientes_hoy=metricas["pendientes"],
        tomas_omitidas_hoy=metricas["omitidas"],
        tomas_criticas_omitidas_hoy=metricas["criticas_omitidas"],
        estado_riesgo=metricas["estado_riesgo"],
        estado_riesgo_label=metricas["estado_riesgo_label"],
        nombre_cuidador=nombre_cuid,
        telefono_cuidador=tel_cuid,
        parentesco_cuidador=parentesco_cuid,
        alertas_no_atendidas=metricas["no_atendidas"],
        paciente_vinculado=paciente_vinculado,
        alertas=[AlertaCuidadorOut.model_validate(a) for a in metricas["alertas"]],
        tomas_hoy=metricas["tomas_hoy"],
    )


@router.post("/codigo-vinculacion", response_model=CodigoVinculacionOut, status_code=status.HTTP_201_CREATED)
def generar_codigo_vinculacion(
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Genera un código único (válido por 24h) para que un cuidador enlace su cuenta a este paciente."""
    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    db.execute(
        update(VinculacionCuidador)
        .where(
            VinculacionCuidador.id_paciente == user.id_usuario,
            VinculacionCuidador.estado == "pendiente",
        )
        .values(estado="revocada")
    )
    code = _generar_codigo_unico(db)
    vinc = VinculacionCuidador(
        id_paciente=user.id_usuario,
        id_cuidador=None,
        codigo_vinculacion=code,
        estado="pendiente",
        expira_en=ahora + timedelta(hours=24),
    )
    db.add(vinc)
    db.commit()
    db.refresh(vinc)
    return CodigoVinculacionOut(
        id_vinculacion=vinc.id_vinculacion,
        codigo_vinculacion=vinc.codigo_vinculacion,
        estado=vinc.estado,
        expira_en=vinc.expira_en,
    )


@router.post("/vincular", response_model=PacienteVinculadoItem)
def vincular_con_paciente(
    body: VincularPacienteRequest,
    tz_offset_minutes: int = Query(default=-360),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Permite a un cuidador enlazar su cuenta ingresando el código generado por el paciente."""
    code = body.codigo_vinculacion.strip().upper()
    vinc = db.scalar(
        select(VinculacionCuidador).where(VinculacionCuidador.codigo_vinculacion == code)
    )
    if vinc is None or vinc.estado == "revocada":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de vinculación inválido o revocado",
        )
    if vinc.estado == "activa":
        if vinc.id_cuidador == user.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya estás vinculado con este paciente",
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este código ya fue utilizado por otro cuidador",
        )

    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    if vinc.expira_en < ahora:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="El código de vinculación expiró. Pide al paciente generar uno nuevo.",
        )
    if vinc.id_paciente == user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes vincular tu propia cuenta como paciente y cuidador simultáneamente",
        )

    ya_vinculado = db.scalar(
        select(VinculacionCuidador).where(
            VinculacionCuidador.id_paciente == vinc.id_paciente,
            VinculacionCuidador.id_cuidador == user.id_usuario,
            VinculacionCuidador.estado == "activa",
        )
    )
    if ya_vinculado is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya cuentas con una vinculación activa con este paciente",
        )

    vinc.id_cuidador = user.id_usuario
    vinc.estado = "activa"
    vinc.parentesco = (body.parentesco or "Cuidador Familiar").strip()[:100]
    vinc.fecha_vinculacion = ahora
    db.commit()
    db.refresh(vinc)

    paciente = db.get(Usuario, vinc.id_paciente)
    if paciente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
    u_out = UsuarioOut.model_validate(paciente)
    metricas = _cargar_metricas_panel_paciente(db, paciente, tz_offset_minutes)

    return PacienteVinculadoItem(
        id_vinculacion=vinc.id_vinculacion,
        id_paciente=paciente.id_usuario,
        nombre_paciente=paciente.nombre_completo,
        correo_paciente=paciente.correo,
        edad_paciente=u_out.edad,
        parentesco=vinc.parentesco,
        estado_riesgo=metricas["estado_riesgo"],
        alertas_no_atendidas=metricas["no_atendidas"],
        fecha_vinculacion=vinc.fecha_vinculacion,
    )


@router.get("/pacientes", response_model=list[PacienteVinculadoItem])
def listar_pacientes_vinculados(
    tz_offset_minutes: int = Query(default=-360),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vinculaciones = db.scalars(
        select(VinculacionCuidador)
        .where(
            VinculacionCuidador.id_cuidador == user.id_usuario,
            VinculacionCuidador.estado == "activa",
        )
        .order_by(VinculacionCuidador.id_vinculacion.asc())
    ).all()

    items: list[PacienteVinculadoItem] = []
    for vinc in vinculaciones:
        paciente = db.get(Usuario, vinc.id_paciente)
        if paciente is None:
            continue
        u_out = UsuarioOut.model_validate(paciente)
        metricas = _cargar_metricas_panel_paciente(db, paciente, tz_offset_minutes)
        items.append(
            PacienteVinculadoItem(
                id_vinculacion=vinc.id_vinculacion,
                id_paciente=paciente.id_usuario,
                nombre_paciente=paciente.nombre_completo,
                correo_paciente=paciente.correo,
                edad_paciente=u_out.edad,
                parentesco=vinc.parentesco,
                estado_riesgo=metricas["estado_riesgo"],
                alertas_no_atendidas=metricas["no_atendidas"],
                fecha_vinculacion=vinc.fecha_vinculacion,
            )
        )
    return items


@router.get("/vinculaciones", response_model=VinculacionesResumenOut)
def obtener_resumen_vinculaciones(
    tz_offset_minutes: int = Query(default=-360),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    como_cuidador = listar_pacientes_vinculados(tz_offset_minutes=tz_offset_minutes, user=user, db=db)

    vinc_cuidadores = db.scalars(
        select(VinculacionCuidador)
        .where(
            VinculacionCuidador.id_paciente == user.id_usuario,
            VinculacionCuidador.estado == "activa",
        )
        .order_by(VinculacionCuidador.id_vinculacion.asc())
    ).all()
    cuidadores_out: list[CuidadorVinculadoItem] = []
    for v in vinc_cuidadores:
        if v.id_cuidador is None:
            continue
        c_usr = db.get(Usuario, v.id_cuidador)
        if c_usr is None:
            continue
        cuidadores_out.append(
            CuidadorVinculadoItem(
                id_vinculacion=v.id_vinculacion,
                id_cuidador=c_usr.id_usuario,
                nombre_cuidador=c_usr.nombre_completo,
                correo_cuidador=c_usr.correo,
                parentesco=v.parentesco,
                fecha_vinculacion=v.fecha_vinculacion,
            )
        )

    cod_pendiente = db.scalar(
        select(VinculacionCuidador)
        .where(
            VinculacionCuidador.id_paciente == user.id_usuario,
            VinculacionCuidador.estado == "pendiente",
            VinculacionCuidador.expira_en >= ahora,
        )
        .order_by(VinculacionCuidador.id_vinculacion.desc())
    )
    codigo_activo = (
        CodigoVinculacionOut(
            id_vinculacion=cod_pendiente.id_vinculacion,
            codigo_vinculacion=cod_pendiente.codigo_vinculacion,
            estado=cod_pendiente.estado,
            expira_en=cod_pendiente.expira_en,
        )
        if cod_pendiente is not None
        else None
    )
    return VinculacionesResumenOut(
        como_cuidador=como_cuidador,
        cuidadores_vinculados=cuidadores_out,
        codigo_activo=codigo_activo,
    )


@router.delete("/vinculaciones/{id_vinculacion}", status_code=status.HTTP_204_NO_CONTENT)
def revocar_vinculacion(
    id_vinculacion: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vinc = db.get(VinculacionCuidador, id_vinculacion)
    if vinc is None or (vinc.id_paciente != user.id_usuario and vinc.id_cuidador != user.id_usuario):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vinculación no encontrada")
    vinc.estado = "revocada"
    db.commit()
    return None


@router.post("/alertas", response_model=AlertaCuidadorOut)
def disparar_alerta_cuidador(
    body: AlertaCuidadorCreate,
    id_paciente: int | None = Query(default=None),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_user = user
    if id_paciente is not None and id_paciente != user.id_usuario:
        if not _tiene_vinculacion_activa(db, id_paciente=id_paciente, id_cuidador=user.id_usuario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado para emitir alertas en este paciente",
            )
        p = db.get(Usuario, id_paciente)
        if p is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")
        target_user = p

    alerta = registrar_alerta_cuidador_db(
        db=db,
        user=target_user,
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
    alerta = db.get(AlertaCuidador, id_alerta)
    if alerta is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrada")

    autorizado = alerta.id_usuario == user.id_usuario or _tiene_vinculacion_activa(
        db, id_paciente=alerta.id_usuario, id_cuidador=user.id_usuario
    )
    if not autorizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrada")

    alerta.atendida = True
    db.commit()
    db.refresh(alerta)
    return AlertaCuidadorOut.model_validate(alerta)
