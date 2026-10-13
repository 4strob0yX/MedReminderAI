package com.medreminder.ai.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.medreminder.ai.data.remote.MedicamentoDto
import com.medreminder.ai.data.remote.RecordatorioDto
import com.medreminder.ai.data.remote.TratamientoDto
import com.medreminder.ai.data.repository.MedRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import java.util.Locale

enum class HomeTab { HOY, MI_BOTIQUIN }

enum class FormaFarmaceutica(val label: String) {
    COMPRIMIDOS("Comprimidos / Cápsulas"),
    GOTAS("Gotas / Jarabe"),
    INYECTABLE("Inyectable / Ampolla")
}

data class TomaHoyItemUi(
    val idRecordatorio: Int,
    val idTratamiento: Int,
    val idMedicamento: Int,
    val etiquetaPeriodo: String,    // TOMA MATUTINA / TOMA DE TARDE / TOMA NOCTURNA
    val horaFormateada: String,     // ej. 08:00 AM, 14:30 PM, 21:00 PM
    val nombreMedicamento: String,
    val dosisDetalle: String,       // ej. 20 mg • En ayunas
    val estado: String,             // pendiente, tomado, pospuesto, omitido
    val vecesPospuesto: Int
)

enum class StockNivel(val label: String) {
    OPTIMO("Óptimo"),
    NORMAL("Normal"),
    BAJO("Bajo")
}

data class BotiquinItemUi(
    val idMedicamento: Int,
    val nombre: String,
    val subtituloDosis: String,     // ej. 400 mg • Caja de 30 comprimidos
    val stockActual: Int,
    val capacidadReferencia: Int,
    val porcentajeRestante: Int,
    val textoQuedan: String,        // ej. Quedan 15 pastillas
    val nivel: StockNivel
)

data class NuevoMedicamentoFormState(
    val forma: FormaFarmaceutica = FormaFarmaceutica.COMPRIMIDOS,
    val nombre: String = "",
    val dosis: String = "",
    val frecuenciaTexto: String = "Cada 8 horas",
    val frecuenciaHoras: Int = 8,
    val cantidadStockTexto: String = "30",
    val nombreError: String? = null,
    val dosisError: String? = null,
    val isSubmitting: Boolean = false
)

data class HomeUiState(
    val selectedTab: HomeTab = HomeTab.HOY,
    val showNuevoMedicamento: Boolean = false,
    val selectedTomaForModal: TomaHoyItemUi? = null,
    val fechaEncabezado: String = "",
    val tomasHoy: List<TomaHoyItemUi> = emptyList(),
    val tomasCompletadasCount: Int = 0,
    val botiquinItems: List<BotiquinItemUi> = emptyList(),
    val porcentajeGlobalSuministros: Int = 100,
    val diasReposicionEstimada: Int = 6,
    val isLoading: Boolean = false,
    val isActionInFlight: Boolean = false,
    val snackbarMessage: String? = null,
    val form: NuevoMedicamentoFormState = NuevoMedicamentoFormState()
)

/**
 * ViewModel principal para las 4 pantallas post-autenticación:
 * 1. Hoy (Plan Diario)
 * 2. Confirmación de Toma (Modal sobre Hoy)
 * 3. Mi Botiquín (Inventario y progreso de suministros)
 * 4. Registrar Medicamento (Formulario clínico de alta)
 */
class HomeViewModel(private val repository: MedRepository) : ViewModel() {

    private val _state = MutableStateFlow(HomeUiState(fechaEncabezado = buildFechaHoyEsp()))
    val state: StateFlow<HomeUiState> = _state.asStateFlow()

    init {
        cargarDatos()
    }

