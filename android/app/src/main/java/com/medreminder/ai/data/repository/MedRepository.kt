package com.medreminder.ai.data.repository

import android.content.Context
import com.medreminder.ai.data.local.LocalCacheStore
import com.medreminder.ai.data.local.OfflineSyncWorker
import com.medreminder.ai.data.local.TokenStore
import com.medreminder.ai.data.remote.AiAdherencePredictRequestDto
import com.medreminder.ai.data.remote.AiChatRequestDto
import com.medreminder.ai.data.remote.AiChatResponseDto
import com.medreminder.ai.data.remote.AiEvaluarPacienteResponseDto
import com.medreminder.ai.data.remote.AiMedicationSuggestRequestDto
import com.medreminder.ai.data.remote.AiMedicationSuggestResponseDto
import com.medreminder.ai.data.remote.AiPrescriptionScanRequestDto
import com.medreminder.ai.data.remote.AiPrescriptionScanResponseDto
import com.medreminder.ai.data.remote.AlergiaCreateDto
import com.medreminder.ai.data.remote.AlergiaDto
import com.medreminder.ai.data.remote.AlertaCuidadorCreateDto
import com.medreminder.ai.data.remote.AlertaCuidadorDto
import com.medreminder.ai.data.remote.ChangePasswordRequestDto
import com.medreminder.ai.data.remote.CodigoVinculacionOutDto
import com.medreminder.ai.data.remote.ContactoApoyoCreateDto
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.data.remote.CuidadorPanelResponseDto
import com.medreminder.ai.data.remote.EscudoActivarResponseDto
import com.medreminder.ai.data.remote.EstadisticasOutDto
import com.medreminder.ai.data.remote.MedApi
import com.medreminder.ai.data.remote.MedicamentoCatalogoItemDto
import com.medreminder.ai.data.remote.MedicamentoCreateDto
import com.medreminder.ai.data.remote.MedicamentoDto
import com.medreminder.ai.data.remote.PacienteVinculadoItemDto
import com.medreminder.ai.data.remote.RecordatorioDto
import com.medreminder.ai.data.remote.StockUpdateDto
import com.medreminder.ai.data.remote.TorneoModelosResponseDto
import com.medreminder.ai.data.remote.TratamientoCreateDto
import com.medreminder.ai.data.remote.TratamientoDto
import com.medreminder.ai.data.remote.TratamientoUpdateDto
import com.medreminder.ai.data.remote.UpdatePerfilEdadRequestDto
import com.medreminder.ai.data.remote.UpdatePerfilRequestDto
import com.medreminder.ai.data.remote.UsuarioDto
import com.medreminder.ai.data.remote.VerificarAlergiasInDto
import com.medreminder.ai.data.remote.VerificarAlergiasOutDto
import com.medreminder.ai.data.remote.VinculacionesResumenOutDto
import com.medreminder.ai.data.remote.VincularPacienteRequestDto
import com.medreminder.ai.data.remote.parseApiErrorDetail
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import retrofit2.HttpException
import java.io.IOException

data class DashboardBundle(
    val medicamentos: List<MedicamentoDto>,
    val tratamientos: List<TratamientoDto>,
    val recordatoriosHoy: List<RecordatorioDto>,
    val alergias: List<AlergiaDto>,
    val contactosApoyo: List<ContactoApoyoDto>,
    val nombreUsuario: String? = null,
    val perfil: UsuarioDto? = null,
    val fromOfflineCache: Boolean = false,
    val pendingSyncCount: Int = 0
)

data class SyncResult(
    val syncedCount: Int,
    val stillPending: Int,
    val hitNetworkError: Boolean
)

class OfflineQueuedException(message: String, val pendingCount: Int) : Exception(message)

