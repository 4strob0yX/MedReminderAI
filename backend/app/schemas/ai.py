from pydantic import BaseModel, Field


class AiChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=600)
    nombre_usuario: str | None = "Paciente"
    contexto_pantalla: str | None = "Hoy"
    tz_offset_minutes: int | None = None


class AiDossierPoint(BaseModel):
    label: str
    description: str
    icon_type: str = "info"  # warning, schedule, check, shield, info


class AiChatMedicationActionItem(BaseModel):
    id_medicamento: int | None = None
    id_tratamiento: int | None = None
    nombre: str
    principio_activo: str = ""
    dosis: str = "1 comprimido"
    frecuencia_horas: int = 8
    duracion_dias: int | None = None
    hora_primera_toma: str | None = None
    cantidad_stock: int = 30
    forma_farmaceutica: str = "comprimidos"
    color_pastilla: str = "blanco"
    instrucciones_toma: str = "Tomar con abundante agua"
    proposito: str = "Registrado por Medi IA"
    contraindicaciones: str | None = None
    es_critico: bool = False
    permite_posponer: bool = True
    alerta_alergia: str | None = None
    alerta_interaccion: str | None = None
    creado_en_bd: bool = False


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
    action_performed: str | None = None
    medications_affected: list[AiChatMedicationActionItem] = Field(default_factory=list)


class AiConfirmMedicationsRequest(BaseModel):
    medicamentos: list[AiChatMedicationActionItem] = Field(..., min_length=1, max_length=8)
    tz_offset_minutes: int | None = None


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


class AiPrescriptionScanRequest(BaseModel):
    texto_receta: str | None = Field(default=None, max_length=4000)
    image_base64: str | None = None


class AiPrescriptionMedItem(BaseModel):
    name: str
    principio_activo: str = ""
    dosage: str
    frequency_hours: int = 8
    duration_days: int = 7
    instructions: str = "Tomar con abundante agua"
    forma_farmaceutica: str = "comprimidos"
    color_sugerido: str = "blanco"
    es_critico: bool = False
    confidence: str = "high"  # "high" | "low"
    alerta_alergia: str | None = None
    alerta_interaccion: str | None = None


class AiPrescriptionScanResponse(BaseModel):
    medico: str = "Médico Tratante"
    resumen_clinico: str
    medicamentos: list[AiPrescriptionMedItem]
    model_used: str = "medi-clinico"
    using_ollama: bool = True


class AiAdherencePredictRequest(BaseModel):
    edad: int = Field(..., ge=0, le=120, description="Edad del paciente")
    medicamentos_activos: int = Field(..., ge=1, le=30, description="Cantidad de fármacos diarios")
    adherencia_historica_pct: float = Field(..., ge=0.0, le=100.0, description="Porcentaje histórico de tomas a tiempo")
    retraso_promedio_min: float = Field(..., ge=0.0, description="Minutos promedio de retraso al confirmar toma")
    tiene_cuidador: int = Field(default=0, ge=0, le=1, description="1 si tiene cuidador asignado, 0 si no")


class AiAdherencePredictResponse(BaseModel):
    riesgo_abandono: bool
    nivel_riesgo: str  # "BAJO" | "MODERADO" | "CRÍTICO"
    probabilidad_abandono_pct: float
    probabilidad_adherencia_pct: float
    factores_riesgo: list[str]
    recomendacion_clinica: str
    alerta_disparada: bool
    modelo: str = "DecisionTreeClassifier (Scikit-Learn 04/11)"


class AiEvaluarPacienteResponse(AiAdherencePredictResponse):
    paciente_id: int
    nombre_paciente: str
    datos_clinicos_extraidos: dict[str, float | int]


class AiPersistenciaMongoInfo(BaseModel):
    guardado: bool
    modo: str
    id_analisis: str = ""
    coleccion: str = ""
    fecha_registro_utc: str = ""
    detalle: str | None = None


class AiPerfilIntegralResponse(BaseModel):
    paciente_id: int
    nombre_paciente: str
    datos_clinicos_extraidos: dict[str, float | int]
    prediccion: AiAdherencePredictResponse
    cluster_kmeans: int
    perfil_kmeans: str
    distancia_centroide: float
    umbral_atipico_p95: float
    es_atipico: bool
    pc1: float
    pc2: float
    recomendaciones_motor: list[str]
    persistencia_mongo: AiPersistenciaMongoInfo


