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
from app.schemas.ai import (
    AiAdherencePredictRequest,
    AiAdherencePredictResponse,
    AiChatRequest,
    AiChatResponse,
    AiEvaluarPacienteResponse,
    AiMedicationSuggestRequest,
    AiMedicationSuggestResponse,
    AiPrescriptionScanRequest,
    AiPrescriptionScanResponse,
    AiStatusResponse,
)
from app.services.ml_risk_service import (
    evaluar_riesgo_paciente_en_bd,
    obtener_comparativa_algoritmos,
    obtener_info_dataset_entrenamiento,
    predecir_adherencia_ml,
)
from app.services.ollama_service import (
    analizar_receta_ollama,
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
    """Consulta en tiempo real al modelo entrenado `medi-clinico` en Ollama con el contexto clínico del paciente."""
    return consultar_medi_ollama(
        query=body.query,
        db=db,
        user=current,
        fallback_name=body.nombre_usuario or "Paciente",
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
    if current.id_usuario != paciente_id:
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



