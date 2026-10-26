from pydantic import BaseModel, Field


class AiChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=600)
    nombre_usuario: str | None = "Paciente"
    contexto_pantalla: str | None = "Hoy"


class AiDossierPoint(BaseModel):
    label: str
    description: str
    icon_type: str = "info"  # warning, schedule, check, shield, info


class AiChatResponse(BaseModel):
    title: str
    category: str
    risk_level: str
    risk_score: float = Field(ge=0.0, le=1.0, default=0.25)
    key_insight: str
    points: list[AiDossierPoint]
    golden_rule: str
    full_voice_script: str
    model_used: str = "medi-clinico"
    using_ollama: bool = True


class AiMedicationSuggestRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)


class AiMedicationSuggestResponse(BaseModel):
    nombre: str
    principio_activo: str
    familia: str
    dosis_sugerida: str
    frecuencia_horas_sugerida: int = 8
    forma_farmaceutica: str = "comprimidos"
    color_sugerido: str = "blanco"
    instrucciones_toma: str = "Con abundante agua"
    contraindicaciones: str
    es_critico_defecto: bool = False
    alerta_alergia: str | None = None
    alerta_interaccion: str | None = None
    model_used: str = "medi-clinico"


class AiStatusResponse(BaseModel):
    status: str
    ollama_reachable: bool
    active_model: str
    available_models: list[str]
    formal_rules_loaded: int = 6
