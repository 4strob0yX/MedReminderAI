package com.medreminder.ai.data.remote

import com.google.gson.annotations.SerializedName

data class MedicamentoCreateDto(
    val nombre: String,
    @SerializedName("principio_activo") val principioActivo: String? = null,
    val dosis: String,
    @SerializedName("cantidad_stock") val cantidadStock: Int,
    @SerializedName("stock_inicial") val stockInicial: Int? = null,
    @SerializedName("forma_farmaceutica") val formaFarmaceutica: String? = "comprimidos",
    @SerializedName("color_pastilla") val colorPastilla: String? = "blanco",
    @SerializedName("instrucciones_toma") val instruccionesToma: String? = null,
    val proposito: String? = null,
    @SerializedName("permite_posponer") val permitePosponer: Boolean = true,
    @SerializedName("es_critico") val esCritico: Boolean = false,
    val contraindicaciones: String? = null
)

data class MedicamentoDto(
    @SerializedName("id_medicamento") val idMedicamento: Int,
    val nombre: String,
    @SerializedName("principio_activo") val principioActivo: String? = null,
    val dosis: String,
    @SerializedName("cantidad_stock") val cantidadStock: Int,
    @SerializedName("stock_inicial") val stockInicial: Int? = null,
    @SerializedName("forma_farmaceutica") val formaFarmaceutica: String? = null,
    @SerializedName("color_pastilla") val colorPastilla: String? = null,
    @SerializedName("instrucciones_toma") val instruccionesToma: String? = null,
    val proposito: String? = null,
    @SerializedName("permite_posponer") val permitePosponer: Boolean = true,
    @SerializedName("es_critico") val esCritico: Boolean = false,
    val contraindicaciones: String? = null
)

data class StockUpdateDto(
    @SerializedName("cantidad_stock") val cantidadStock: Int
)

data class TratamientoCreateDto(
    @SerializedName("id_medicamento") val idMedicamento: Int,
    @SerializedName("frecuencia_horas") val frecuenciaHoras: Int,
    @SerializedName("fecha_inicio") val fechaInicio: String? = null,
    @SerializedName("fecha_fin") val fechaFin: String? = null,
    val estado: String = "activo"
)

data class TratamientoDto(
    @SerializedName("id_tratamiento") val idTratamiento: Int,
    @SerializedName("id_medicamento") val idMedicamento: Int,
    @SerializedName("frecuencia_horas") val frecuenciaHoras: Int,
    @SerializedName("fecha_inicio") val fechaInicio: String,
    @SerializedName("fecha_fin") val fechaFin: String?,
    val estado: String
)

data class TratamientoUpdateDto(
    @SerializedName("frecuencia_horas") val frecuenciaHoras: Int? = null,
    @SerializedName("fecha_inicio") val fechaInicio: String? = null,
    @SerializedName("fecha_fin") val fechaFin: String? = null,
    val estado: String? = null
)

data class RecordatorioDto(
    @SerializedName("id_recordatorio") val idRecordatorio: Int,
    @SerializedName("id_tratamiento") val idTratamiento: Int,
    @SerializedName("id_medicamento") val idMedicamento: Int? = null,
    @SerializedName("hora_programada") val horaProgramada: String,
    val estado: String,
    @SerializedName("veces_pospuesto") val vecesPospuesto: Int,
    @SerializedName("permite_posponer") val permitePosponer: Boolean = true,
    @SerializedName("es_critico") val esCritico: Boolean = false,
    @SerializedName("posponer_bloqueado_por_castigo") val posponerBloqueadoPorCastigo: Boolean = false,
    @SerializedName("nombre_medicamento") val nombreMedicamento: String? = null,
    val dosis: String? = null,
    val proposito: String? = null,
    @SerializedName("forma_farmaceutica") val formaFarmaceutica: String? = null,
    @SerializedName("color_pastilla") val colorPastilla: String? = null,
    @SerializedName("instrucciones_toma") val instruccionesToma: String? = null
)

data class MedicamentoCatalogoItemDto(
    val nombre: String,
    @SerializedName("principio_activo") val principioActivo: String,
    val familia: String,
    @SerializedName("dosis_sugerida") val dosisSugerida: String,
    @SerializedName("forma_farmaceutica") val formaFarmaceutica: String,
    val contraindicaciones: String,
    @SerializedName("es_critico_defecto") val esCriticoDefecto: Boolean = false,
    @SerializedName("color_sugerido") val colorSugerido: String? = null,
    @SerializedName("instrucciones_toma") val instruccionesToma: String? = null
)