    fun onSelectTab(tab: HomeTab) {
        _state.update { it.copy(selectedTab = tab, selectedTomaForModal = null) }
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

    fun onOpenConfirmacionToma(item: TomaHoyItemUi) {
        if (item.estado != "pendiente") return
        _state.update { it.copy(selectedTomaForModal = item) }
    }

    fun onDismissConfirmacionToma() {
        if (_state.value.isActionInFlight) return
        _state.update { it.copy(selectedTomaForModal = null) }
    }

    fun onSnackbarShown() {
        _state.update { it.copy(snackbarMessage = null) }
    }

    // --- Eventos de Confirmación de Toma (Estrictamente esperan 200 OK del backend) ---

    fun onTomarAhora() {
        val toma = _state.value.selectedTomaForModal ?: return
        if (_state.value.isActionInFlight) return

        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            val res = repository.tomarRecordatorio(toma.idRecordatorio)
            res.fold(
                onSuccess = {
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            selectedTomaForModal = null,
                            snackbarMessage = "Toma registrada: ${toma.nombreMedicamento}"
                        )
                    }
                    cargarDatos(silencioso = true)
                },
                onFailure = { err ->
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            snackbarMessage = err.message ?: "No se pudo registrar la toma"
                        )
                    }
                }
            )
        }
    }

    fun onPosponer30Min() {
        val toma = _state.value.selectedTomaForModal ?: return
        if (_state.value.isActionInFlight) return

        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            val res = repository.posponerRecordatorio(toma.idRecordatorio)
            res.fold(
                onSuccess = { updatedDto ->
                    val msg = if (updatedDto.estado == "omitido") {
                        "Límite de posposiciones alcanzado: marcado como omitido"
                    } else {
                        "Pospuesto 30 minutos (${updatedDto.vecesPospuesto}/2)"
                    }
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            selectedTomaForModal = null,
                            snackbarMessage = msg
                        )
                    }
                    cargarDatos(silencioso = true)
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

        _state.update { it.copy(isActionInFlight = true, snackbarMessage = null) }
        viewModelScope.launch {
            val res = repository.omitirRecordatorio(toma.idRecordatorio)
            res.fold(
                onSuccess = {
                    _state.update {
                        it.copy(
                            isActionInFlight = false,
                            selectedTomaForModal = null,
                            snackbarMessage = "Toma marcada como omitida"
                        )
                    }
                    cargarDatos(silencioso = true)
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

    // --- Eventos del Formulario "Registrar Medicamento" ---

    fun onFormaChange(forma: FormaFarmaceutica) {
        _state.update { it.copy(form = it.form.copy(forma = forma)) }
    }

    fun onNombreMedChange(v: String) {
        _state.update { it.copy(form = it.form.copy(nombre = v, nombreError = null)) }
    }

    fun onDosisMedChange(v: String) {
        _state.update { it.copy(form = it.form.copy(dosis = v, dosisError = null)) }
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

    fun onGuardarMedicamento() {
        val f = _state.value.form
        if (f.isSubmitting) return

        val nombreErr = if (f.nombre.isBlank()) "Ingresa el nombre del medicamento" else null
        val dosisReal = f.dosis.ifBlank { "1 comprimido" }
        if (nombreErr != null) {
            _state.update { it.copy(form = f.copy(nombreError = nombreErr)) }
            return
        }

        val stock = f.cantidadStockTexto.toIntOrNull()?.coerceAtLeast(0) ?: 30
        val freqHoras = f.frecuenciaHoras.coerceIn(1, 168)

        _state.update { it.copy(form = f.copy(isSubmitting = true)) }
        viewModelScope.launch {
            val res = repository.registrarMedicamentoConTratamiento(
                nombre = f.nombre,
                dosis = dosisReal,
                frecuenciaHoras = freqHoras,
                cantidadStock = stock
            )
            res.fold(
                onSuccess = { medCreado ->
                    _state.update {
                        it.copy(
                            showNuevoMedicamento = false,
                            form = NuevoMedicamentoFormState(),
                            snackbarMessage = "${medCreado.nombre} guardado y alarmas programadas"
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

    // --- Carga y mapeo de datos desde el Backend ---

    fun cargarDatos(silencioso: Boolean = false) {
        if (!silencioso) {
            _state.update { it.copy(isLoading = true) }
        }
        viewModelScope.launch {
            val hoyUtc = LocalDate.now(ZoneOffset.UTC).toString()
            val res = repository.cargarDashboard(fechaUtc = hoyUtc)
            res.fold(
                onSuccess = { bundle ->
                    val tomasUi = mapRecordatoriosToUi(
                        recordatorios = bundle.recordatoriosHoy,
                        tratamientos = bundle.tratamientos,
                        medicamentos = bundle.medicamentos
                    )
                    val botiquinUi = mapMedicamentosToBotiquinUi(bundle.medicamentos)
                    val completadas = tomasUi.count { it.estado == "tomado" }
                    val promedioGlobal = if (botiquinUi.isEmpty()) 100 else {
                        botiquinUi.map { it.porcentajeRestante }.average().toInt().coerceIn(0, 100)
                    }

                    _state.update {
                        it.copy(
                            isLoading = false,
                            fechaEncabezado = buildFechaHoyEsp(),
                            tomasHoy = tomasUi,
                            tomasCompletadasCount = completadas,
                            botiquinItems = botiquinUi,
                            porcentajeGlobalSuministros = promedioGlobal
                        )
                    }
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

    private fun mapRecordatoriosToUi(
        recordatorios: List<RecordatorioDto>,
        tratamientos: List<TratamientoDto>,
        medicamentos: List<MedicamentoDto>
    ): List<TomaHoyItemUi> {
        val tratById = tratamientos.associateBy { it.idTratamiento }
        val medById = medicamentos.associateBy { it.idMedicamento }
        val zoneLocal = ZoneId.systemDefault()

        return recordatorios.mapNotNull { rec ->
            val trat = tratById[rec.idTratamiento]
            val med = trat?.let { medById[it.idMedicamento] }
            val nombreMed = med?.nombre ?: "Medicamento #${rec.idTratamiento}"
            val dosisMed = med?.dosis ?: "1 dosis"

            val localDateTime = parseUtcToLocal(rec.horaProgramada, zoneLocal)
            val hour = localDateTime.hour
            val minute = localDateTime.minute

            val periodo = when {
                hour < 12 -> "TOMA MATUTINA"
                hour < 19 -> "TOMA DE TARDE"
                else -> "TOMA NOCTURNA"
            }
            val sufijo = if (hour < 12) "AM" else "PM"
            val horaStr = String.format(Locale.US, "%02d:%02d %s", hour, minute, sufijo)

            val indicacion = when {
                hour < 12 -> "En ayunas"
                hour < 19 -> "Con el almuerzo"
                else -> "1 comprimido"
            }

            TomaHoyItemUi(
                idRecordatorio = rec.idRecordatorio,
                idTratamiento = rec.idTratamiento,
                idMedicamento = med?.idMedicamento ?: 0,
                etiquetaPeriodo = periodo,
                horaFormateada = horaStr,
                nombreMedicamento = nombreMed,
                dosisDetalle = "$dosisMed • $indicacion",
                estado = rec.estado,
                vecesPospuesto = rec.vecesPospuesto
            )
        }
    }

    private fun mapMedicamentosToBotiquinUi(medicamentos: List<MedicamentoDto>): List<BotiquinItemUi> {
        return medicamentos.map { med ->
            val capacidadRef = when {
                med.cantidadStock > 30 -> ((med.cantidadStock + 9) / 10) * 10
                med.cantidadStock in 21..30 -> 30
                med.cantidadStock in 15..20 -> 20
                else -> 30
            }
            val pct = ((med.cantidadStock.toFloat() / capacidadRef.toFloat()) * 100f)
                .toInt()
                .coerceIn(0, 100)

            val nivel = when {
                pct <= 25 || med.cantidadStock <= 5 -> StockNivel.BAJO
                pct >= 85 -> StockNivel.OPTIMO
                else -> StockNivel.NORMAL
            }

            BotiquinItemUi(
                idMedicamento = med.idMedicamento,
                nombre = med.nombre,
                subtituloDosis = "${med.dosis} • Caja de $capacidadRef comprimidos",
                stockActual = med.cantidadStock,
                capacidadReferencia = capacidadRef,
                porcentajeRestante = pct,
                textoQuedan = "Quedan ${med.cantidadStock} comprimidos",
                nivel = nivel
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
        val hoy = LocalDate.now()
        val esLocale = Locale.forLanguageTag("es-ES")
        val formatter = DateTimeFormatter.ofPattern("EEEE, d 'de' MMM", esLocale)
        val raw = hoy.format(formatter)
        return raw.replaceFirstChar { if (it.isLowerCase()) it.titlecase(esLocale) else it.toString() }
    }

    class Factory(private val repository: MedRepository) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T = HomeViewModel(repository) as T
    }
}
