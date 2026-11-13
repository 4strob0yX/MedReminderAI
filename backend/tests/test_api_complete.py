from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.db.session import Base, get_db
from app.main import app
from app.models.alergia import AlergiaUsuario  # noqa: F401
from app.models.alerta_cuidador import AlertaCuidador  # noqa: F401
from app.models.contacto import ContactoApoyo  # noqa: F401
from app.models.medicamento import Medicamento
from app.models.password_reset import PasswordResetCode  # noqa: F401
from app.models.recordatorio import HistorialToma, Recordatorio
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.models.vinculacion_cuidador import VinculacionCuidador  # noqa: F401
from app.services.ollama_service import analizar_receta_ollama


@pytest.fixture()
def db_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client, TestingSession
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_auth_forgot_reset_profile_and_change_password(db_client):
    client, _Session = db_client

    reg = client.post(
        "/auth/register",
        json={
            "nombre": "Ana López",
            "email": "ana@example.com",
            "password": "Password123!",
            "fecha_nacimiento": "1955-04-10",
            "rol": "paciente",
        },
    )
    assert reg.status_code == 201
    token = reg.json()["access_token"]

    # Solicitar código de recuperación y rechazar reset sin código válido
    forgot = client.post("/auth/forgot-password", json={"email": "ana@example.com"})
    assert forgot.status_code == 200
    demo_code = forgot.json()["demo_code"]
    assert demo_code and len(demo_code) == 6

    bad_reset = client.post(
        "/auth/reset-password",
        json={
            "email": "ana@example.com",
            "codigo": "000000",
            "new_password": "NuevaPassword99!",
        },
    )
    assert bad_reset.status_code == 400

    ok_reset = client.post(
        "/auth/reset-password",
        json={
            "email": "ana@example.com",
            "codigo": demo_code,
            "new_password": "NuevaPassword99!",
        },
    )
    assert ok_reset.status_code == 200
    assert ok_reset.json()["access_token"]

    # Reutilizar código debe fallar
    reuse = client.post(
        "/auth/reset-password",
        json={
            "email": "ana@example.com",
            "codigo": demo_code,
            "new_password": "OtraPassword99!",
        },
    )
    assert reuse.status_code == 400

    # Login con nueva contraseña
    login = client.post(
        "/auth/login",
        json={"email": "ana@example.com", "password": "NuevaPassword99!"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Actualizar perfil completo
    upd = client.patch(
        "/auth/me",
        headers=_auth_header(token),
        json={"nombre_completo": "Ana López Ruiz", "rol": "paciente"},
    )
    assert upd.status_code == 200
    assert upd.json()["nombre_completo"] == "Ana López Ruiz"

    # Cambiar contraseña autenticada
    bad_chg = client.post(
        "/auth/change-password",
        headers=_auth_header(token),
        json={"current_password": "Incorrecta", "new_password": "FinalPassword123!"},
    )
    assert bad_chg.status_code == 401

    ok_chg = client.post(
        "/auth/change-password",
        headers=_auth_header(token),
        json={"current_password": "NuevaPassword99!", "new_password": "FinalPassword123!"},
    )
    assert ok_chg.status_code == 200


def test_vinculacion_cuidador_panel_y_ml_riesgo(db_client):
    client, SessionLocal = db_client

    # Registrar paciente y cuidador en cuentas separadas
    pac_res = client.post(
        "/auth/register",
        json={
            "nombre": "Carlos Mendoza",
            "email": "carlos@example.com",
            "password": "Password123!",
            "fecha_nacimiento": "1950-02-15",
            "rol": "paciente",
        },
    )
    cuid_res = client.post(
        "/auth/register",
        json={
            "nombre": "Laura Mendoza",
            "email": "laura@example.com",
            "password": "Password123!",
            "fecha_nacimiento": "1985-08-20",
            "rol": "cuidador",
        },
    )
    assert pac_res.status_code == 201
    assert cuid_res.status_code == 201
    pac_token = pac_res.json()["access_token"]
    cuid_token = cuid_res.json()["access_token"]

    pac_id = client.get("/auth/me", headers=_auth_header(pac_token)).json()["id_usuario"]

    # Sembrar medicamentos críticos e historial con omisiones para activar riesgo IA y alertas
    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    with SessionLocal() as db:
        for idx in range(4):
            med = Medicamento(
                id_usuario=pac_id,
                nombre=f"Fármaco Crítico {idx + 1}",
                dosis="50 mg",
                cantidad_stock=10,
                stock_inicial=30,
                es_critico=(idx == 0),
                permite_posponer=(idx != 0),
            )
            db.add(med)
            db.flush()
            trat = Tratamiento(
                id_medicamento=med.id_medicamento,
                frecuencia_horas=12,
                fecha_inicio=ahora - timedelta(days=5),
                estado="activo",
            )
            db.add(trat)
            db.flush()
            for day_back in range(3):
                rec = Recordatorio(
                    id_tratamiento=trat.id_tratamiento,
                    hora_programada=ahora - timedelta(days=day_back, hours=1),
                    estado="omitido",
                    veces_pospuesto=2,
                )
                db.add(rec)
        db.commit()

    # Cuidador NO vinculado aún no puede consultar evaluación ML del paciente
    forb_ml = client.get(f"/ai/evaluar-paciente/{pac_id}", headers=_auth_header(cuid_token))
    assert forb_ml.status_code == 403

    # Paciente genera código y cuidador se vincula
    cod_res = client.post("/cuidador/codigo-vinculacion", headers=_auth_header(pac_token))
    assert cod_res.status_code == 201
    codigo = cod_res.json()["codigo_vinculacion"]

    vinc_res = client.post(
        "/cuidador/vincular",
        headers=_auth_header(cuid_token),
        json={"codigo_vinculacion": codigo, "parentesco": "Hija"},
    )
    assert vinc_res.status_code == 200
    assert vinc_res.json()["id_paciente"] == pac_id

    # Cuidador consulta evaluación ML del paciente con BD real (sin errores de columnas ORM)
    ml_res = client.get(
        f"/ai/evaluar-paciente/{pac_id}?algoritmo=random_forest",
        headers=_auth_header(cuid_token),
    )
    assert ml_res.status_code == 200
    ml_json = ml_res.json()
    assert ml_json["paciente_id"] == pac_id
    assert ml_json["nivel_riesgo"] in ("CRÍTICO", "MODERADO", "BAJO")
    assert ml_json["datos_clinicos_extraidos"]["medicamentos_activos"] == 4

    # Cuidador consulta panel del paciente vinculado y verifica campos alineados
    panel_res = client.get(
        f"/cuidador/panel?id_paciente={pac_id}&tz_offset_minutes=0",
        headers=_auth_header(cuid_token),
    )
    assert panel_res.status_code == 200
    panel = panel_res.json()
    assert panel["id_paciente"] == pac_id
    assert panel["paciente_vinculado"] is True
    assert panel["estado_riesgo"] in ("alerta_critica", "atencion_requerida", "estable")
    assert panel["tomas_totales_hoy"] >= 1
    assert len(panel["alertas"]) >= 1

    # Cuidador marca alerta como atendida
    alerta_id = panel["alertas"][0]["id_alerta"]
    atender = client.patch(
        f"/cuidador/alertas/{alerta_id}/atender",
        headers=_auth_header(cuid_token),
    )
    assert atender.status_code == 200
    assert atender.json()["atendida"] is True


def test_estadisticas_y_escudo_racha_persistente(db_client):
    client, SessionLocal = db_client

    reg = client.post(
        "/auth/register",
        json={
            "nombre": "Marco Silva",
            "email": "marco@example.com",
            "password": "Password123!",
            "fecha_nacimiento": "1998-05-10",
            "rol": "paciente",
        },
    )
    assert reg.status_code == 201
    token = reg.json()["access_token"]
    uid = client.get("/auth/me", headers=_auth_header(token)).json()["id_usuario"]

    # Sembrar 8 días seguidos tomados para otorgar al menos 1 escudo de racha
    ahora = datetime.now(timezone.utc).replace(tzinfo=None)
    with SessionLocal() as db:
        med = Medicamento(
            id_usuario=uid,
            nombre="Vitamina D3",
            dosis="1000 UI",
            cantidad_stock=30,
            stock_inicial=30,
        )
        db.add(med)
        db.flush()
        trat = Tratamiento(
            id_medicamento=med.id_medicamento,
            frecuencia_horas=24,
            fecha_inicio=ahora - timedelta(days=9),
            estado="activo",
        )
        db.add(trat)
        db.flush()
        for d in range(8):
            ts = ahora - timedelta(days=d, hours=1)
            rec = Recordatorio(
                id_tratamiento=trat.id_tratamiento,
                hora_programada=ts,
                estado="tomado",
                veces_pospuesto=0,
            )
            db.add(rec)
            db.flush()
            db.add(
                HistorialToma(
                    id_recordatorio=rec.id_recordatorio,
                    fecha_accion=ts,
                    estado_final="tomado",
                )
            )
        db.commit()

    stats_before = client.get(
        "/recordatorios/estadisticas?tz_offset_minutes=0",
        headers=_auth_header(token),
    )
    assert stats_before.status_code == 200
    sb = stats_before.json()
    assert sb["racha_dias"] >= 7
    assert sb["escudos_racha"] >= 1
    assert sb["escudo_activo_hoy"] is False
    escudos_prev = sb["escudos_racha"]

    # Activar escudo persistente
    act = client.post(
        "/recordatorios/escudo?tz_offset_minutes=0",
        headers=_auth_header(token),
    )
    assert act.status_code == 200
    assert act.json()["escudo_activado"] is True
    assert act.json()["escudos_racha"] == escudos_prev - 1

    # Estadísticas subsecuentes reflejan escudo activo y descuento persistido
    stats_after = client.get(
        "/recordatorios/estadisticas?tz_offset_minutes=0",
        headers=_auth_header(token),
    )
    assert stats_after.status_code == 200
    sa = stats_after.json()
    assert sa["escudo_activo_hoy"] is True
    assert sa["escudos_racha"] == escudos_prev - 1


def test_analizar_receta_imagen_sin_ocr_ni_vision():
    with patch(
        "app.services.ollama_service._resolve_ollama_endpoint",
        return_value=(None, "medi-clinico", []),
    ):
        res = analizar_receta_ollama(
            texto_receta="",
            image_base64="ZmFrZV9pbWFnZQ==",
            db=None,
            user=None,
        )
    assert res.medicamentos == []
    assert "no se detectó texto ocr legible" in res.resumen_clinico.lower()