data class AlergiaCreateDto(
    val sustancia: String,
    val severidad: String = "grave",
    val reaccion: String? = null
)

data class AlergiaDto(
    @SerializedName("id_alergia") val idAlergia: Int,
    val sustancia: String,
    val severidad: String,
    val reaccion: String?,
    @SerializedName("fecha_registro") val fechaRegistro: String
)

data class ContactoApoyoCreateDto(
    @SerializedName("nombre_completo") val nombreCompleto: String,
    val telefono: String,
    val parentesco: String,
    val correo: String? = null,
    @SerializedName("es_principal") val esPrincipal: Boolean = true
)

data class ContactoApoyoDto(
    @SerializedName("id_contacto") val idContacto: Int,
    @SerializedName("nombre_completo") val nombreCompleto: String,
    val telefono: String,
    val parentesco: String,
    val correo: String?,
    @SerializedName("es_principal") val esPrincipal: Boolean,
    @SerializedName("fecha_registro") val fechaRegistro: String
)

data class VerificarAlergiasInDto(
    val nombre: String,
    @SerializedName("principio_activo") val principioActivo: String? = null
)

data class VerificarAlergiasOutDto(
    @SerializedName("tiene_conflicto") val tieneConflicto: Boolean,
    val alerta: String?,
    @SerializedName("alergia_detectada") val alergiaDetectada: String?,
    @SerializedName("severidad") val severidad: String?
)


// --- Motor de Inteligencia Artificial Clínica (Ollama medi-clinico) ---

data class AiChatRequestDto(
    val query: String,
    @SerializedName("nombre_usuario") val nombreUsuario: String? = "Paciente",
    @SerializedName("contexto_pantalla") val contextoPantalla: String? = "Hoy"
)

data class AiDossierPointDto(
    val label: String,
    val description: String,
    @SerializedName("icon_type") val iconType: String = "info"
)

data class AiChatResponseDto(
    val title: String,
    val category: String,
    @SerializedName("risk_level") val riskLevel: String,
    @SerializedName("risk_score") val riskScore: Float = 0.25f,
    @SerializedName("key_insight") val keyInsight: String,
    val points: List<AiDossierPointDto> = emptyList(),
    @SerializedName("golden_rule") val goldenRule: String,
    @SerializedName("full_voice_script") val fullVoiceScript: String,
    @SerializedName("model_used") val modelUsed: String = "medi-clinico",
    @SerializedName("using_ollama") val usingOllama: Boolean = true
)

data class AiMedicationSuggestRequestDto(
    val nombre: String
)

data class AiMedicationSuggestResponseDto(
    val nombre: String,
    @SerializedName("principio_activo") val principioActivo: String,
    val familia: String,
    @SerializedName("dosis_sugerida") val dosisSugerida: String,
    @SerializedName("frecuencia_horas_sugerida") val frecuenciaHorasSugerida: Int = 8,
    @SerializedName("forma_farmaceutica") val formaFarmaceutica: String = "comprimidos",
    @SerializedName("color_sugerido") val colorSugerido: String = "blanco",
    @SerializedName("instrucciones_toma") val instruccionesToma: String = "Con abundante agua",
    val contraindicaciones: String,
    @SerializedName("es_critico_defecto") val esCriticoDefecto: Boolean = false,
    @SerializedName("alerta_alergia") val alertaAlergia: String? = null,
    @SerializedName("alerta_interaccion") val alertaInteraccion: String? = null,
    @SerializedName("model_used") val modelUsed: String = "medi-clinico"
)

data class AiPrescriptionScanRequestDto(
    @SerializedName("texto_receta") val textoReceta: String? = null,
    @SerializedName("image_base64") val imageBase64: String? = null
)

data class AiPrescriptionMedItemDto(
    val name: String,
    @SerializedName("principio_activo") val principioActivo: String = "",
    val dosage: String,
    @SerializedName("frequency_hours") val frequencyHours: Int = 8,
    @SerializedName("duration_days") val durationDays: Int = 7,
    val instructions: String = "Tomar con abundante agua",
    @SerializedName("forma_farmaceutica") val formaFarmaceutica: String = "comprimidos",
    @SerializedName("color_sugerido") val colorSugerido: String = "blanco",
    @SerializedName("es_critico") val esCritico: Boolean = false,
    val confidence: String = "high",
    @SerializedName("alerta_alergia") val alertaAlergia: String? = null,
    @SerializedName("alerta_interaccion") val alertaInteraccion: String? = null
)