class MedRepository(
    private val api: MedApi,
    private val localCache: LocalCacheStore? = null,
    private val tokenStore: TokenStore? = null,
    private val appContext: Context? = null
) {

    @Volatile
    var cachedBundle: DashboardBundle? = localCache?.loadLatestDashboard()
        private set

    fun getLocalCachedDashboard(fechaKey: String): DashboardBundle? {
        val loaded = localCache?.loadDashboard(fechaKey) ?: return null
        return loaded.copy(
            fromOfflineCache = true,
            pendingSyncCount = localCache.pendingActionsCount()
        )
    }

    fun getLocalCachedEstadisticas(): EstadisticasOutDto? = localCache?.loadEstadisticas()

    fun pendingSyncCount(): Int = localCache?.pendingActionsCount() ?: 0

    suspend fun syncPendingActions(): SyncResult {
        val store = localCache ?: return SyncResult(0, 0, false)
        if (tokenStore != null && tokenStore.accessToken.isNullOrBlank()) {
            return SyncResult(0, store.pendingActionsCount(), false)
        }
        val queue = store.getPendingActions()
        if (queue.isEmpty()) return SyncResult(0, 0, false)

        var synced = 0
        var networkFailed = false
        for (item in queue) {
            try {
                when (item.accion) {
                    "tomar" -> api.tomarRecordatorio(item.idRecordatorio)
                    "posponer" -> api.posponerRecordatorio(item.idRecordatorio)
                    "omitir" -> api.omitirRecordatorio(item.idRecordatorio)
                    "revertir" -> api.revertirRecordatorio(item.idRecordatorio)
                }
                store.removePendingAction(item.id)
                synced++
            } catch (e: CancellationException) {
                throw e
            } catch (e: HttpException) {
                // Si el servidor ya procesó o rechazó por estado previo (404/409), limpiar entrada obsoleta
                if (e.code() == 404 || e.code() == 409) {
                    store.removePendingAction(item.id)
                } else if (e.code() == 401) {
                    networkFailed = true
                    break
                } else {
                    store.removePendingAction(item.id)
                }
            } catch (_: IOException) {
                networkFailed = true
                break
            }
        }
        return SyncResult(
            syncedCount = synced,
            stillPending = store.pendingActionsCount(),
            hitNetworkError = networkFailed
        )
    }

    private suspend inline fun <T> safeCall(crossinline block: suspend () -> T): Result<T> =
        try {
            Result.success(block())
        } catch (e: CancellationException) {
            throw e
        } catch (e: Throwable) {
            Result.failure(Exception(mapError(e)))
        }

    suspend fun cargarDashboard(
        fechaUtc: String?,
        tzOffsetMinutes: Int? = null
    ): Result<DashboardBundle> {
        val cacheKey = fechaUtc?.trim()?.ifBlank { null } ?: "hoy"
        return try {
            syncPendingActions()
            val unified = runCatching {
                api.obtenerDashboardUnificado(fecha = fechaUtc, tzOffsetMinutes = tzOffsetMinutes)
            }.onFailure { if (it is CancellationException) throw it }.getOrNull()

            val bundle = if (unified != null) {
                DashboardBundle(
                    medicamentos = unified.medicamentos,
                    tratamientos = unified.tratamientos,
                    recordatoriosHoy = unified.recordatoriosHoy,
                    alergias = unified.alergias,
                    contactosApoyo = unified.contactosApoyo,
                    nombreUsuario = unified.perfil?.nombre,
                    perfil = unified.perfil,
                    fromOfflineCache = false,
                    pendingSyncCount = pendingSyncCount()
                )
            } else {
                coroutineScope {
                    val medsDef = async { api.listarMedicamentos() }
                    val tratsDef = async { api.listarTratamientos() }
                    val recsDef = async { api.listarRecordatorios(fecha = fechaUtc, tzOffsetMinutes = tzOffsetMinutes) }
                    val alergiasDef = async {
                        runCatching { api.listarAlergias() }.onFailure { if (it is CancellationException) throw it }.getOrDefault(emptyList())
                    }
                    val contactosDef = async {
                        runCatching { api.listarContactos() }.onFailure { if (it is CancellationException) throw it }.getOrDefault(emptyList())
                    }
                    val perfilDef = async {
                        runCatching { api.obtenerPerfil() }.onFailure { if (it is CancellationException) throw it }.getOrNull()
                    }

                    val perfil = perfilDef.await()
                    DashboardBundle(
                        medicamentos = medsDef.await(),
                        tratamientos = tratsDef.await(),
                        recordatoriosHoy = recsDef.await(),
                        alergias = alergiasDef.await(),
                        contactosApoyo = contactosDef.await(),
                        nombreUsuario = perfil?.nombre,
                        perfil = perfil,
                        fromOfflineCache = false,
                        pendingSyncCount = pendingSyncCount()
                    )
                }
            }
            localCache?.saveDashboard(cacheKey, bundle)
            cachedBundle = bundle
            Result.success(bundle)
        } catch (e: CancellationException) {
            throw e
        } catch (e: IOException) {
            val offline = getLocalCachedDashboard(cacheKey)
            if (offline != null) {
                cachedBundle = offline
                Result.success(offline)
            } else {
                Result.failure(Exception(mapError(e)))
            }
        } catch (e: Throwable) {
            Result.failure(Exception(mapError(e)))
        }
    }

    suspend fun buscarCatalogo(query: String?): Result<List<MedicamentoCatalogoItemDto>> =
        safeCall { api.buscarCatalogo(query) }

    suspend fun verificarAlergias(nombre: String, principioActivo: String?): Result<VerificarAlergiasOutDto> =
        safeCall { api.verificarAlergias(VerificarAlergiasInDto(nombre = nombre, principioActivo = principioActivo)) }

    suspend fun registrarMedicamentoConTratamiento(
        nombre: String,
        principioActivo: String?,
        dosis: String,
        frecuenciaHoras: Int,
        cantidadStock: Int,
        permitePosponer: Boolean,
        esCritico: Boolean,
        contraindicaciones: String?,
        formaFarmaceutica: String = "comprimidos",
        colorPastilla: String = "blanco",
        instruccionesToma: String? = null,
        proposito: String? = null,
        fechaInicio: String? = null,
        fechaFin: String? = null
    ): Result<MedicamentoDto> = safeCall {
        val med = api.crearMedicamento(
            MedicamentoCreateDto(
                nombre = nombre.trim(),
                principioActivo = principioActivo?.trim()?.ifBlank { null },
                dosis = dosis.trim(),
                cantidadStock = cantidadStock,
                stockInicial = cantidadStock,
                formaFarmaceutica = formaFarmaceutica,
                colorPastilla = colorPastilla,
                instruccionesToma = instruccionesToma?.trim()?.ifBlank { null },
                proposito = proposito?.trim()?.ifBlank { null },
                permitePosponer = permitePosponer,
                esCritico = esCritico,
                contraindicaciones = contraindicaciones?.trim()?.ifBlank { null }
            )
        )
        api.crearTratamiento(
            TratamientoCreateDto(
                idMedicamento = med.idMedicamento,
                frecuenciaHoras = frecuenciaHoras,
                fechaInicio = fechaInicio,
                fechaFin = fechaFin,
                estado = "activo"
            )
        )
        med
    }

    suspend fun actualizarMedicamento(
        idMedicamento: Int,
        body: MedicamentoCreateDto
    ): Result<MedicamentoDto> = safeCall {
        api.actualizarMedicamento(idMedicamento, body)
    }

    suspend fun actualizarStockMedicamento(
        idMedicamento: Int,
        nuevoStock: Int,
        medFallback: MedicamentoCreateDto? = null
    ): Result<MedicamentoDto> = safeCall {
        try {
            api.actualizarStock(idMedicamento, StockUpdateDto(cantidadStock = nuevoStock))
        } catch (e: HttpException) {
            if ((e.code() == 404 || e.code() == 405) && medFallback != null) {
                api.actualizarMedicamento(idMedicamento, medFallback.copy(cantidadStock = nuevoStock))
            } else {
                throw e
            }
        }
    }

    suspend fun eliminarMedicamento(idMedicamento: Int): Result<Unit> = safeCall {
        val res = api.eliminarMedicamento(idMedicamento)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar el medicamento")
        }
    }

    suspend fun actualizarTratamiento(
        idTratamiento: Int,
        frecuenciaHoras: Int? = null,
        estado: String? = null
    ): Result<TratamientoDto> = safeCall {
        api.actualizarTratamiento(
            idTratamiento = idTratamiento,
            body = TratamientoUpdateDto(
                frecuenciaHoras = frecuenciaHoras,
                estado = estado
            )
        )
    }

    private suspend inline fun recordatorioActionWithOfflineQueue(
        idRecordatorio: Int,
        accion: String,
        crossinline apiCall: suspend () -> RecordatorioDto
    ): Result<RecordatorioDto> = try {
        val dto = apiCall()
        Result.success(dto)
    } catch (e: CancellationException) {
        throw e
    } catch (_: IOException) {
        val store = localCache
        if (store != null) {
            store.enqueuePendingAction(idRecordatorio, accion)
            appContext?.let { OfflineSyncWorker.enqueue(it) }
            val count = store.pendingActionsCount()
            Result.failure(
                OfflineQueuedException(
                    "Sin conexión: acción guardada localmente ($count pendiente(s) de sincronizar).",
                    pendingCount = count
                )
            )
        } else {
            Result.failure(Exception("Sin conexión con el servidor. Verifica tu red."))
        }
    } catch (e: Throwable) {
        Result.failure(Exception(mapError(e)))
    }

    suspend fun tomarRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> =
        recordatorioActionWithOfflineQueue(idRecordatorio, "tomar") {
            api.tomarRecordatorio(idRecordatorio)
        }

    suspend fun posponerRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> =
        recordatorioActionWithOfflineQueue(idRecordatorio, "posponer") {
            api.posponerRecordatorio(idRecordatorio)
        }

    suspend fun omitirRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> =
        recordatorioActionWithOfflineQueue(idRecordatorio, "omitir") {
            api.omitirRecordatorio(idRecordatorio)
        }

    suspend fun revertirRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> =
        recordatorioActionWithOfflineQueue(idRecordatorio, "revertir") {
            api.revertirRecordatorio(idRecordatorio)
        }

    // --- Estadísticas reales y Escudo de Racha ---

    suspend fun obtenerEstadisticas(tzOffsetMinutes: Int? = null): Result<EstadisticasOutDto> =
        try {
            val stats = api.obtenerEstadisticas(tzOffsetMinutes = tzOffsetMinutes)
            localCache?.saveEstadisticas(stats)
            Result.success(stats)
        } catch (e: CancellationException) {
            throw e
        } catch (e: IOException) {
            val cached = localCache?.loadEstadisticas()
            if (cached != null) Result.success(cached) else Result.failure(Exception(mapError(e)))
        } catch (e: Throwable) {
            Result.failure(Exception(mapError(e)))
        }

    suspend fun activarEscudo(tzOffsetMinutes: Int? = null): Result<EscudoActivarResponseDto> =
        safeCall { api.activarEscudo(tzOffsetMinutes = tzOffsetMinutes) }

    // --- Alergias ---
    suspend fun listarAlergias(): Result<List<AlergiaDto>> = safeCall { api.listarAlergias() }

    suspend fun agregarAlergia(sustancia: String, severidad: String, reaccion: String?): Result<AlergiaDto> =
        safeCall {
            api.agregarAlergia(
                AlergiaCreateDto(
                    sustancia = sustancia.trim(),
                    severidad = severidad,
                    reaccion = reaccion?.trim()?.ifBlank { null }
                )
            )
        }

    suspend fun eliminarAlergia(idAlergia: Int): Result<Unit> = safeCall {
        val res = api.eliminarAlergia(idAlergia)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar la alergia")
        }
    }

    // --- Contactos de Apoyo ---
    suspend fun listarContactos(): Result<List<ContactoApoyoDto>> = safeCall { api.listarContactos() }

    suspend fun guardarContacto(
        idContacto: Int?,
        nombre: String,
        telefono: String,
        parentesco: String,
        correo: String?,
        esPrincipal: Boolean
    ): Result<ContactoApoyoDto> = safeCall {
        val dto = ContactoApoyoCreateDto(
            nombreCompleto = nombre.trim(),
            telefono = telefono.trim(),
            parentesco = parentesco.trim(),
            correo = correo?.trim()?.ifBlank { null },
            esPrincipal = esPrincipal
        )
        if (idContacto != null) {
            api.actualizarContacto(idContacto, dto)
        } else {
            api.agregarContacto(dto)
        }
    }

    suspend fun eliminarContacto(idContacto: Int): Result<Unit> = safeCall {
        val res = api.eliminarContacto(idContacto)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar el contacto")
        }
    }

    // --- Motor IA Clínico Ollama (medi-clinico) & Predictor ML ---
    suspend fun consultarMediAi(
        query: String,
        nombreUsuario: String? = "Paciente",
        contextoPantalla: String? = "Hoy"
    ): Result<AiChatResponseDto> = safeCall {
        api.consultarMediAi(
            AiChatRequestDto(
                query = query.trim(),
                nombreUsuario = nombreUsuario,
                contextoPantalla = contextoPantalla
            )
        )
    }

    suspend fun sugerirMedicamentoAi(nombre: String): Result<AiMedicationSuggestResponseDto> = safeCall {
        api.sugerirMedicamentoAi(AiMedicationSuggestRequestDto(nombre = nombre.trim()))
    }

    suspend fun analizarRecetaAi(
        textoReceta: String? = null,
        imageBase64: String? = null
    ): Result<AiPrescriptionScanResponseDto> = safeCall {
        api.analizarRecetaAi(
            AiPrescriptionScanRequestDto(
                textoReceta = textoReceta?.trim()?.ifBlank { null },
                imageBase64 = imageBase64?.ifBlank { null }
            )
        )
    }

    suspend fun evaluarPacienteMl(
        pacienteId: Int,
        algoritmo: String = "random_forest"
    ): Result<AiEvaluarPacienteResponseDto> = safeCall {
        api.evaluarPacienteMl(pacienteId = pacienteId, algoritmo = algoritmo)
    }

    suspend fun predecirAdherenciaMl(
        request: AiAdherencePredictRequestDto,
        algoritmo: String = "random_forest"
    ): Result<AiEvaluarPacienteResponseDto> = safeCall {
        api.predecirAdherenciaMl(body = request, algoritmo = algoritmo)
    }

    suspend fun obtenerTorneoModelosMl(): Result<TorneoModelosResponseDto> = safeCall {
        api.obtenerTorneoModelosMl()
    }

    // --- Perfil de Usuario, Vista del Cuidador y Vinculación ---

    suspend fun actualizarPerfilCompleto(
        nombreCompleto: String? = null,
        fechaNacimiento: String? = null,
        rol: String? = null
    ): Result<UsuarioDto> = safeCall {
        api.actualizarPerfil(
            UpdatePerfilRequestDto(
                nombreCompleto = nombreCompleto?.trim()?.ifBlank { null },
                fechaNacimiento = fechaNacimiento?.trim()?.ifBlank { null },
                rol = rol
            )
        )
    }

    suspend fun cambiarPassword(currentPassword: String, newPassword: String): Result<String> = safeCall {
        val res = api.cambiarPassword(
            ChangePasswordRequestDto(
                currentPassword = currentPassword,
                newPassword = newPassword
            )
        )
        res.mensaje ?: res.detail ?: "Contraseña actualizada correctamente"
    }

    suspend fun actualizarPerfilEdad(fechaNacimiento: String, rol: String? = null): Result<UsuarioDto> = safeCall {
        api.actualizarPerfilEdad(UpdatePerfilEdadRequestDto(fechaNacimiento = fechaNacimiento, rol = rol))
    }

    suspend fun obtenerPanelCuidador(
        tzOffsetMinutes: Int? = null,
        idPaciente: Int? = null
    ): Result<CuidadorPanelResponseDto> = safeCall {
        api.obtenerPanelCuidador(idPaciente = idPaciente, tzOffsetMinutes = tzOffsetMinutes)
    }

    suspend fun generarCodigoVinculacion(): Result<CodigoVinculacionOutDto> = safeCall {
        api.generarCodigoVinculacion()
    }

    suspend fun vincularConPaciente(
        codigo: String,
        parentesco: String? = null,
        tzOffsetMinutes: Int? = null
    ): Result<PacienteVinculadoItemDto> = safeCall {
        api.vincularConPaciente(
            body = VincularPacienteRequestDto(
                codigoVinculacion = codigo.trim().uppercase(),
                parentesco = parentesco?.trim()?.ifBlank { null }
            ),
            tzOffsetMinutes = tzOffsetMinutes
        )
    }

    suspend fun listarPacientesVinculados(tzOffsetMinutes: Int? = null): Result<List<PacienteVinculadoItemDto>> =
        safeCall { api.listarPacientesVinculados(tzOffsetMinutes = tzOffsetMinutes) }

    suspend fun obtenerResumenVinculaciones(tzOffsetMinutes: Int? = null): Result<VinculacionesResumenOutDto> =
        safeCall { api.obtenerResumenVinculaciones(tzOffsetMinutes = tzOffsetMinutes) }

    suspend fun revocarVinculacion(idVinculacion: Int): Result<Unit> = safeCall {
        val res = api.revocarVinculacion(idVinculacion)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo desvincular el enlace")
        }
    }

    suspend fun dispararAlertaCuidador(
        tipoAlerta: String,
        medicamentoNombre: String,
        dosis: String,
        accion: String,
        esCritico: Boolean,
        mensaje: String,
        idPaciente: Int? = null
    ): Result<AlertaCuidadorDto> = safeCall {
        api.dispararAlertaCuidador(
            body = AlertaCuidadorCreateDto(
                tipoAlerta = tipoAlerta,
                medicamentoNombre = medicamentoNombre,
                dosis = dosis,
                accion = accion,
                esCritico = esCritico,
                mensaje = mensaje
            ),
            idPaciente = idPaciente
        )
    }

    suspend fun marcarAlertaCuidadorAtendida(idAlerta: Int): Result<AlertaCuidadorDto> = safeCall {
        api.marcarAlertaCuidadorAtendida(idAlerta)
    }

    private fun mapError(t: Throwable): String = when (t) {
        is HttpException -> {
            val raw = t.response()?.errorBody()?.string()
            val detail = parseApiErrorDetail(raw)
            detail ?: "Error del servidor (${t.code()})"
        }
        is IOException -> "Sin conexión con el servidor. Verifica tu red."
        else -> t.message ?: "Error inesperado"
    }
}
