package com.medreminder.ai.data.repository

import com.medreminder.ai.data.remote.AiChatRequestDto
import com.medreminder.ai.data.remote.AiChatResponseDto
import com.medreminder.ai.data.remote.AiMedicationSuggestRequestDto
import com.medreminder.ai.data.remote.AiMedicationSuggestResponseDto
import com.medreminder.ai.data.remote.AiPrescriptionScanRequestDto
import com.medreminder.ai.data.remote.AiPrescriptionScanResponseDto
import com.medreminder.ai.data.remote.AlergiaCreateDto
import com.medreminder.ai.data.remote.AlergiaDto
import com.medreminder.ai.data.remote.AlertaCuidadorCreateDto
import com.medreminder.ai.data.remote.AlertaCuidadorDto
import com.medreminder.ai.data.remote.ContactoApoyoCreateDto
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.data.remote.CuidadorPanelResponseDto
import com.medreminder.ai.data.remote.MedApi
import com.medreminder.ai.data.remote.MedicamentoCatalogoItemDto
import com.medreminder.ai.data.remote.MedicamentoCreateDto
import com.medreminder.ai.data.remote.MedicamentoDto
import com.medreminder.ai.data.remote.RecordatorioDto
import com.medreminder.ai.data.remote.StockUpdateDto
import com.medreminder.ai.data.remote.TratamientoCreateDto
import com.medreminder.ai.data.remote.TratamientoDto
import com.medreminder.ai.data.remote.UpdatePerfilEdadRequestDto
import com.medreminder.ai.data.remote.UsuarioDto
import com.medreminder.ai.data.remote.VerificarAlergiasInDto
import com.medreminder.ai.data.remote.VerificarAlergiasOutDto
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
    val perfil: UsuarioDto? = null
)

class MedRepository(private val api: MedApi) {

    @Volatile
    var cachedBundle: DashboardBundle? = null
        private set

    suspend fun cargarDashboard(
        fechaUtc: String?,
        tzOffsetMinutes: Int? = null
    ): Result<DashboardBundle> = runCatching {
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
                perfil = unified.perfil
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
                    perfil = perfil
                )
            }
        }
        cachedBundle = bundle
        bundle
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun buscarCatalogo(query: String?): Result<List<MedicamentoCatalogoItemDto>> = runCatching {
        api.buscarCatalogo(query)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun verificarAlergias(nombre: String, principioActivo: String?): Result<VerificarAlergiasOutDto> = runCatching {
        api.verificarAlergias(VerificarAlergiasInDto(nombre = nombre, principioActivo = principioActivo))
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

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
    ): Result<MedicamentoDto> = runCatching {
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
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun actualizarStockMedicamento(
        idMedicamento: Int,
        nuevoStock: Int,
        medFallback: MedicamentoCreateDto? = null
    ): Result<MedicamentoDto> = runCatching {
        try {
            api.actualizarStock(idMedicamento, StockUpdateDto(cantidadStock = nuevoStock))
        } catch (e: HttpException) {
            if ((e.code() == 404 || e.code() == 405) && medFallback != null) {
                api.actualizarMedicamento(idMedicamento, medFallback.copy(cantidadStock = nuevoStock))
            } else {
                throw e
            }
        }
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun eliminarMedicamento(idMedicamento: Int): Result<Unit> = runCatching {
        val res = api.eliminarMedicamento(idMedicamento)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar el medicamento")
        }
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun tomarRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.tomarRecordatorio(idRecordatorio)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun posponerRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.posponerRecordatorio(idRecordatorio)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun omitirRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.omitirRecordatorio(idRecordatorio)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun revertirRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.revertirRecordatorio(idRecordatorio)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    // --- Alergias ---
    suspend fun listarAlergias(): Result<List<AlergiaDto>> = runCatching {
        api.listarAlergias()
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun agregarAlergia(sustancia: String, severidad: String, reaccion: String?): Result<AlergiaDto> = runCatching {
        api.agregarAlergia(
            AlergiaCreateDto(
                sustancia = sustancia.trim(),
                severidad = severidad,
                reaccion = reaccion?.trim()?.ifBlank { null }
            )
        )
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun eliminarAlergia(idAlergia: Int): Result<Unit> = runCatching {
        val res = api.eliminarAlergia(idAlergia)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar la alergia")
        }
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    // --- Contactos de Apoyo ---
    suspend fun listarContactos(): Result<List<ContactoApoyoDto>> = runCatching {
        api.listarContactos()
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun guardarContacto(
        idContacto: Int?,
        nombre: String,
        telefono: String,
        parentesco: String,
        correo: String?,
        esPrincipal: Boolean
    ): Result<ContactoApoyoDto> = runCatching {
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
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun eliminarContacto(idContacto: Int): Result<Unit> = runCatching {
        val res = api.eliminarContacto(idContacto)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar el contacto")
        }
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    // --- Motor IA Clínico Ollama (medi-clinico) ---
    suspend fun consultarMediAi(
        query: String,
        nombreUsuario: String? = "Paciente",
        contextoPantalla: String? = "Hoy"
    ): Result<AiChatResponseDto> = runCatching {
        api.consultarMediAi(
            AiChatRequestDto(
                query = query.trim(),
                nombreUsuario = nombreUsuario,
                contextoPantalla = contextoPantalla
            )
        )
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun sugerirMedicamentoAi(nombre: String): Result<AiMedicationSuggestResponseDto> = runCatching {
        api.sugerirMedicamentoAi(AiMedicationSuggestRequestDto(nombre = nombre.trim()))
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun analizarRecetaAi(
        textoReceta: String? = null,
        imageBase64: String? = null
    ): Result<AiPrescriptionScanResponseDto> = runCatching {
        api.analizarRecetaAi(
            AiPrescriptionScanRequestDto(
                textoReceta = textoReceta?.trim()?.ifBlank { null },
                imageBase64 = imageBase64?.ifBlank { null }
            )
        )
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    // --- Vista del Cuidador y Edad del Perfil ---

    suspend fun actualizarPerfilEdad(fechaNacimiento: String, rol: String? = null): Result<UsuarioDto> = runCatching {
        api.actualizarPerfilEdad(UpdatePerfilEdadRequestDto(fechaNacimiento = fechaNacimiento, rol = rol))
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun obtenerPanelCuidador(tzOffsetMinutes: Int? = null): Result<CuidadorPanelResponseDto> = runCatching {
        api.obtenerPanelCuidador(tzOffsetMinutes = tzOffsetMinutes)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun dispararAlertaCuidador(
        tipoAlerta: String,
        medicamentoNombre: String,
        dosis: String,
        accion: String,
        esCritico: Boolean,
        mensaje: String
    ): Result<AlertaCuidadorDto> = runCatching {
        api.dispararAlertaCuidador(
            AlertaCuidadorCreateDto(
                tipoAlerta = tipoAlerta,
                medicamentoNombre = medicamentoNombre,
                dosis = dosis,
                accion = accion,
                esCritico = esCritico,
                mensaje = mensaje
            )
        )
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
    }

    suspend fun marcarAlertaCuidadorAtendida(idAlerta: Int): Result<AlertaCuidadorDto> = runCatching {
        api.marcarAlertaCuidadorAtendida(idAlerta)
    }.recoverCatching {
        if (it is CancellationException) throw it
        throw Exception(mapError(it))
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