data class AiPrescriptionScanResponseDto(
    val medico: String = "Médico Tratante",
    @SerializedName("resumen_clinico") val resumenClinico: String,
    val medicamentos: List<AiPrescriptionMedItemDto> = emptyList(),
    @SerializedName("model_used") val modelUsed: String = "medi-clinico",
    @SerializedName("using_ollama") val usingOllama: Boolean = true
)

// --- Supervisión, Estadísticas, Predictor ML y Vinculación de Cuidador ---

data class AdherenciaDiaOutDto(
    val dia: String,
    val fecha: String,
    val tomadas: Int = 0,
    val programadas: Int = 0,
    val omitidas: Int = 0,
    val pospuestas: Int = 0,
    val porcentaje: Float = 0f
)

data class AdherenciaMedicamentoOutDto(
    @SerializedName("id_medicamento") val idMedicamento: Int,
    val nombre: String,
    val dosis: String,
    val tomadas: Int = 0,
    val omitidas: Int = 0,
    val programadas: Int = 0,
    val porcentaje: Float = 100f
)

data class DiaMapaCalorOutDto(
    val dia: String,
    val omisiones: Int = 0,
    val tomadas: Int = 0,
    val total: Int = 0
)

data class BloqueMapaCalorOutDto(
    val franja: String,
    val dias: List<DiaMapaCalorOutDto> = emptyList(),
    val valores: List<Int> = emptyList(),
    @SerializedName("total_omisiones") val totalOmisiones: Int = 0
)

data class EstadisticasOutDto(
    @SerializedName("racha_dias") val rachaDias: Int = 0,
    @SerializedName("color_fuego") val colorFuego: String = "gris",
    @SerializedName("escudos_racha") val escudosRacha: Int = 0,
    @SerializedName("xp_honor") val xpHonor: Int = 0,
    @SerializedName("xp_siguiente_rango") val xpSiguienteRango: Int = 100,
    @SerializedName("rango_honor") val rangoHonor: String = "Hierro",
    @SerializedName("emblema_agrietado") val emblemaAgrietado: Boolean = false,
    @SerializedName("posponer_bloqueado") val posponerBloqueado: Boolean = false,
    @SerializedName("dias_limpios_recuperacion") val diasLimpiosRecuperacion: Int = 3,
    @SerializedName("requiere_alerta_cuidador") val requiereAlertaCuidador: Boolean = false,
    @SerializedName("mensaje_alerta_cuidador") val mensajeAlertaCuidador: String? = null,
    @SerializedName("contacto_principal_nombre") val contactoPrincipalNombre: String? = null,
    @SerializedName("contacto_principal_telefono") val contactoPrincipalTelefono: String? = null,
    @SerializedName("porcentaje_global") val porcentajeGlobal: Float = 100f,
    @SerializedName("total_tomadas") val totalTomadas: Int = 0,
    @SerializedName("total_omitidas") val totalOmitidas: Int = 0,
    @SerializedName("total_pospuestas") val totalPospuestas: Int = 0,
    @SerializedName("adherencia_semanal") val adherenciaSemanal: List<AdherenciaDiaOutDto> = emptyList(),
    @SerializedName("adherencia_por_medicamento") val adherenciaPorMedicamento: List<AdherenciaMedicamentoOutDto> = emptyList(),
    @SerializedName("mapa_calor") val mapaCalor: List<BloqueMapaCalorOutDto> = emptyList(),
    @SerializedName("insight_debilidad") val insightDebilidad: String = "",
    @SerializedName("escudo_activo_hoy") val escudoActivoHoy: Boolean = false,
    @SerializedName("escudo_usado_fecha") val escudoUsadoFecha: String? = null
)

data class EscudoActivarResponseDto(
    @SerializedName("escudo_activado") val escudoActivado: Boolean,
    @SerializedName("escudos_racha") val escudosRacha: Int,
    @SerializedName("escudo_usado_fecha") val escudoUsadoFecha: String,
    val mensaje: String
)

