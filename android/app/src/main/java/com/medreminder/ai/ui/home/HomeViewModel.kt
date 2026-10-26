package com.medreminder.ai.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.medreminder.ai.data.remote.AiChatResponseDto
import com.medreminder.ai.data.remote.AlergiaDto
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.data.remote.CuidadorPanelResponseDto
import com.medreminder.ai.data.remote.MedicamentoCatalogoItemDto
import com.medreminder.ai.data.remote.MedicamentoCreateDto
import com.medreminder.ai.data.remote.MedicamentoDto
import com.medreminder.ai.data.remote.RecordatorioDto
import com.medreminder.ai.data.remote.TratamientoDto
import com.medreminder.ai.data.repository.MedRepository
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.time.Duration
import java.time.Instant
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import java.util.Locale

enum class HomeTab { HOY, MI_BOTIQUIN, SALUD_APOYO, ANALISIS_DFS }

enum class FormaFarmaceutica(
    val label: String,
    val shortLabel: String,
    val apiKey: String,
    val unitPlural: String
) {
    COMPRIMIDOS("Comprimidos / Cápsulas", "Pastilla", "comprimidos", "comprimidos"),
    GOTAS("Gotas / Jarabe", "Gotas", "gotas", "ml/gotas"),
    INYECTABLE("Inyectable / Ampolla", "Inyección", "inyectable", "dosis");

    companion object {
        fun fromString(raw: String?): FormaFarmaceutica {
            if (raw.isNullOrBlank()) return COMPRIMIDOS
            return when {
                raw.contains("gota", ignoreCase = true) ||
                    raw.contains("jarabe", ignoreCase = true) ||
                    raw.contains("ml", ignoreCase = true) -> GOTAS
                raw.contains("inyec", ignoreCase = true) ||
                    raw.contains("ampolla", ignoreCase = true) -> INYECTABLE
                else -> COMPRIMIDOS
            }
        }
    }
}

data class TomaHoyItemUi(
    val idRecordatorio: Int,
    val idTratamiento: Int,
    val idMedicamento: Int,
    val etiquetaPeriodo: String,    // TOMA MATUTINA / TOMA DE TARDE / TOMA NOCTURNA
    val horaFormateada: String,     // ej. 08:00 AM, 02:30 PM, 09:00 PM
    val nombreMedicamento: String,
    val dosisDetalle: String,       // ej. 20 mg • Con alimentos
    val instruccionesToma: String = "Tomar con abundante agua.",
    val formaFarmaceutica: FormaFarmaceutica = FormaFarmaceutica.COMPRIMIDOS,
    val colorPastilla: String = "blanco",
    val estado: String,             // pendiente, tomado, pospuesto, omitido
    val vecesPospuesto: Int,
    val permitePosponer: Boolean = true,
    val esCritico: Boolean = false,
    val contraindicaciones: String? = null,
    val minutosParaToma: Long = 0L,
    val esEnFuturoLejano: Boolean = false // true si falta > 2 horas (120 min)
)

enum class StockNivel(val label: String) {
    OPTIMO("Óptimo"),
    NORMAL("Normal"),
    BAJO("Bajo")
}

data class BotiquinItemUi(
    val idMedicamento: Int,
    val nombre: String,
    val principioActivo: String? = null,
    val dosis: String = "",
    val subtituloDosis: String,
    val stockActual: Int,
    val capacidadReferencia: Int,
    val porcentajeRestante: Int,
    val textoQuedan: String,
    val unidadTexto: String = "comprimidos",
    val formaFarmaceutica: FormaFarmaceutica = FormaFarmaceutica.COMPRIMIDOS,
    val colorPastilla: String = "blanco",
    val instruccionesToma: String? = null,
    val nivel: StockNivel,
    val permitePosponer: Boolean = true,
    val esCritico: Boolean = false,
    val contraindicaciones: String? = null
)

data class NuevoMedicamentoFormState(
    val forma: FormaFarmaceutica = FormaFarmaceutica.COMPRIMIDOS,
    val colorPastilla: String = "blanco",
    val nombre: String = "",
    val principioActivo: String = "",
    val dosis: String = "",
    val frecuenciaTexto: String = "Cada 8 horas",
    val frecuenciaHoras: Int = 8,
    val horaPrimeraToma: String = "08:00 AM",
    val duracionTratamiento: String = "Crónico / Continuo",
    val duracionDias: Int? = null,
    val instruccionesToma: String = "Con abundante agua",
    val proposito: String = "",
    val cantidadStockTexto: String = "30",
    val permitePosponer: Boolean = true,
    val esCritico: Boolean = false,
    val contraindicaciones: String = "",
    val alertaAlergia: String? = null,
    val alertaInteraccion: String? = null,
    val showConfirmacionRiesgoModal: Boolean = false,
    val catalogoSugerencias: List<MedicamentoCatalogoItemDto> = emptyList(),
    val isBuscandoCatalogo: Boolean = false,
    val nombreError: String? = null,
    val dosisError: String? = null,
    val isSubmitting: Boolean = false
)

enum class MediReactionKind { TAKEN, SNOOZED, SKIPPED }

data class MediReaction(val kind: MediReactionKind, val seq: Int)

data class EditablePrescriptionItem(
    val seleccionado: Boolean = true,
    val nombre: String,
    val principioActivo: String = "",
    val dosis: String,
    val frecuenciaHoras: Int = 8,
    val duracionDias: Int = 7,
    val instrucciones: String = "Tomar con abundante agua",
    val formaFarmaceutica: String = "comprimidos",
    val colorPastilla: String = "blanco",
    val esCritico: Boolean = false,
    val confidence: String = "high",
    val alertaAlergia: String? = null,
    val alertaInteraccion: String? = null
)

data class SeniorPenaltyModalState(
    val isCriticalAutoSent: Boolean,
    val idRecordatorio: Int,
    val medicamentoNombre: String,
    val dosisDetalle: String,
    val accionIntentada: String, // "omitir" o "posponer"
    val cuidadorNombre: String,
    val cuidadorTelefono: String,
    val mensajeAlerta: String
)

data class HomeUiState(
    val mediReaction: MediReaction? = null,
    val selectedTab: HomeTab = HomeTab.HOY,
    val showNuevoMedicamento: Boolean = false,
    val showEscaneoReceta: Boolean = false,
    val showVistaCuidador: Boolean = false,
    val analizandoRecetaIa: Boolean = false,
    val guardandoRecetaMasiva: Boolean = false,
    val medicoRecetaDetectado: String = "Médico Tratante",
    val resumenRecetaIa: String? = null,
    val modeloRecetaUsado: String = "medi-clinico",
    val itemsRecetaEditables: List<EditablePrescriptionItem> = emptyList(),
    val selectedTomaForModal: TomaHoyItemUi? = null,
    val seniorPenaltyModal: SeniorPenaltyModalState? = null,
    val cuidadorPanel: CuidadorPanelResponseDto? = null,
    val cargandoPanelCuidador: Boolean = false,
    val nombreUsuario: String = "Paciente",
    val fechaNacimiento: String = "1957-05-14",
    val edadUsuario: Int = 68,
    val esAdultoMayor: Boolean = true,
    val rangoEdad: String = "adulto_mayor",
    val rolUsuario: String = "paciente",
    val fechaEncabezado: String = "",
    val tomasHoy: List<TomaHoyItemUi> = emptyList(),
    val tomasCompletadasCount: Int = 0,
    val vecesOmitidasHoy: Int = 0,
    val tomasCriticasOmitidasHoy: Int = 0,
    val rachaDias: Int = 5,
    val escudosRacha: Int = 2,
    val puntosXp: Int = 340,
    val rangoHonor: String = "Plata",
    val progresoHonorPct: Int = 68,
    val castigoActivo: Boolean = false,
    val castigoPosponerBloqueado: Boolean = false,
    val modoTextoGrande: Boolean = false,
    val modoAltoContraste: Boolean = false,
    val botiquinItems: List<BotiquinItemUi> = emptyList(),
    val porcentajeGlobalSuministros: Int = 0,
    val diasReposicionEstimada: Int = 0,
    val alergiasUsuario: List<AlergiaDto> = emptyList(),
    val contactosApoyo: List<ContactoApoyoDto> = emptyList(),
    val isLoading: Boolean = false,
    val isActionInFlight: Boolean = false,
    val snackbarMessage: String? = null,
    val form: NuevoMedicamentoFormState = NuevoMedicamentoFormState()
)

