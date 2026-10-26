import jwt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import ACCESS, decode_token
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.ai import (
    AiChatRequest,
    AiChatResponse,
    AiMedicationSuggestRequest,
    AiMedicationSuggestResponse,
    AiPrescriptionScanRequest,
    AiPrescriptionScanResponse,
    AiStatusResponse,
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
