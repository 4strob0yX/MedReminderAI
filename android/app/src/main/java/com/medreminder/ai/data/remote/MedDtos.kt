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

data class RecordatorioDto(
    @SerializedName("id_recordatorio") val idRecordatorio: Int,
    @SerializedName("id_tratamiento") val idTratamiento: Int,
    @SerializedName("hora_programada") val horaProgramada: String,
    val estado: String,
    @SerializedName("veces_pospuesto") val vecesPospuesto: Int,
    @SerializedName("permite_posponer") val permitePosponer: Boolean = true,
    @SerializedName("es_critico") val esCritico: Boolean = false,
    @SerializedName("nombre_medicamento") val nombreMedicamento: String? = null,
    val dosis: String? = null,
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

// --- Supervisión y Vista del Cuidador (Adultos Mayores y Alertas Críticas) ---

data class AlertaCuidadorCreateDto(
    @SerializedName("tipo_alerta") val tipoAlerta: String, // "advertencia_normal" | "critica_automatica"
    @SerializedName("medicamento_nombre") val medicamentoNombre: String,
    val dosis: String,
    val accion: String, // "posponer" | "omitir"
    @SerializedName("es_critico") val esCritico: Boolean = false,
    val mensaje: String
)

data class AlertaCuidadorDto(
    @SerializedName("id_alerta") val idAlerta: Int,
    @SerializedName("id_paciente") val idPaciente: Int,
    @SerializedName("nombre_paciente") val nombrePaciente: String,
    @SerializedName("edad_paciente") val edadPaciente: Int,
    @SerializedName("tipo_alerta") val tipoAlerta: String,
    @SerializedName("medicamento_nombre") val medicamentoNombre: String,
    val dosis: String,
    val accion: String,
    @SerializedName("es_critico") val esCritico: Boolean,
    val mensaje: String,
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
    @SerializedName("id_paciente") val idPaciente: Int,
    @SerializedName("nombre_paciente") val nombrePaciente: String,
    @SerializedName("correo_paciente") val correoPaciente: String,
    @SerializedName("fecha_nacimiento") val fechaNacimiento: String? = null,
    @SerializedName("edad_paciente") val edadPaciente: Int = 68,
    @SerializedName("es_adulto_mayor") val esAdultoMayor: Boolean = true,
    @SerializedName("rango_edad") val rangoEdad: String = "adulto_mayor",
    @SerializedName("adherencia_hoy_pct") val adherenciaHoyPct: Int = 0,
    @SerializedName("tomas_completadas_hoy") val tomasCompletadasHoy: Int = 0,
    @SerializedName("tomas_totales_hoy") val tomasTotalesHoy: Int = 0,
    @SerializedName("tomas_omitidas_hoy") val tomasOmitidasHoy: Int = 0,
    @SerializedName("tomas_criticas_omitidas_hoy") val tomasCriticasOmitidasHoy: Int = 0,
    @SerializedName("alertas_activas") val alertasActivas: List<AlertaCuidadorDto> = emptyList(),
    @SerializedName("tomas_hoy") val tomasHoy: List<TomaSupervisadaItemDto> = emptyList(),
    @SerializedName("estado_riesgo") val estadoRiesgo: String = "estable"
)

data class DashboardUnificadoDto(
    val medicamentos: List<MedicamentoDto> = emptyList(),
    val tratamientos: List<TratamientoDto> = emptyList(),
    @SerializedName("recordatorios_hoy") val recordatoriosHoy: List<RecordatorioDto> = emptyList(),
    val alergias: List<AlergiaDto> = emptyList(),
    @SerializedName("contactos_apoyo") val contactosApoyo: List<ContactoApoyoDto> = emptyList(),
    val perfil: UsuarioDto? = null
)
