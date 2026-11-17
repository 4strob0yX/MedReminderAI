from datetime import datetime
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import ACCESS, decode_token
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.vinculacion_cuidador import VinculacionCuidador
from app.core.mongo import consultar_historial_reportes_mongo
from app.schemas.ai import (
    AiAdherencePredictRequest,
    AiAdherencePredictResponse,
    AiChatRequest,
    AiChatResponse,
    AiConfirmMedicationsRequest,
    AiEvaluarPacienteResponse,
    AiMedicationSuggestRequest,
    AiMedicationSuggestResponse,
    AiPerfilIntegralResponse,
    AiPrescriptionScanRequest,
    AiPrescriptionScanResponse,
    AiStatusResponse,
)
from app.services.ml_analytics_service import (
    ejecutar_optimizacion_hiperparametros_p06,
    evaluar_perfil_integral_paciente,
    obtener_resumen_segmentacion_pca,
)
from app.services.ml_risk_service import (
    evaluar_perfil_integral_en_bd,
    evaluar_riesgo_paciente_en_bd,
    obtener_comparativa_algoritmos,
    obtener_info_dataset_entrenamiento,
    predecir_adherencia_ml,
)
from app.services.ollama_service import (
    analizar_receta_ollama,
    confirmar_medicamentos_chat,
    consultar_medi_ollama,
    obtener_estado_ollama,
    sugerir_medicamento_ia,
)

router = APIRouter(prefix="/ai", tags=["ai"])
_optional_bearer = HTTPBearer(auto_error=False)


def get_optional_user(
    creds: HTTPAuthorizationCredentials | None = Depends(_optional_bearer),
    db: Session = Depends(get_db),
) -> Usuario | None:
    if creds is None:
        return None
    try:
        user_id = decode_token(creds.credentials, ACCESS)
        return db.get(Usuario, user_id)
    except (jwt.PyJWTError, Exception):
        return None


@router.get("/status", response_model=AiStatusResponse)
def estado_motor_ia():
    """Devuelve el estado en tiempo real del motor Ollama (`medi-clinico`) y las reglas formales."""
    return obtener_estado_ollama()


@router.post("/chat", response_model=AiChatResponse)
def chat_clinico_medi(
    body: AiChatRequest,
    db: Session = Depends(get_db),
    current: Usuario | None = Depends(get_optional_user),
):
    """Consulta en tiempo real al modelo entrenado `medi-clinico` en Ollama con el contexto clínico del paciente.
    Si la consulta solicita agregar o programar medicamentos, los valida contra alergias/interacciones y los inserta."""
    return consultar_medi_ollama(
        query=body.query,
        db=db,
        user=current,
        fallback_name=body.nombre_usuario or "Paciente",
        tz_offset_minutes=body.tz_offset_minutes,
    )


@router.post("/confirmar-medicamentos", response_model=AiChatResponse)
def confirmar_insercion_medicamentos_chat(
    body: AiConfirmMedicationsRequest,
    db: Session = Depends(get_db),
    current: Usuario = Depends(get_current_user),
):
    """Confirma e inserta en el botiquín y agenda los medicamentos propuestos por Medi tras advertencia clínica."""
    return confirmar_medicamentos_chat(
        medicamentos=body.medicamentos,
        db=db,
        user=current,
        tz_offset_minutes=body.tz_offset_minutes,
    )


@router.post("/sugerir-medicamento", response_model=AiMedicationSuggestResponse)
def autocompletar_medicamento_ia(
    body: AiMedicationSuggestRequest,
    db: Session = Depends(get_db),
    current: Usuario | None = Depends(get_optional_user),
):
    """Autocompleta datos farmacológicos, dosis, horario e interacciones de un medicamento usando IA + Catálogo."""
    return sugerir_medicamento_ia(
        nombre=body.nombre,
        db=db,
        user=current,
    )


@router.post("/analizar-receta", response_model=AiPrescriptionScanResponse)
def escanear_receta_medica_ia(
    body: AiPrescriptionScanRequest,
    db: Session = Depends(get_db),
    current: Usuario | None = Depends(get_optional_user),
):
    """Analiza el texto OCR o imagen de una receta médica con nuestro modelo `medi-clinico` en Ollama
    y valida automáticamente alergias cruzadas e interacciones del paciente."""
    return analizar_receta_ollama(
        texto_receta=body.texto_receta,
        image_base64=body.image_base64,
        db=db,
        user=current,
    )


@router.post("/predecir-riesgo-adherencia", response_model=AiAdherencePredictResponse)
def predecir_riesgo_adherencia_endpoint(
    body: AiAdherencePredictRequest,
    algoritmo: str = "random_forest",
):
    """
    Clasifica el riesgo de abandono de un paciente utilizando Machine Learning.
    Permite elegir el algoritmo evaluado en la Práctica 05:
    'random_forest' (defecto), 'decision_tree' o 'knn'.
    """
    return predecir_adherencia_ml(
        edad=body.edad,
        medicamentos_activos=body.medicamentos_activos,
        adherencia_historica_pct=body.adherencia_historica_pct,
        retraso_promedio_min=body.retraso_promedio_min,
        tiene_cuidador=body.tiene_cuidador,
        algoritmo=algoritmo,
    )