data class AiAdherencePredictRequestDto(
    val edad: Int,
    @SerializedName("medicamentos_activos") val medicamentosActivos: Int,
    @SerializedName("adherencia_historica_pct") val adherenciaHistoricaPct: Float,
    @SerializedName("retraso_promedio_min") val retrasoPromedioMin: Float,
    @SerializedName("tiene_cuidador") val tieneCuidador: Int
)

data class AiEvaluarPacienteResponseDto(
    @SerializedName("paciente_id") val pacienteId: Int = 0,
    @SerializedName("nombre_paciente") val nombrePaciente: String = "",
    @SerializedName("datos_clinicos_extraidos") val datosClinicosExtraidos: Map<String, Float> = emptyMap(),
    @SerializedName("riesgo_abandono") val riesgoAbandono: Boolean = false,
    @SerializedName("nivel_riesgo") val nivelRiesgo: String = "BAJO",
    @SerializedName("probabilidad_abandono_pct") val probabilidadAbandonoPct: Float = 0f,
    @SerializedName("probabilidad_adherencia_pct") val probabilidadAdherenciaPct: Float = 100f,
    @SerializedName("factores_riesgo") val factoresRiesgo: List<String> = emptyList(),
    @SerializedName("recomendacion_clinica") val recomendacionClinica: String = "",
    @SerializedName("alerta_disparada") val alertaDisparada: Boolean = false,
    val modelo: String = "RandomForestClassifier"
)

data class TorneoModeloItemDto(
    val clave: String,
    val nombre: String,
    @SerializedName("exactitud_val_pct") val exactitudValPct: Float = 0f,
    @SerializedName("precision_pct") val precisionPct: Float = 0f,
    @SerializedName("recall_sensibilidad_pct") val recallSensibilidadPct: Float = 0f,
    @SerializedName("f1_score_pct") val f1ScorePct: Float = 0f
)

data class TorneoModelosResponseDto(
    @SerializedName("algoritmo_activo") val algoritmoActivo: String = "random_forest",
    @SerializedName("particion_datos") val particionDatos: Map<String, String> = emptyMap(),
    @SerializedName("tabla_comparativa") val tablaComparativa: List<TorneoModeloItemDto> = emptyList(),
    @SerializedName("criterio_seleccion") val criterioSeleccion: String = ""
)

data class AlertaCuidadorCreateDto(
    @SerializedName("tipo_alerta") val tipoAlerta: String, // "advertencia_normal" | "critica_automatica"
    @SerializedName("nombre_medicamento") val medicamentoNombre: String,
    val dosis: String,
    @SerializedName("accion_origen") val accion: String, // "posponer" | "omitir"
    @SerializedName("es_critico") val esCritico: Boolean = false,
    val mensaje: String? = null
)

data class AlertaCuidadorDto(
    @SerializedName("id_alerta") val idAlerta: Int,
    @SerializedName("id_paciente") val idPaciente: Int = 0,
    @SerializedName("nombre_paciente") val nombrePaciente: String = "",
    @SerializedName("edad_paciente") val edadPaciente: Int = 68,
    @SerializedName("tipo_alerta") val tipoAlerta: String,
    @SerializedName(value = "nombre_medicamento", alternate = ["medicamento_nombre"]) val medicamentoNombre: String = "",
    val dosis: String = "",
    @SerializedName(value = "accion_origen", alternate = ["accion"]) val accion: String = "posponer",
    @SerializedName("es_critico") val esCritico: Boolean = false,
    val mensaje: String = "",
    @SerializedName("nombre_cuidador") val nombreCuidador: String = "",
    @SerializedName("telefono_cuidador") val telefonoCuidador: String = "",
    val atendida: Boolean = false,
    @SerializedName("fecha_creacion") val fechaCreacion: String = ""
)

data class TomaSupervisadaItemDto(
    @SerializedName("id_recordatorio") val idRecordatorio: Int,
    @SerializedName("nombre_medicamento") val nombreMedicamento: String,
    val dosis: String,
    @SerializedName("hora_programada") val horaProgramada: String,
    val estado: String,
    @SerializedName("es_critico") val esCritico: Boolean,
    @SerializedName("veces_pospuesto") val vecesPospuesto: Int
)