class HomeViewModel(private val repository: MedRepository) : ViewModel() {

    private val _state = MutableStateFlow(HomeUiState(fechaEncabezado = buildFechaHoyEsp()))
    val state: StateFlow<HomeUiState> = _state.asStateFlow()

    private var searchJob: Job? = null
    private val capacidadPorMedicamento = mutableMapOf<Int, Int>()
    private val metadatosLocalesMed = mutableMapOf<Int, LocalMedMeta>()

    private data class LocalMedMeta(
        val forma: FormaFarmaceutica,
        val colorPastilla: String,
        val instruccionesToma: String,
        val stockInicial: Int
    )

    fun limpiarSesion() {
        searchJob?.cancel()
        capacidadPorMedicamento.clear()
        metadatosLocalesMed.clear()
        _state.value = HomeUiState(fechaEncabezado = buildFechaHoyEsp())
    }

    fun onToggleTextoGrande() {
        _state.update { it.copy(modoTextoGrande = !it.modoTextoGrande) }
    }

    fun onToggleAltoContraste() {
        _state.update { it.copy(modoAltoContraste = !it.modoAltoContraste) }
    }

    private var lastLoadedTime: Long = 0L

    fun onSelectTab(tab: HomeTab) {
        _state.update { it.copy(selectedTab = tab, selectedTomaForModal = null) }
        val now = System.currentTimeMillis()
        if ((tab == HomeTab.MI_BOTIQUIN || tab == HomeTab.HOY) &&
            (now - lastLoadedTime > 60_000L || _state.value.tomasHoy.isEmpty())
        ) {
            cargarDatos(silencioso = true)
        }
    }

    fun onOpenNuevoMedicamento() {
        _state.update {
            it.copy(
                showNuevoMedicamento = true,
                selectedTomaForModal = null,
                form = NuevoMedicamentoFormState()
            )
        }
    }

    fun onCloseNuevoMedicamento() {
        _state.update { it.copy(showNuevoMedicamento = false) }
    }

    fun onCerrarNuevoMedicamento() = onCloseNuevoMedicamento()

    fun onOpenConfirmacionToma(item: TomaHoyItemUi) {
        if (item.estado != "pendiente") return
        _state.update { it.copy(selectedTomaForModal = item) }
    }

    fun onDismissConfirmacionToma() {
        if (_state.value.isActionInFlight) return
        _state.update { it.copy(selectedTomaForModal = null) }
    }

    private fun nextReaction(prev: HomeUiState, kind: MediReactionKind) =
        MediReaction(kind, (prev.mediReaction?.seq ?: 0) + 1)

    fun onSnackbarShown() {
        _state.update { it.copy(snackbarMessage = null) }
    }

    // --- Acciones de Toma y Reversión (Undo) ---

    private fun applyOptimisticStatus(prev: HomeUiState, idRecordatorio: Int, nuevoEstado: String): HomeUiState {
        val updatedTomas = prev.tomasHoy.map {
            if (it.idRecordatorio == idRecordatorio) it.copy(estado = nuevoEstado) else it
        }
        val completadas = updatedTomas.count { it.estado == "tomado" }
        val omitidas = updatedTomas.count { it.estado == "omitido" }
        return prev.copy(
            tomasHoy = updatedTomas,
            tomasCompletadasCount = completadas,
            vecesOmitidasHoy = omitidas
        )
    }

    fun onTomarAhora() {
        val toma = _state.value.selectedTomaForModal ?: return
        if (_state.value.isActionInFlight) return

        // Actualización optimista inmediata (0ms latencia percibida)
        _state.update { prev ->
            applyOptimisticStatus(prev, toma.idRecordatorio, "tomado").copy(
                isActionInFlight = true,
                selectedTomaForModal = null,
                seniorPenaltyModal = null,
                snackbarMessage = if (prev.esAdultoMayor) {
                    "✓ Toma registrada a tiempo: ${toma.nombreMedicamento}"
                } else {
                    "+25 XP • Toma registrada: ${toma.nombreMedicamento}"
                },
                mediReaction = nextReaction(prev, MediReactionKind.TAKEN)
            )
        }
        viewModelScope.launch {
            val res = repository.tomarRecordatorio(toma.idRecordatorio)
            res.fold(
                onSuccess = {
                    _state.update { it.copy(isActionInFlight = false) }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { prev ->
                        applyOptimisticStatus(prev, toma.idRecordatorio, "pendiente").copy(
                            isActionInFlight = false,
                            snackbarMessage = err.message ?: "No se pudo registrar la toma"
                        )
                    }
                }
            )
        }
    }

    fun onTomarPorId(idRecordatorio: Int, nombreMedicamento: String) {
        if (_state.value.isActionInFlight) return
        _state.update { prev ->
            applyOptimisticStatus(prev, idRecordatorio, "tomado").copy(
                isActionInFlight = true,
                selectedTomaForModal = null,
                seniorPenaltyModal = null,
                snackbarMessage = "✓ Toma confirmada: $nombreMedicamento",
                mediReaction = nextReaction(prev, MediReactionKind.TAKEN)
            )
        }
        viewModelScope.launch {
            val res = repository.tomarRecordatorio(idRecordatorio)
            res.fold(
                onSuccess = {
                    _state.update { it.copy(isActionInFlight = false) }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { prev ->
                        applyOptimisticStatus(prev, idRecordatorio, "pendiente").copy(
                            isActionInFlight = false,
                            snackbarMessage = err.message ?: "No se pudo registrar la toma"
                        )
                    }
                }
            )
        }
    }

    fun onDismissSeniorPenaltyModal() {
        _state.update { it.copy(seniorPenaltyModal = null) }
    }

