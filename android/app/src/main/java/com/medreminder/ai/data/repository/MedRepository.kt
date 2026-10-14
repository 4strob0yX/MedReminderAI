package com.medreminder.ai.data.repository

import com.google.gson.Gson
import com.medreminder.ai.data.remote.AlergiaCreateDto
import com.medreminder.ai.data.remote.AlergiaDto
import com.medreminder.ai.data.remote.ApiError
import com.medreminder.ai.data.remote.ContactoApoyoCreateDto
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.data.remote.MedApi
import com.medreminder.ai.data.remote.MedicamentoCatalogoItemDto
import com.medreminder.ai.data.remote.MedicamentoCreateDto
import com.medreminder.ai.data.remote.MedicamentoDto
import com.medreminder.ai.data.remote.RecordatorioDto
import com.medreminder.ai.data.remote.TratamientoCreateDto
import com.medreminder.ai.data.remote.TratamientoDto
import com.medreminder.ai.data.remote.VerificarAlergiasInDto
import com.medreminder.ai.data.remote.VerificarAlergiasOutDto
import retrofit2.HttpException
import java.io.IOException

data class DashboardBundle(
    val medicamentos: List<MedicamentoDto>,
    val tratamientos: List<TratamientoDto>,
    val recordatoriosHoy: List<RecordatorioDto>,
    val alergias: List<AlergiaDto>,
    val contactosApoyo: List<ContactoApoyoDto>
)

class MedRepository(private val api: MedApi) {

    private val gson = Gson()

    suspend fun cargarDashboard(fechaUtc: String?): Result<DashboardBundle> = runCatching {
        val medicamentos = api.listarMedicamentos()
        val tratamientos = api.listarTratamientos()
        val recordatorios = api.listarRecordatorios(fecha = fechaUtc)
        val alergias = runCatching { api.listarAlergias() }.getOrDefault(emptyList())
        val contactos = runCatching { api.listarContactos() }.getOrDefault(emptyList())
        DashboardBundle(
            medicamentos = medicamentos,
            tratamientos = tratamientos,
            recordatoriosHoy = recordatorios,
            alergias = alergias,
            contactosApoyo = contactos
        )
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun buscarCatalogo(query: String?): Result<List<MedicamentoCatalogoItemDto>> = runCatching {
        api.buscarCatalogo(query)
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun verificarAlergias(nombre: String, principioActivo: String?): Result<VerificarAlergiasOutDto> = runCatching {
        api.verificarAlergias(VerificarAlergiasInDto(nombre = nombre, principioActivo = principioActivo))
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun registrarMedicamentoConTratamiento(
        nombre: String,
        principioActivo: String?,
        dosis: String,
        frecuenciaHoras: Int,
        cantidadStock: Int,
        permitePosponer: Boolean,
        esCritico: Boolean,
        contraindicaciones: String?
    ): Result<MedicamentoDto> = runCatching {
        val med = api.crearMedicamento(
            MedicamentoCreateDto(
                nombre = nombre.trim(),
                principioActivo = principioActivo?.trim()?.ifBlank { null },
                dosis = dosis.trim(),
                cantidadStock = cantidadStock,
                permitePosponer = permitePosponer,
                esCritico = esCritico,
                contraindicaciones = contraindicaciones?.trim()?.ifBlank { null }
            )
        )
        api.crearTratamiento(
            TratamientoCreateDto(
                idMedicamento = med.idMedicamento,
                frecuenciaHoras = frecuenciaHoras,
                estado = "activo"
            )
        )
        med
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun tomarRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.tomarRecordatorio(idRecordatorio)
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun posponerRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.posponerRecordatorio(idRecordatorio)
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun omitirRecordatorio(idRecordatorio: Int): Result<RecordatorioDto> = runCatching {
        api.omitirRecordatorio(idRecordatorio)
    }.recoverCatching { throw Exception(mapError(it)) }

    // --- Alergias ---
    suspend fun listarAlergias(): Result<List<AlergiaDto>> = runCatching {
        api.listarAlergias()
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun agregarAlergia(sustancia: String, severidad: String, reaccion: String?): Result<AlergiaDto> = runCatching {
        api.agregarAlergia(
            AlergiaCreateDto(
                sustancia = sustancia.trim(),
                severidad = severidad,
                reaccion = reaccion?.trim()?.ifBlank { null }
            )
        )
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun eliminarAlergia(idAlergia: Int): Result<Unit> = runCatching {
        val res = api.eliminarAlergia(idAlergia)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar la alergia")
        }
    }.recoverCatching { throw Exception(mapError(it)) }

    // --- Contactos de Apoyo ---
    suspend fun listarContactos(): Result<List<ContactoApoyoDto>> = runCatching {
        api.listarContactos()
    }.recoverCatching { throw Exception(mapError(it)) }

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
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun eliminarContacto(idContacto: Int): Result<Unit> = runCatching {
        val res = api.eliminarContacto(idContacto)
        if (!res.isSuccessful && res.code() != 204) {
            throw Exception("No se pudo eliminar el contacto")
        }
    }.recoverCatching { throw Exception(mapError(it)) }

    private fun mapError(t: Throwable): String = when (t) {
        is HttpException -> {
            val raw = t.response()?.errorBody()?.string()
            val detail = runCatching { gson.fromJson(raw, ApiError::class.java)?.detail }.getOrNull()
            detail ?: "Error del servidor (${t.code()})"
        }
        is IOException -> "Sin conexión con el servidor. Verifica tu red."
        else -> t.message ?: "Error inesperado"
    }
}