data class CuidadorPanelResponseDto(
    @SerializedName("id_paciente") val idPaciente: Int = 0,
    @SerializedName(value = "paciente_nombre", alternate = ["nombre_paciente"]) val nombrePaciente: String = "",
    @SerializedName("correo_paciente") val correoPaciente: String = "",
    @SerializedName("fecha_nacimiento") val fechaNacimiento: String? = null,
    @SerializedName(value = "paciente_edad", alternate = ["edad_paciente"]) val edadPaciente: Int = 68,
    @SerializedName("es_adulto_mayor") val esAdultoMayor: Boolean = true,
    @SerializedName(value = "rango_edad_label", alternate = ["rango_edad"]) val rangoEdad: String = "adulto_mayor",
    @SerializedName("adherencia_hoy_pct") val adherenciaHoyPct: Int = 0,
    @SerializedName("tomas_completadas_hoy") val tomasCompletadasHoy: Int = 0,
    @SerializedName("tomas_pendientes_hoy") val tomasPendientesHoy: Int = 0,
    @SerializedName("tomas_totales_hoy") val tomasTotalesHoy: Int = 0,
    @SerializedName("tomas_omitidas_hoy") val tomasOmitidasHoy: Int = 0,
    @SerializedName("tomas_criticas_omitidas_hoy") val tomasCriticasOmitidasHoy: Int = 0,
    @SerializedName("nombre_cuidador") val nombreCuidador: String = "",
    @SerializedName("telefono_cuidador") val telefonoCuidador: String = "",
    @SerializedName("parentesco_cuidador") val parentescoCuidador: String = "",
    @SerializedName("alertas_no_atendidas") val alertasNoAtendidas: Int = 0,
    @SerializedName("paciente_vinculado") val pacienteVinculado: Boolean = true,
    @SerializedName(value = "alertas", alternate = ["alertas_activas"]) val alertasActivas: List<AlertaCuidadorDto> = emptyList(),
    @SerializedName("tomas_hoy") val tomasHoy: List<TomaSupervisadaItemDto> = emptyList(),
    @SerializedName("estado_riesgo") val estadoRiesgo: String = "estable",
    @SerializedName("estado_riesgo_label") val estadoRiesgoLabel: String = "Paciente Estable"
)

data class CodigoVinculacionOutDto(
    @SerializedName("id_vinculacion") val idVinculacion: Int,
    @SerializedName("codigo_vinculacion") val codigoVinculacion: String,
    val estado: String,
    @SerializedName("expira_en") val expiraEn: String
)

data class VincularPacienteRequestDto(
    @SerializedName("codigo_vinculacion") val codigoVinculacion: String,
    val parentesco: String? = null
)

data class PacienteVinculadoItemDto(
    @SerializedName("id_vinculacion") val idVinculacion: Int,
    @SerializedName("id_paciente") val idPaciente: Int,
    @SerializedName("nombre_paciente") val nombrePaciente: String,
    @SerializedName("correo_paciente") val correoPaciente: String,
    @SerializedName("edad_paciente") val edadPaciente: Int,
    val parentesco: String? = null,
    @SerializedName("estado_riesgo") val estadoRiesgo: String = "estable",
    @SerializedName("alertas_no_atendidas") val alertasNoAtendidas: Int = 0,
    @SerializedName("fecha_vinculacion") val fechaVinculacion: String? = null
)

data class CuidadorVinculadoItemDto(
    @SerializedName("id_vinculacion") val idVinculacion: Int,
    @SerializedName("id_cuidador") val idCuidador: Int,
    @SerializedName("nombre_cuidador") val nombreCuidador: String,
    @SerializedName("correo_cuidador") val correoCuidador: String,
    val parentesco: String? = null,
    @SerializedName("fecha_vinculacion") val fechaVinculacion: String? = null
)

data class VinculacionesResumenOutDto(
    @SerializedName("como_cuidador") val comoCuidador: List<PacienteVinculadoItemDto> = emptyList(),
    @SerializedName("cuidadores_vinculados") val cuidadoresVinculados: List<CuidadorVinculadoItemDto> = emptyList(),
    @SerializedName("codigo_activo") val codigoActivo: CodigoVinculacionOutDto? = null
)

data class DashboardUnificadoDto(
    val medicamentos: List<MedicamentoDto> = emptyList(),
    val tratamientos: List<TratamientoDto> = emptyList(),
    @SerializedName("recordatorios_hoy") val recordatoriosHoy: List<RecordatorioDto> = emptyList(),
    val alergias: List<AlergiaDto> = emptyList(),
    @SerializedName("contactos_apoyo") val contactosApoyo: List<ContactoApoyoDto> = emptyList(),
    val perfil: UsuarioDto? = null
)