    /**
     * Cuando un adulto mayor (o cualquier paciente con supervisión) intenta omitir o no puede tomar
     * un medicamento CRÍTICO: se envía AUTOMÁTICAMENTE la alerta crítica al cuidador y se muestra el modal rojo.
     */
    fun onOmitirCriticoConAlertaAutomatica() {
        val toma = _state.value.selectedTomaForModal ?: return
        if (_state.value.isActionInFlight) return

        val cuidador = _state.value.contactosApoyo.firstOrNull { it.esPrincipal }
            ?: _state.value.contactosApoyo.firstOrNull()
        val nombreCuidador = cuidador?.nombreCompleto ?: "Familiar / Cuidador Principal"
        val telCuidador = cuidador?.telefono ?: ""
        val dosisLimpia = toma.dosisDetalle.substringBefore("•").trim()
        val msgCritico = "ALERTA CRÍTICA AUTOMÁTICA: ${_state.value.nombreUsuario} (${_state.value.edadUsuario} años) " +
            "no tomó su medicamento CRÍTICO ${toma.nombreMedicamento} ($dosisLimpia) de las ${toma.horaFormateada}. " +
            "Se ha enviado notificación urgente a $nombreCuidador."

        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            // 1. Registrar omisión en backend (que también registra la alerta crítica en BD)
            runCatching { repository.omitirRecordatorio(toma.idRecordatorio) }
            // 2. Disparar explícitamente alerta crítica automática al panel del cuidador
            runCatching {
                repository.dispararAlertaCuidador(
                    tipoAlerta = "critica_automatica",
                    medicamentoNombre = toma.nombreMedicamento,
                    dosis = dosisLimpia,
                    accion = "omitir",
                    esCritico = true,
                    mensaje = msgCritico
                )
            }
            _state.update {
                it.copy(
                    isActionInFlight = false,
                    selectedTomaForModal = null,
                    seniorPenaltyModal = SeniorPenaltyModalState(
                        isCriticalAutoSent = true,
                        idRecordatorio = toma.idRecordatorio,
                        medicamentoNombre = toma.nombreMedicamento,
                        dosisDetalle = dosisLimpia,
                        accionIntentada = "omitir",
                        cuidadorNombre = nombreCuidador,
                        cuidadorTelefono = telCuidador,
                        mensajeAlerta = msgCritico
                    ),
                    snackbarMessage = "🚨 Alerta crítica enviada automáticamente a $nombreCuidador",
                    mediReaction = nextReaction(it, MediReactionKind.SKIPPED)
                )
            }
            cargarDatos(silencioso = true)
            cargarPanelCuidador(silencioso = true)
        }
    }

    fun onPosponer30Min() {
        val toma = _state.value.selectedTomaForModal ?: return
        if (_state.value.isActionInFlight) return

        if (!_state.value.esAdultoMayor && _state.value.castigoPosponerBloqueado) {
            _state.update {
                it.copy(snackbarMessage = "Posponer bloqueado por bajo Honor. Cumple tus tomas a tiempo para desbloquearlo.")
            }
            return
        }

        if (!toma.permitePosponer || toma.esCritico) {
            if (_state.value.esAdultoMayor && toma.esCritico) {
                onOmitirCriticoConAlertaAutomatica()
                return
            }
            _state.update {
                it.copy(snackbarMessage = "Este medicamento es crítico y NO puede posponerse.")
            }
            return
        }

        val esSenior = _state.value.esAdultoMayor
        val cuidador = _state.value.contactosApoyo.firstOrNull { it.esPrincipal }
            ?: _state.value.contactosApoyo.firstOrNull()
        val nombreCuidador = cuidador?.nombreCompleto ?: "Familiar / Cuidador Principal"
        val telCuidador = cuidador?.telefono ?: ""
        val dosisLimpia = toma.dosisDetalle.substringBefore("•").trim()

        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            val res = repository.posponerRecordatorio(toma.idRecordatorio)
            res.fold(
                onSuccess = { updatedDto ->
                    val msg = if (esSenior) {
                        "Aviso: Se registró posposición de ${toma.nombreMedicamento}. Se notificará a $nombreCuidador."
                    } else if (updatedDto.estado == "omitido") {
                        "Límite de posposiciones alcanzado: marcado como omitido (-45 XP)"
                    } else {
                        "Pospuesto 30 minutos (${updatedDto.vecesPospuesto}/2)"
                    }

                    val penaltyModal = if (esSenior) {
                        SeniorPenaltyModalState(
                            isCriticalAutoSent = false,
                            idRecordatorio = toma.idRecordatorio,
                            medicamentoNombre = toma.nombreMedicamento,
                            dosisDetalle = dosisLimpia,
                            accionIntentada = if (updatedDto.estado == "omitido") "omitir" else "posponer",
                            cuidadorNombre = nombreCuidador,
                            cuidadorTelefono = telCuidador,
                            mensajeAlerta = "Atención ${_state.value.nombreUsuario}: Has pospuesto tu medicamento ${toma.nombreMedicamento} ($dosisLimpia). " +
                                "Por protocolo de cuidado para adulto mayor, se notificará a tu cuidador ($nombreCuidador) sobre este retraso."
                        )
                    } else null

                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            selectedTomaForModal = null,
                            seniorPenaltyModal = penaltyModal,
                            snackbarMessage = msg,
                            mediReaction = nextReaction(
                                it,
                                if (updatedDto.estado == "omitido") MediReactionKind.SKIPPED else MediReactionKind.SNOOZED
                            )
                        )
                    }
                    cargarDatos(silencioso = true)
                    if (esSenior) cargarPanelCuidador(silencioso = true)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            snackbarMessage = err.message ?: "No se pudo posponer la toma"
                        )
                    }
                }
            )
        }
    }

    fun onOmitirToma() {
        val toma = _state.value.selectedTomaForModal ?: return
        if (_state.value.isActionInFlight) return

        // Si el medicamento es crítico, dispara la alerta crítica automática al cuidador
        if (toma.esCritico) {
            onOmitirCriticoConAlertaAutomatica()
            return
        }

        val esSenior = _state.value.esAdultoMayor
        val cuidador = _state.value.contactosApoyo.firstOrNull { it.esPrincipal }
            ?: _state.value.contactosApoyo.firstOrNull()
        val nombreCuidador = cuidador?.nombreCompleto ?: "Familiar / Cuidador Principal"
        val telCuidador = cuidador?.telefono ?: ""
        val dosisLimpia = toma.dosisDetalle.substringBefore("•").trim()

        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            val res = repository.omitirRecordatorio(toma.idRecordatorio)
            res.fold(
                onSuccess = {
                    val penaltyModal = if (esSenior) {
                        SeniorPenaltyModalState(
                            isCriticalAutoSent = false,
                            idRecordatorio = toma.idRecordatorio,
                            medicamentoNombre = toma.nombreMedicamento,
                            dosisDetalle = dosisLimpia,
                            accionIntentada = "omitir",
                            cuidadorNombre = nombreCuidador,
                            cuidadorTelefono = telCuidador,
                            mensajeAlerta = "Atención ${_state.value.nombreUsuario}: Omitiste tu medicamento normal ${toma.nombreMedicamento} ($dosisLimpia). " +
                                "Se notificará a tu cuidador ($nombreCuidador) para que esté al tanto de tu tratamiento."
                        )
                    } else null

                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            selectedTomaForModal = null,
                            seniorPenaltyModal = penaltyModal,
                            snackbarMessage = if (esSenior) {
                                "⚠️ Toma omitida: se notificará a tu cuidador ($nombreCuidador)"
                            } else {
                                "Toma omitida (-45 XP • Honor penalizado)"
                            },
                            mediReaction = nextReaction(it, MediReactionKind.SKIPPED)
                        )
                    }
                    cargarDatos(silencioso = true)
                    if (esSenior) cargarPanelCuidador(silencioso = true)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            snackbarMessage = err.message ?: "No se pudo omitir la toma"
                        )
                    }
                }
            )
        }
    }

    fun onRevertirToma(idRecordatorio: Int) {
        if (_state.value.isActionInFlight) return
        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            val res = repository.revertirRecordatorio(idRecordatorio)
            res.fold(
                onSuccess = {
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            snackbarMessage = "Acción deshecha: la toma volvió a estado Pendiente"
                        )
                    }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    // Si el backend aún no expone /revertir, revertimos localmente en UI para no bloquear al paciente
                    _state.update { prev ->
                        val updatedTomas = prev.tomasHoy.map { item ->
                            if (item.idRecordatorio == idRecordatorio) item.copy(estado = "pendiente") else item
                        }
                        val completadas = updatedTomas.count { it.estado == "tomado" }
                        val omitidas = updatedTomas.count { it.estado == "omitido" }
                        prev.copy(
                            isActionInFlight = false,
                            tomasHoy = updatedTomas,
                            tomasCompletadasCount = completadas,
                            vecesOmitidasHoy = omitidas,
                            castigoActivo = omitidas > 0,
                            castigoPosponerBloqueado = omitidas > 0,
                            snackbarMessage = err.message ?: "Toma restaurada a pendiente"
                        )
                    }
                }
            )
        }
    }

    // --- Acciones de Botiquín: Recargar Caja (+30) y Eliminar Medicamento ---

    fun onRecargarStock(idMedicamento: Int, cantidadExtra: Int = 30) {
        val item = _state.value.botiquinItems.firstOrNull { it.idMedicamento == idMedicamento } ?: return
        val nuevoStock = (item.stockActual + cantidadExtra).coerceAtLeast(1)
        capacidadPorMedicamento[idMedicamento] = maxOf(item.capacidadReferencia, nuevoStock)

        val fallbackDto = MedicamentoCreateDto(
            nombre = item.nombre,
            principioActivo = item.principioActivo,
            dosis = item.dosis.ifBlank { "1 comprimido" },
            cantidadStock = nuevoStock,
            stockInicial = maxOf(item.capacidadReferencia, nuevoStock),
            formaFarmaceutica = item.formaFarmaceutica.apiKey,
            colorPastilla = item.colorPastilla,
            instruccionesToma = item.instruccionesToma,
            permitePosponer = item.permitePosponer,
            esCritico = item.esCritico,
            contraindicaciones = item.contraindicaciones
        )

        viewModelScope.launch {
            val res = repository.actualizarStockMedicamento(idMedicamento, nuevoStock, fallbackDto)
            res.fold(
                onSuccess = {
                    _state.update {
                        it.copy(snackbarMessage = "+$cantidadExtra ${item.unidadTexto} agregados a ${item.nombre}")
                    }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(snackbarMessage = err.message ?: "No se pudo actualizar el stock")
                    }
                }
            )
        }
    }

    fun onEliminarMedicamento(idMedicamento: Int) {
        val item = _state.value.botiquinItems.firstOrNull { it.idMedicamento == idMedicamento }
        viewModelScope.launch {
            val res = repository.eliminarMedicamento(idMedicamento)
            res.fold(
                onSuccess = {
                    capacidadPorMedicamento.remove(idMedicamento)
                    metadatosLocalesMed.remove(idMedicamento)
                    _state.update {
                        it.copy(snackbarMessage = "${item?.nombre ?: "Medicamento"} eliminado del botiquín")
                    }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(snackbarMessage = err.message ?: "No se pudo eliminar el medicamento")
                    }
                }
            )
        }
    }

    // --- Formulario Nuevo Medicamento & Autocompletado ---

    fun onFormaChange(forma: FormaFarmaceutica) {
        val defaultDosis = when (forma) {
            FormaFarmaceutica.COMPRIMIDOS -> if (_state.value.form.dosis.isBlank()) "1 comprimido" else _state.value.form.dosis
            FormaFarmaceutica.GOTAS -> if (_state.value.form.dosis.isBlank() || _state.value.form.dosis == "1 comprimido") "10 ml" else _state.value.form.dosis
            FormaFarmaceutica.INYECTABLE -> if (_state.value.form.dosis.isBlank() || _state.value.form.dosis == "1 comprimido") "1 ampolla" else _state.value.form.dosis
        }
        _state.update { it.copy(form = it.form.copy(forma = forma, dosis = defaultDosis)) }
    }

    fun onColorPastillaChange(color: String) {
        _state.update { it.copy(form = it.form.copy(colorPastilla = color)) }
    }

    fun onHoraPrimeraTomaChange(hora: String) {
        _state.update { it.copy(form = it.form.copy(horaPrimeraToma = hora)) }
    }

    fun onDuracionChange(etiqueta: String, dias: Int?) {
        _state.update { it.copy(form = it.form.copy(duracionTratamiento = etiqueta, duracionDias = dias)) }
    }

    fun onInstruccionesTomaChange(instruccion: String) {
        _state.update { it.copy(form = it.form.copy(instruccionesToma = instruccion)) }
    }

    fun onPropositoChange(v: String) {
        _state.update { it.copy(form = it.form.copy(proposito = v)) }
    }

    fun onDismissConfirmacionRiesgoModal() {
        _state.update { it.copy(form = it.form.copy(showConfirmacionRiesgoModal = false)) }
    }

    fun onNombreMedChange(v: String) {
        _state.update { it.copy(form = it.form.copy(nombre = v, nombreError = null)) }

        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            delay(200) // Debounce para no saturar
            if (v.isBlank()) {
                _state.update {
                    it.copy(
                        form = it.form.copy(
                            catalogoSugerencias = emptyList(),
                            alertaAlergia = null,
                            alertaInteraccion = null
                        )
                    )
                }
                return@launch
            }

            // 1. Buscar sugerencias de catálogo
            val catRes = repository.buscarCatalogo(v)
            val sugerencias = catRes.getOrDefault(emptyList())

            // 2. Verificar si hay alertas de alergia con lo que el usuario está escribiendo
            val alergiaRes = repository.verificarAlergias(nombre = v, principioActivo = _state.value.form.principioActivo)
            val alerta = alergiaRes.getOrNull()?.let { if (it.tieneConflicto) it.alerta?.cleanClinicalText() else null }

            // 3. Verificar interacciones medicamentosas con el botiquín actual
            val interaccion = evaluarInteraccionConBotiquin(v, _state.value.form.principioActivo)

            _state.update {
                it.copy(
                    form = it.form.copy(
                        catalogoSugerencias = sugerencias,
                        alertaAlergia = alerta,
                        alertaInteraccion = interaccion
                    )
                )
            }
        }
    }

    fun onSelectCatalogoSugerencia(item: MedicamentoCatalogoItemDto) {
        val formaEncontrada = FormaFarmaceutica.fromString(item.formaFarmaceutica)
        val esCritico = item.esCriticoDefecto
        val permitePosponer = !item.esCriticoDefecto
        val colorSugerido = item.colorSugerido ?: _state.value.form.colorPastilla
        val instruccionSugerida = item.instruccionesToma ?: _state.value.form.instruccionesToma
        val interaccion = evaluarInteraccionConBotiquin(item.nombre, item.principioActivo)

        _state.update {
            it.copy(
                form = it.form.copy(
                    nombre = item.nombre,
                    principioActivo = item.principioActivo,
                    dosis = item.dosisSugerida,
                    forma = formaEncontrada,
                    colorPastilla = colorSugerido,
                    instruccionesToma = instruccionSugerida,
                    contraindicaciones = item.contraindicaciones,
                    esCritico = esCritico,
                    permitePosponer = permitePosponer,
                    alertaInteraccion = interaccion,
                    catalogoSugerencias = emptyList()
                )
            )
        }

        // Validar alergias del medicamento seleccionado de inmediato
        viewModelScope.launch {
            val alergiaRes = repository.verificarAlergias(nombre = item.nombre, principioActivo = item.principioActivo)
            val alerta = alergiaRes.getOrNull()?.let { if (it.tieneConflicto) it.alerta?.cleanClinicalText() else null }
            _state.update { it.copy(form = it.form.copy(alertaAlergia = alerta)) }
        }
    }

    /**
     * Consulta en vivo al motor Ollama (`medi-clinico`) desde la mascota Medi.
     */
    suspend fun consultarMediAi(query: String, contextoPantalla: String = "Hoy"): AiChatResponseDto? {
        val nombreActual = _state.value.nombreUsuario.ifBlank { "Paciente" }
        return repository.consultarMediAi(
            query = query,
            nombreUsuario = nombreActual,
            contextoPantalla = contextoPantalla
        ).getOrNull()
    }

    /**
     * Acción del botón "Sugerencias IA" en Nuevo Medicamento:
     * - Si el usuario ya escribió un nombre de medicamento, invoca al motor Ollama `medi-clinico`
     *   (/ai/sugerir-medicamento) para autocompletar principio activo, dosis, horario, forma, color e interacciones.
     * - Si el campo está vacío, despliega las sugerencias principales del catálogo farmacológico.
     */
    fun onSolicitarSugerenciasIa() {
        val nombreActual = _state.value.form.nombre.trim()
        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            _state.update { it.copy(form = it.form.copy(isBuscandoCatalogo = true)) }
            if (nombreActual.isBlank()) {
                val catRes = repository.buscarCatalogo(null)
                val lista = catRes.getOrDefault(emptyList())
                _state.update {
                    it.copy(
                        form = it.form.copy(
                            catalogoSugerencias = lista,
                            isBuscandoCatalogo = false
                        ),
                        snackbarMessage = if (lista.isNotEmpty()) {
                            "Sugerencias IA: selecciona un medicamento o escribe su nombre"
                        } else {
                            "Escribe el nombre del medicamento para autocompletar con IA"
                        }
                    )
                }
                return@launch
            }

            val aiRes = repository.sugerirMedicamentoAi(nombreActual).getOrNull()
            if (aiRes != null) {
                val formaEncontrada = FormaFarmaceutica.fromString(aiRes.formaFarmaceutica)
                val esCritico = aiRes.esCriticoDefecto
                val permitePosponer = !esCritico
                val freqHoras = aiRes.frecuenciaHorasSugerida.coerceIn(4, 24)
                val freqLabel = when (freqHoras) {
                    6 -> "Cada 6 horas"
                    8 -> "Cada 8 horas"
                    12 -> "Cada 12 horas"
                    24 -> "1 vez al día"
                    else -> "Cada $freqHoras horas"
                }
                val interaccionLocal = evaluarInteraccionConBotiquin(aiRes.nombre, aiRes.principioActivo)
                _state.update {
                    it.copy(
                        form = it.form.copy(
                            nombre = aiRes.nombre,
                            principioActivo = aiRes.principioActivo,
                            dosis = aiRes.dosisSugerida,
                            frecuenciaHoras = freqHoras,
                            frecuenciaTexto = freqLabel,
                            forma = formaEncontrada,
                            colorPastilla = aiRes.colorSugerido.ifBlank { it.form.colorPastilla },
                            instruccionesToma = aiRes.instruccionesToma.ifBlank { it.form.instruccionesToma },
                            contraindicaciones = aiRes.contraindicaciones,
                            esCritico = esCritico,
                            permitePosponer = permitePosponer,
                            alertaAlergia = aiRes.alertaAlergia?.cleanClinicalText(),
                            alertaInteraccion = (aiRes.alertaInteraccion ?: interaccionLocal)?.cleanClinicalText(),
                            catalogoSugerencias = emptyList(),
                            isBuscandoCatalogo = false,
                            nombreError = null,
                            dosisError = null
                        ),
                        snackbarMessage = "IA (${aiRes.modelUsed}): ficha de ${aiRes.nombre} autocompletada"
                    )
                }
            } else {
                val catRes = repository.buscarCatalogo(nombreActual)
                val sugerencias = catRes.getOrDefault(emptyList())
                if (sugerencias.isNotEmpty()) {
                    onSelectCatalogoSugerencia(sugerencias.first())
                    _state.update {
                        it.copy(
                            form = it.form.copy(isBuscandoCatalogo = false),
                            snackbarMessage = "Ficha clínica autocompletada para ${sugerencias.first().nombre}"
                        )
                    }
                } else {
                    _state.update {
                        it.copy(
                            form = it.form.copy(isBuscandoCatalogo = false),
                            snackbarMessage = "Completa la dosis manualmente para '$nombreActual'"
                        )
                    }
                }
            }
        }
    }

    private fun evaluarInteraccionConBotiquin(nombreNuevo: String, principioNuevo: String?): String? {
        val textoNuevo = "${nombreNuevo.lowercase()} ${(principioNuevo ?: "").lowercase()}"
        val actuales = _state.value.botiquinItems
        if (actuales.isEmpty()) return null

        // Duplicidad de medicamento o principio activo
        val duplicado = actuales.firstOrNull {
            it.nombre.equals(nombreNuevo.trim(), ignoreCase = true) ||
                (!principioNuevo.isNullOrBlank() && it.principioActivo?.equals(principioNuevo.trim(), ignoreCase = true) == true)
        }
        if (duplicado != null) {
            return "Duplicidad terapéutica: '${duplicado.nombre}' ya está activo en tu botiquín con el mismo principio activo."
        }

        // Interacción AINEs (Ibuprofeno, Naproxeno, Aspirina, Ketorolaco) con Antihipertensivos / Anticoagulantes
        val esAine = listOf("ibuprofeno", "naproxeno", "aspirina", "ketorolaco", "diclofenaco", "meloxicam").any { textoNuevo.contains(it) }
        val tieneAntihipertensivoOAnticoagulante = actuales.firstOrNull { med ->
            val t = "${med.nombre.lowercase()} ${(med.principioActivo ?: "").lowercase()}"
            listOf("losartan", "losartán", "enalapril", "warfarina", "acenocumarol", "clopidogrel", "rivaroxaban", "aspirina").any { t.contains(it) }
        }
        if (esAine && tieneAntihipertensivoOAnticoagulante != null) {
            return "Posible interacción farmacológica con '${tieneAntihipertensivoOAnticoagulante.nombre}': los AINEs pueden reducir el efecto antihipertensivo o aumentar el riesgo gástrico/hemorrágico."
        }
        return null
    }

    fun onDosisMedChange(v: String) {
        _state.update { it.copy(form = it.form.copy(dosis = v, dosisError = null)) }
    }

    fun onPrincipioActivoChange(v: String) {
        _state.update { it.copy(form = it.form.copy(principioActivo = v)) }
    }

    fun onContraindicacionesChange(v: String) {
        _state.update { it.copy(form = it.form.copy(contraindicaciones = v)) }
    }

    fun onTogglePermitePosponer(permite: Boolean) {
        _state.update {
            it.copy(
                form = it.form.copy(
                    permitePosponer = permite,
                    esCritico = if (!permite) true else it.form.esCritico
                )
            )
        }
    }

    fun onToggleEsCritico(critico: Boolean) {
        _state.update {
            it.copy(
                form = it.form.copy(
                    esCritico = critico,
                    permitePosponer = if (critico) false else it.form.permitePosponer
                )
            )
        }
    }

    fun onFrecuenciaTextoChange(v: String) {
        val digits = v.filter { it.isDigit() }.toIntOrNull()
        val freq = when {
            v.contains("1 vez", ignoreCase = true) -> 24
            digits != null && digits in 1..168 -> digits
            else -> _state.value.form.frecuenciaHoras
        }
        _state.update { it.copy(form = it.form.copy(frecuenciaTexto = v, frecuenciaHoras = freq)) }
    }

    fun onSelectFrecuenciaChip(horas: Int, etiqueta: String) {
        _state.update {
            it.copy(form = it.form.copy(frecuenciaHoras = horas, frecuenciaTexto = etiqueta))
        }
    }

    fun onStockTextoChange(v: String) {
        val filtered = v.filter { it.isDigit() }
        _state.update { it.copy(form = it.form.copy(cantidadStockTexto = filtered)) }
    }

    fun onIncrementStock(delta: Int) {
        val current = _state.value.form.cantidadStockTexto.toIntOrNull() ?: 0
        val next = (current + delta).coerceAtLeast(0)
        _state.update { it.copy(form = it.form.copy(cantidadStockTexto = next.toString())) }
    }

    fun onGuardarMedicamento(forzarConRiesgo: Boolean = false) {
        val f = _state.value.form
        if (f.isSubmitting) return

        val nombreErr = if (f.nombre.isBlank()) "Ingresa el nombre del medicamento" else null
        val dosisDefault = when (f.forma) {
            FormaFarmaceutica.COMPRIMIDOS -> "1 comprimido"
            FormaFarmaceutica.GOTAS -> "10 ml"
            FormaFarmaceutica.INYECTABLE -> "1 ampolla"
        }
        val dosisReal = f.dosis.ifBlank { dosisDefault }
        if (nombreErr != null) {
            _state.update { it.copy(form = f.copy(nombreError = nombreErr)) }
            return
        }

        // Si existe alerta de alergia o interacción farmacológica y el usuario aún no la confirmó explícitamente:
        if (!forzarConRiesgo && (f.alertaAlergia != null || f.alertaInteraccion != null)) {
            _state.update { it.copy(form = f.copy(showConfirmacionRiesgoModal = true)) }
            return
        }

        val stock = f.cantidadStockTexto.toIntOrNull()?.coerceAtLeast(0) ?: 30
        val freqHoras = f.frecuenciaHoras.coerceIn(1, 168)
        val (fechaInicioIso, fechaFinIso) = calcularFechasTratamientoUtc(f.horaPrimeraToma, f.duracionDias)

        _state.update { it.copy(form = f.copy(isSubmitting = true, showConfirmacionRiesgoModal = false)) }
        viewModelScope.launch {
            val res = repository.registrarMedicamentoConTratamiento(
                nombre = f.nombre,
                principioActivo = f.principioActivo,
                dosis = dosisReal,
                frecuenciaHoras = freqHoras,
                cantidadStock = stock,
                permitePosponer = f.permitePosponer,
                esCritico = f.esCritico,
                contraindicaciones = f.contraindicaciones,
                formaFarmaceutica = f.forma.apiKey,
                colorPastilla = f.colorPastilla,
                instruccionesToma = f.instruccionesToma,
                proposito = f.proposito,
                fechaInicio = fechaInicioIso,
                fechaFin = fechaFinIso
            )
            res.fold(
                onSuccess = { medCreado ->
                    capacidadPorMedicamento[medCreado.idMedicamento] = maxOf(stock, 1)
                    metadatosLocalesMed[medCreado.idMedicamento] = LocalMedMeta(
                        forma = f.forma,
                        colorPastilla = f.colorPastilla,
                        instruccionesToma = f.instruccionesToma,
                        stockInicial = stock
                    )
                    _state.update {
                        it.copy(
                            showNuevoMedicamento = false,
                            form = NuevoMedicamentoFormState(),
                            snackbarMessage = "${medCreado.nombre} registrado con éxito"
                        )
                    }
                    cargarDatos(silencioso = false)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(
                            form = it.form.copy(isSubmitting = false),
                            snackbarMessage = err.message ?: "Error al guardar medicamento"
                        )
                    }
                }
            )
        }
    }

    private fun calcularFechasTratamientoUtc(horaPrimeraToma: String, duracionDias: Int?): Pair<String?, String?> {
        return runCatching {
            val zone = ZoneId.systemDefault()
            val hoy = LocalDate.now(zone)
            val ldtLocal = when (horaPrimeraToma) {
                "08:00 AM" -> hoy.atTime(8, 0)
                "02:00 PM" -> hoy.atTime(14, 0)
                "09:00 PM" -> hoy.atTime(21, 0)
                else -> LocalDateTime.now(zone)
            }
            val inicioUtc = ldtLocal.atZone(zone).withZoneSameInstant(ZoneOffset.UTC).toLocalDateTime()
            val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss")
            val inicioStr = inicioUtc.format(fmt)
            val finStr = duracionDias?.let { inicioUtc.plusDays(it.toLong()).format(fmt) }
            inicioStr to finStr
        }.getOrDefault(null to null)
    }

    // --- Operaciones de Alergias ---

    fun onAgregarAlergia(sustancia: String, severidad: String, reaccion: String?) {
        if (sustancia.isBlank()) return
        viewModelScope.launch {
            val res = repository.agregarAlergia(sustancia, severidad, reaccion)
            res.fold(
                onSuccess = { dto ->
                    _state.update { it.copy(snackbarMessage = "Alergia a '${dto.sustancia}' agregada") }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { it.copy(snackbarMessage = err.message ?: "No se pudo registrar la alergia") }
                }
            )
        }
    }

    fun onEliminarAlergia(idAlergia: Int) {
        viewModelScope.launch {
            val res = repository.eliminarAlergia(idAlergia)
            res.fold(
                onSuccess = {
                    _state.update { it.copy(snackbarMessage = "Alergia eliminada") }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { it.copy(snackbarMessage = err.message ?: "No se pudo eliminar") }
                }
            )
        }
    }

    // --- Operaciones de Contacto de Apoyo ---

    fun onGuardarContacto(
        idContacto: Int?,
        nombre: String,
        telefono: String,
        parentesco: String,
        correo: String?,
        esPrincipal: Boolean
    ) {
        if (nombre.isBlank() || telefono.isBlank()) return
        viewModelScope.launch {
            val res = repository.guardarContacto(
                idContacto = idContacto,
                nombre = nombre,
                telefono = telefono,
                parentesco = parentesco,
                correo = correo,
                esPrincipal = esPrincipal
            )
            res.fold(
                onSuccess = {
                    _state.update { it.copy(snackbarMessage = "Contacto de apoyo guardado") }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { it.copy(snackbarMessage = err.message ?: "No se pudo guardar contacto") }
                }
            )
        }
    }

    fun onEliminarContacto(idContacto: Int) {
        viewModelScope.launch {
            val res = repository.eliminarContacto(idContacto)
            res.fold(
                onSuccess = {
                    _state.update { it.copy(snackbarMessage = "Contacto eliminado") }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { it.copy(snackbarMessage = err.message ?: "No se pudo eliminar") }
                }
            )
        }
    }

    // --- Escaneo y Confirmación de Receta Médica con Ollama (`medi-clinico`) ---

    fun onOpenEscaneoReceta() {
        _state.update {
            it.copy(
                showEscaneoReceta = true,
                analizandoRecetaIa = false,
                guardandoRecetaMasiva = false
            )
        }
    }

    fun onCloseEscaneoReceta() {
        _state.update {
            it.copy(
                showEscaneoReceta = false,
                analizandoRecetaIa = false,
                guardandoRecetaMasiva = false
            )
        }
    }

    fun onAnalizarRecetaIa(textoReceta: String?, imageBase64: String? = null) {
        if (textoReceta.isNullOrBlank() && imageBase64.isNullOrBlank()) {
            _state.update { it.copy(snackbarMessage = "Ingresa o selecciona una receta médica para analizar") }
            return
        }
        _state.update {
            it.copy(
                analizandoRecetaIa = true,
                snackbarMessage = "Analizando receta médica con motor Ollama (medi-clinico)..."
            )
        }
        viewModelScope.launch {
            val res = repository.analizarRecetaAi(
                textoReceta = textoReceta,
                imageBase64 = imageBase64
            )
            res.fold(
                onSuccess = { scan ->
                    val editables = scan.medicamentos.map { item ->
                        EditablePrescriptionItem(
                            // Si tiene conflicto de alergia cruzada (Regla 1), lo desmarcamos preventivamente
                            seleccionado = item.alertaAlergia.isNullOrBlank(),
                            nombre = item.name,
                            principioActivo = item.principioActivo,
                            dosis = item.dosage,
                            frecuenciaHoras = item.frequencyHours,
                            duracionDias = item.durationDays,
                            instrucciones = item.instructions,
                            formaFarmaceutica = item.formaFarmaceutica,
                            colorPastilla = item.colorSugerido,
                            esCritico = item.esCritico,
                            confidence = item.confidence,
                            alertaAlergia = item.alertaAlergia,
                            alertaInteraccion = item.alertaInteraccion
                        )
                    }
                    _state.update {
                        it.copy(
                            analizandoRecetaIa = false,
                            medicoRecetaDetectado = scan.medico,
                            resumenRecetaIa = scan.resumenClinico,
                            modeloRecetaUsado = scan.modelUsed,
                            itemsRecetaEditables = editables,
                            snackbarMessage = "Receta analizada por ${scan.modelUsed}"
                        )
                    }
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(
                            analizandoRecetaIa = false,
                            snackbarMessage = err.message ?: "No se pudo analizar la receta médica"
                        )
                    }
                }
            )
        }
    }

    fun onActualizarItemReceta(index: Int, updated: EditablePrescriptionItem) {
        _state.update { prev ->
            if (index !in prev.itemsRecetaEditables.indices) return@update prev
            val nuevaLista = prev.itemsRecetaEditables.toMutableList()
            nuevaLista[index] = updated
            prev.copy(itemsRecetaEditables = nuevaLista)
        }
    }

    fun onConfirmarYGuardarReceta() {
        val seleccionados = _state.value.itemsRecetaEditables.filter { it.seleccionado && it.nombre.isNotBlank() }
        if (seleccionados.isEmpty()) {
            _state.update { it.copy(snackbarMessage = "Selecciona al menos un medicamento de la receta para guardar") }
            return
        }
        _state.update { it.copy(guardandoRecetaMasiva = true) }
        viewModelScope.launch {
            val zoneLocal = ZoneId.systemDefault()
            val ahora = LocalDateTime.now(zoneLocal)
            val inicioUtc = ahora.atZone(zoneLocal).withZoneSameInstant(ZoneOffset.UTC)
                .toLocalDateTime().withNano(0).toString()

            var guardados = 0
            for (med in seleccionados) {
                val tomasPorDia = (24 / med.frecuenciaHoras.coerceAtLeast(1)).coerceAtLeast(1)
                val stockCalculado = (tomasPorDia * med.duracionDias.coerceAtLeast(1)).coerceIn(10, 120)
                val finUtc = ahora.plusDays(med.duracionDias.toLong().coerceAtLeast(1L))
                    .atZone(zoneLocal).withZoneSameInstant(ZoneOffset.UTC)
                    .toLocalDateTime().withNano(0).toString()

                val res = repository.registrarMedicamentoConTratamiento(
                    nombre = med.nombre,
                    principioActivo = med.principioActivo.ifBlank { null },
                    dosis = med.dosis.ifBlank { "1 comprimido" },
                    frecuenciaHoras = med.frecuenciaHoras,
                    cantidadStock = stockCalculado,
                    permitePosponer = !med.esCritico,
                    esCritico = med.esCritico,
                    contraindicaciones = null,
                    formaFarmaceutica = med.formaFarmaceutica,
                    colorPastilla = med.colorPastilla,
                    instruccionesToma = med.instrucciones,
                    proposito = "Receta médica (${_state.value.medicoRecetaDetectado})",
                    fechaInicio = inicioUtc,
                    fechaFin = finUtc
                )
                if (res.isSuccess) {
                    guardados++
                }
            }

            _state.update {
                it.copy(
                    guardandoRecetaMasiva = false,
                    showEscaneoReceta = false,
                    showNuevoMedicamento = false,
                    itemsRecetaEditables = emptyList(),
                    resumenRecetaIa = null,
                    snackbarMessage = "Se registraron $guardados medicamento(s) de tu receta en Mi Botiquín"
                )
            }
            cargarDatos(silencioso = false)
        }
    }

    // --- Vista del Cuidador y Cambio de Rango Etario en Vivo ---

    fun onOpenVistaCuidador() {
        _state.update { it.copy(showVistaCuidador = true) }
        cargarPanelCuidador(silencioso = false)
    }

    fun onCloseVistaCuidador() {
        _state.update { it.copy(showVistaCuidador = false) }
    }

    fun cargarPanelCuidador(silencioso: Boolean = true) {
        if (!silencioso) {
            _state.update { it.copy(cargandoPanelCuidador = true) }
        }
        viewModelScope.launch {
            val zoneLocal = ZoneId.systemDefault()
            val tzOffsetMinutes = zoneLocal.rules.getOffset(Instant.now()).totalSeconds / 60
            val res = repository.obtenerPanelCuidador(tzOffsetMinutes = tzOffsetMinutes)
            res.fold(
                onSuccess = { panel ->
                    _state.update {
                        it.copy(
                            cargandoPanelCuidador = false,
                            cuidadorPanel = panel
                        )
                    }
                },
                onFailure = {
                    _state.update { it.copy(cargandoPanelCuidador = false) }
                }
            )
        }
    }

    fun onAtenderAlertaCuidador(idAlerta: Int) {
        viewModelScope.launch {
            val res = repository.marcarAlertaCuidadorAtendida(idAlerta)
            res.fold(
                onSuccess = {
                    _state.update { it.copy(snackbarMessage = "✓ Alerta marcada como atendida por el cuidador") }
                    cargarPanelCuidador(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { it.copy(snackbarMessage = err.message ?: "No se pudo actualizar la alerta") }
                }
            )
        }
    }

    fun onSimularAlertaCriticaCuidador() {
        val medCritico = _state.value.tomasHoy.firstOrNull { it.esCritico }
            ?: _state.value.tomasHoy.firstOrNull()
        val nombreMed = medCritico?.nombreMedicamento ?: "Insulina Glargina / Losartán"
        val dosisMed = medCritico?.dosisDetalle?.substringBefore("•")?.trim() ?: "50 mg"
        val cuidador = _state.value.contactosApoyo.firstOrNull { it.esPrincipal }
            ?: _state.value.contactosApoyo.firstOrNull()
        val nombreCuidador = cuidador?.nombreCompleto ?: "Cuidador Principal"
        val telCuidador = cuidador?.telefono ?: ""
        val mensaje = "ALERTA CRÍTICA AUTOMÁTICA: ${_state.value.nombreUsuario} (${_state.value.edadUsuario} años) " +
            "omitió la toma crítica de $nombreMed ($dosisMed). Se requiere verificación inmediata por parte de $nombreCuidador."

        viewModelScope.launch {
            val res = repository.dispararAlertaCuidador(
                tipoAlerta = "critica_automatica",
                medicamentoNombre = nombreMed,
                dosis = dosisMed,
                accion = "omitir",
                esCritico = true,
                mensaje = mensaje
            )
            res.fold(
                onSuccess = {
                    _state.update {
                        it.copy(
                            seniorPenaltyModal = SeniorPenaltyModalState(
                                isCriticalAutoSent = true,
                                idRecordatorio = medCritico?.idRecordatorio ?: 0,
                                medicamentoNombre = nombreMed,
                                dosisDetalle = dosisMed,
                                accionIntentada = "omitir",
                                cuidadorNombre = nombreCuidador,
                                cuidadorTelefono = telCuidador,
                                mensajeAlerta = mensaje
                            ),
                            snackbarMessage = "🚨 Alerta crítica enviada automáticamente al cuidador"
                        )
                    }
                    cargarPanelCuidador(silencioso = true)
                },
                onFailure = { err ->
                    _state.update { it.copy(snackbarMessage = err.message ?: "Error al enviar alerta") }
                }
            )
        }
    }

    fun onCambiarRangoEdadDemo(esAdultoMayorTarget: Boolean) {
        val nuevaFecha = if (esAdultoMayorTarget) "1957-05-14" else "1998-08-20"
        viewModelScope.launch {
            val res = repository.actualizarPerfilEdad(fechaNacimiento = nuevaFecha)
            res.fold(
                onSuccess = { perfilActualizado ->
                    _state.update {
                        it.copy(
                            fechaNacimiento = perfilActualizado.fechaNacimiento ?: nuevaFecha,
                            edadUsuario = perfilActualizado.edad,
                            esAdultoMayor = perfilActualizado.esAdultoMayor,
                            rangoEdad = perfilActualizado.rangoEdad,
                            snackbarMessage = if (perfilActualizado.esAdultoMayor) {
                                "Perfil actualizado: Adulto Mayor (${perfilActualizado.edad} años) • Supervisión de Cuidador Activa"
                            } else {
                                "Perfil actualizado: Joven/Adulto (${perfilActualizado.edad} años) • Racha y Penalización de Honor Activos"
                            }
                        )
                    }
                    cargarDatos(silencioso = true)
                },
                onFailure = {
                    // Fallback local inmediato
                    _state.update {
                        it.copy(
                            fechaNacimiento = nuevaFecha,
                            edadUsuario = if (esAdultoMayorTarget) 69 else 28,
                            esAdultoMayor = esAdultoMayorTarget,
                            rangoEdad = if (esAdultoMayorTarget) "adulto_mayor" else "joven",
                            snackbarMessage = if (esAdultoMayorTarget) {
                                "Modo Adulto Mayor (69 años) activado"
                            } else {
                                "Modo Joven/Adulto (28 años • Racha y Honor) activado"
                            }
                        )
                    }
                }
            )
        }
    }

    // --- Carga y mapeo de datos desde el Backend ---

    fun cargarDatos(silencioso: Boolean = false) {
        lastLoadedTime = System.currentTimeMillis()
        if (!silencioso) {
            _state.update { it.copy(isLoading = true) }
        }
        viewModelScope.launch {
            val zoneLocal = ZoneId.systemDefault()
            val hoyLocal = LocalDate.now(zoneLocal).toString()
            val tzOffsetMinutes = zoneLocal.rules.getOffset(Instant.now()).totalSeconds / 60

            val res = repository.cargarDashboard(
                fechaUtc = hoyLocal,
                tzOffsetMinutes = tzOffsetMinutes
            )
            res.fold(
                onSuccess = { bundle ->
                    val tomasUi = mapRecordatoriosToUi(
                        recordatorios = bundle.recordatoriosHoy,
                        tratamientos = bundle.tratamientos,
                        medicamentos = bundle.medicamentos
                    )
                    val botiquinUi = mapMedicamentosToBotiquinUi(bundle.medicamentos)
                    val completadas = tomasUi.count { it.estado == "tomado" }
                    val omitidas = tomasUi.count { it.estado == "omitido" }
                    val criticasOmitidas = tomasUi.count { it.estado == "omitido" && it.esCritico }

                    // Estado de Botiquín vacío: 0% y 0 días (nunca 100% ni 6 días cuando no hay medicamentos)
                    val promedioGlobal = if (botiquinUi.isEmpty()) 0 else {
                        botiquinUi.map { it.porcentajeRestante }.average().toInt().coerceIn(0, 100)
                    }
                    val diasReposicion = if (botiquinUi.isEmpty()) {
                        0
                    } else {
                        bundle.medicamentos.mapNotNull { med ->
                            val trat = bundle.tratamientos.firstOrNull {
                                it.idMedicamento == med.idMedicamento && it.estado == "activo"
                            }
                            if (trat != null && trat.frecuenciaHoras > 0) {
                                (med.cantidadStock * trat.frecuenciaHoras) / 24
                            } else {
                                med.cantidadStock
                            }
                        }.minOrNull() ?: 0
                    }

                    // Cálculo de Racha estilo TikTok, Escudos y Rango de Honor
                    val baseXp = 320 + (completadas * 30) - (omitidas * 55)
                    val xpActual = baseXp.coerceAtLeast(40)
                    val (rangoNombre, progresoPct) = calcularRangoHonor(xpActual)
                    val rachaCalculada = when {
                        omitidas > 0 -> 0 // Racha apagada por omisión no protegida
                        completadas > 0 -> 7 + completadas // Evoluciona a fuego azul eléctrico
                        else -> 5
                    }
                    val escudosDisp = if (omitidas > 0) 1 else 2
                    val castigoActivo = omitidas > 0 || xpActual < 200

                    val perfil = bundle.perfil
                    val edadActual = perfil?.edad ?: _state.value.edadUsuario
                    val esSenior = perfil?.esAdultoMayor ?: (edadActual >= 60)
                    val rangoActual = perfil?.rangoEdad ?: if (esSenior) "adulto_mayor" else "joven"
                    val fechaNac = perfil?.fechaNacimiento ?: _state.value.fechaNacimiento
                    val rolActual = perfil?.rol ?: _state.value.rolUsuario

                    _state.update { prev ->
                        prev.copy(
                            isLoading = false,
                            nombreUsuario = bundle.nombreUsuario?.takeIf { it.isNotBlank() } ?: prev.nombreUsuario,
                            fechaNacimiento = fechaNac,
                            edadUsuario = edadActual,
                            esAdultoMayor = esSenior,
                            rangoEdad = rangoActual,
                            rolUsuario = rolActual,
                            fechaEncabezado = buildFechaHoyEsp(),
                            tomasHoy = tomasUi,
                            tomasCompletadasCount = completadas,
                            vecesOmitidasHoy = omitidas,
                            tomasCriticasOmitidasHoy = criticasOmitidas,
                            rachaDias = rachaCalculada,
                            escudosRacha = escudosDisp,
                            puntosXp = xpActual,
                            rangoHonor = rangoNombre,
                            progresoHonorPct = progresoPct,
                            castigoActivo = castigoActivo,
                            castigoPosponerBloqueado = castigoActivo,
                            botiquinItems = botiquinUi,
                            porcentajeGlobalSuministros = promedioGlobal,
                            diasReposicionEstimada = diasReposicion,
                            alergiasUsuario = bundle.alergias,
                            contactosApoyo = bundle.contactosApoyo
                        )
                    }
                    cargarPanelCuidador(silencioso = true)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(
                            isLoading = false,
                            snackbarMessage = err.message
                        )
                    }
                }
            )
        }
    }

    private fun calcularRangoHonor(xp: Int): Pair<String, Int> {
        return when {
            xp < 200 -> "Hierro" to ((xp.coerceAtLeast(0) * 100) / 200).coerceIn(5, 100)
            xp < 300 -> "Bronce" to (((xp - 200) * 100) / 100).coerceIn(5, 100)
            xp < 450 -> "Plata" to (((xp - 300) * 100) / 150).coerceIn(5, 100)
            xp < 650 -> "Oro" to (((xp - 450) * 100) / 200).coerceIn(5, 100)
            else -> "Diamante" to 100
        }
    }

    private fun mapRecordatoriosToUi(
        recordatorios: List<RecordatorioDto>,
        tratamientos: List<TratamientoDto>,
        medicamentos: List<MedicamentoDto>
    ): List<TomaHoyItemUi> {
        val tratById = tratamientos.associateBy { it.idTratamiento }
        val medById = medicamentos.associateBy { it.idMedicamento }
        val zoneLocal = ZoneId.systemDefault()
        val ahoraLocal = LocalDateTime.now(zoneLocal)

        return recordatorios.mapNotNull { rec ->
            val trat = tratById[rec.idTratamiento]
            val med = trat?.let { medById[it.idMedicamento] }
            val idMed = med?.idMedicamento ?: 0
            val localMeta = metadatosLocalesMed[idMed]

            val nombreMed = rec.nombreMedicamento ?: med?.nombre ?: "Medicamento #${rec.idTratamiento}"
            val dosisMed = rec.dosis ?: med?.dosis ?: "1 dosis"

            val localDateTime = parseUtcToLocal(rec.horaProgramada, zoneLocal)
            val hour = localDateTime.hour
            val minute = localDateTime.minute

            val periodo = when {
                hour < 12 -> "TOMA MATUTINA"
                hour < 19 -> "TOMA DE TARDE"
                else -> "TOMA NOCTURNA"
            }

            // Formato 12h real (ej. 14:30 -> 02:30 PM, 00:15 -> 12:15 AM)
            val hour12 = if (hour % 12 == 0) 12 else hour % 12
            val sufijo = if (hour < 12) "AM" else "PM"
            val horaStr = String.format(Locale.US, "%02d:%02d %s", hour12, minute, sufijo)

            val formaReal = FormaFarmaceutica.fromString(
                rec.formaFarmaceutica ?: med?.formaFarmaceutica ?: localMeta?.forma?.apiKey ?: dosisMed
            )
            val colorReal = (rec.colorPastilla ?: med?.colorPastilla ?: localMeta?.colorPastilla ?: "blanco").lowercase()
            val instruccionReal = (rec.instruccionesToma ?: med?.instruccionesToma ?: localMeta?.instruccionesToma)
                ?.takeIf { it.isNotBlank() }
                ?: formaReal.label

            val minutosParaToma = Duration.between(ahoraLocal, localDateTime).toMinutes()

            TomaHoyItemUi(
                idRecordatorio = rec.idRecordatorio,
                idTratamiento = rec.idTratamiento,
                idMedicamento = idMed,
                etiquetaPeriodo = periodo,
                horaFormateada = horaStr,
                nombreMedicamento = nombreMed,
                dosisDetalle = "$dosisMed • $instruccionReal",
                instruccionesToma = instruccionReal,
                formaFarmaceutica = formaReal,
                colorPastilla = colorReal,
                estado = rec.estado,
                vecesPospuesto = rec.vecesPospuesto,
                permitePosponer = rec.permitePosponer && (med?.permitePosponer != false),
                esCritico = rec.esCritico || (med?.esCritico == true),
                contraindicaciones = med?.contraindicaciones,
                minutosParaToma = minutosParaToma,
                esEnFuturoLejano = minutosParaToma > 120L
            )
        }
    }

    private fun mapMedicamentosToBotiquinUi(medicamentos: List<MedicamentoDto>): List<BotiquinItemUi> {
        return medicamentos.map { med ->
            val stock = med.cantidadStock
            val localMeta = metadatosLocalesMed[med.idMedicamento]
            val stockInicialDto = med.stockInicial ?: localMeta?.stockInicial
            val prevCap = capacidadPorMedicamento[med.idMedicamento]

            val capacidadRef = when {
                stockInicialDto != null && stockInicialDto >= stock && stockInicialDto > 0 -> stockInicialDto
                prevCap != null && prevCap >= stock -> prevCap
                stock > 30 -> ((stock + 9) / 10) * 10
                stock in 21..30 -> 30
                stock in 15..20 -> 20
                stock in 1..14 -> 20
                else -> 30
            }
            capacidadPorMedicamento[med.idMedicamento] = maxOf(
                capacidadPorMedicamento[med.idMedicamento] ?: 0,
                capacidadRef,
                stock
            )

            val pct = if (capacidadRef > 0) {
                ((stock.toFloat() / capacidadRef.toFloat()) * 100f).toInt().coerceIn(0, 100)
            } else 0

            val nivel = when {
                pct <= 25 || stock <= 5 -> StockNivel.BAJO
                pct >= 85 -> StockNivel.OPTIMO
                else -> StockNivel.NORMAL
            }

            val formaReal = FormaFarmaceutica.fromString(
                med.formaFarmaceutica ?: localMeta?.forma?.apiKey ?: med.dosis
            )
            val unidad = formaReal.unitPlural
            val colorReal = (med.colorPastilla ?: localMeta?.colorPastilla ?: "blanco").lowercase()
            val instruccionReal = med.instruccionesToma ?: localMeta?.instruccionesToma

            BotiquinItemUi(
                idMedicamento = med.idMedicamento,
                nombre = med.nombre,
                principioActivo = med.principioActivo,
                dosis = med.dosis,
                subtituloDosis = "${med.dosis} • Envase de $capacidadRef $unidad",
                stockActual = stock,
                capacidadReferencia = capacidadRef,
                porcentajeRestante = pct,
                textoQuedan = "Quedan $stock $unidad",
                unidadTexto = unidad,
                formaFarmaceutica = formaReal,
                colorPastilla = colorReal,
                instruccionesToma = instruccionReal,
                nivel = nivel,
                permitePosponer = med.permitePosponer,
                esCritico = med.esCritico,
                contraindicaciones = med.contraindicaciones
            )
        }
    }

    private fun parseUtcToLocal(isoUtc: String, targetZone: ZoneId): LocalDateTime {
        return runCatching {
            val clean = isoUtc.removeSuffix("Z").substringBefore("+")
            val ldtUtc = LocalDateTime.parse(clean)
            ldtUtc.atZone(ZoneOffset.UTC).withZoneSameInstant(targetZone).toLocalDateTime()
        }.getOrElse {
            LocalDateTime.now()
        }
    }

    private fun buildFechaHoyEsp(): String {
        val hoy = LocalDate.now(ZoneId.systemDefault())
        val esLocale = Locale.forLanguageTag("es-ES")
        val formatter = DateTimeFormatter.ofPattern("EEEE, d 'de' MMM", esLocale)
        val raw = hoy.format(formatter)
        return raw.replaceFirstChar { if (it.isLowerCase()) it.titlecase(esLocale) else it.toString() }
    }

    private fun String.cleanClinicalText(): String {
        return this.replace(Regex("[\\p{So}\\p{Cn}\\u2600-\\u27BF\\uD83C-\\uDBFF\\uDC00-\\uDFFF]"), "").trim()
    }

    class Factory(private val repository: MedRepository) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T = HomeViewModel(repository) as T
    }
}