def _verificar_autorizacion_paciente(db: Session, current: Usuario, paciente_id: int) -> None:
    """Valida que el usuario sea el propio paciente o un cuidador vinculado activamente."""
    if current.id_usuario == paciente_id:
        return
    vinculado = db.scalar(
        select(VinculacionCuidador.id_vinculacion).where(
            VinculacionCuidador.id_paciente == paciente_id,
            VinculacionCuidador.id_cuidador == current.id_usuario,
            VinculacionCuidador.estado == "activa",
        )
    )
    if vinculado is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes autorización para consultar la evaluación de este paciente",
        )


@router.get("/evaluar-paciente/{paciente_id}", response_model=AiEvaluarPacienteResponse)
def evaluar_paciente_bd_endpoint(
    paciente_id: int,
    algoritmo: str = "random_forest",
    db: Session = Depends(get_db),
    current: Usuario = Depends(get_current_user),
):
    """
    Extrae las métricas reales del paciente de MySQL (edad, medicamentos activos, tomas y retrasos)
    y ejecuta la inferencia del modelo ('random_forest', 'decision_tree' o 'knn').
    Accesible por el propio paciente o por un cuidador vinculado activamente.
    """
    _verificar_autorizacion_paciente(db, current, paciente_id)

    try:
        res = evaluar_riesgo_paciente_en_bd(db=db, paciente_id=paciente_id, algoritmo=algoritmo)
        pred = res["prediccion"]
        return AiEvaluarPacienteResponse(
            paciente_id=res["paciente_id"],
            nombre_paciente=res["nombre_paciente"],
            datos_clinicos_extraidos=res["datos_clinicos_extraidos"],
            **pred,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/datos-entrenamiento")
def consultar_datos_entrenamiento():
    """
    Retorna la información, metadatos, muestra de filas y métricas de exactitud
    del conjunto de datos clínicos utilizado para entrenar el modelo de Machine Learning.
    """
    return obtener_info_dataset_entrenamiento()


@router.get("/torneo-modelos")
def consultar_torneo_modelos_p05():
    """
    Retorna los resultados del Torneo de Algoritmos Supervisados (Práctica 05)
    comparando Decision Tree vs Random Forest vs KNN en Exactitud, Precisión, Recall y F1.
    """
    return obtener_comparativa_algoritmos()


@router.get("/optimizacion-hiperparametros")
def consultar_optimizacion_hiperparametros_p06():
    """
    Práctica 06: Devuelve la optimización de hiperparámetros con GridSearchCV y RandomizedSearchCV
    (StratifiedKFold) para Decision Tree, Random Forest y KNN.
    """
    return ejecutar_optimizacion_hiperparametros_p06()


@router.get("/segmentacion-pca")
def consultar_segmentacion_kmeans_y_pca():
    """
    Prácticas 07, 08, 09, 12 y 13: Devuelve perfiles K-Means, análisis de estabilidad ARI,
    escaladores, atípicos P95 y proyección PCA 2D con cargas y varianza explicada.
    """
    return obtener_resumen_segmentacion_pca()


@router.get("/perfil-integral/{paciente_id}", response_model=AiPerfilIntegralResponse)
def evaluar_perfil_integral_bd_endpoint(
    paciente_id: int,
    algoritmo: str = "random_forest",
    persistir: bool = True,
    db: Session = Depends(get_db),
    current: Usuario = Depends(get_current_user),
):
    """
    Prácticas 10 a 15: Evalúa integralmente al paciente desde MySQL combinando modelo supervisado,
    segmentación K-Means, detección de atípicos P95, coordenadas PCA 2D, motor de recomendaciones
    clínicas y persistencia en MongoDB (local o Atlas).
    """
    _verificar_autorizacion_paciente(db, current, paciente_id)
    try:
        return evaluar_perfil_integral_en_bd(
            db=db,
            paciente_id=paciente_id,
            algoritmo=algoritmo,
            persistir_mongo=persistir,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/perfil-integral", response_model=AiPerfilIntegralResponse)
def evaluar_perfil_integral_manual_endpoint(
    body: AiAdherencePredictRequest,
    algoritmo: str = "random_forest",
    persistir: bool = True,
    current: Usuario | None = Depends(get_optional_user),
):
    """
    Prácticas 10 a 15: Evalúa integralmente un vector clínico enviado en JSON (modo invitado/simulación)
    y persiste el reporte en MongoDB.
    """
    return evaluar_perfil_integral_paciente(
        edad=body.edad,
        medicamentos_activos=body.medicamentos_activos,
        adherencia_historica_pct=body.adherencia_historica_pct,
        retraso_promedio_min=body.retraso_promedio_min,
        tiene_cuidador=body.tiene_cuidador,
        algoritmo=algoritmo,
        id_usuario=current.id_usuario if current else None,
        nombre_paciente=current.nombre_completo if current else "Paciente",
        persistir_mongo=persistir,
    )


@router.get("/historial-reportes")
def consultar_historial_reportes_p15(
    limite: int = 10,
    current: Usuario | None = Depends(get_optional_user),
):
    """Práctica 15: Consulta los últimos reportes integrales guardados en MongoDB."""
    return consultar_historial_reportes_mongo(
        id_usuario=current.id_usuario if current else None,
        limite=limite,
    )



