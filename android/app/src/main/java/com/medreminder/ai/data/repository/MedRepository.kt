package com.medreminder.ai.data.repository

import com.google.gson.Gson
import com.medreminder.ai.data.remote.ApiError
import com.medreminder.ai.data.remote.MedApi
import com.medreminder.ai.data.remote.MedicamentoCreateDto
import com.medreminder.ai.data.remote.MedicamentoDto
import com.medreminder.ai.data.remote.RecordatorioDto
import com.medreminder.ai.data.remote.TratamientoCreateDto
import com.medreminder.ai.data.remote.TratamientoDto
import retrofit2.HttpException
import java.io.IOException

data class DashboardBundle(
    val medicamentos: List<MedicamentoDto>,
    val tratamientos: List<TratamientoDto>,
    val recordatoriosHoy: List<RecordatorioDto>
)

class MedRepository(private val api: MedApi) {

    private val gson = Gson()

    suspend fun cargarDashboard(fechaUtc: String?): Result<DashboardBundle> = runCatching {
        val medicamentos = api.listarMedicamentos()
        val tratamientos = api.listarTratamientos()
        val recordatorios = api.listarRecordatorios(fecha = fechaUtc)
        DashboardBundle(
            medicamentos = medicamentos,
            tratamientos = tratamientos,
            recordatoriosHoy = recordatorios
        )
    }.recoverCatching { throw Exception(mapError(it)) }

    suspend fun registrarMedicamentoConTratamiento(
        nombre: String,
        dosis: String,
        frecuenciaHoras: Int,
        cantidadStock: Int
    ): Result<MedicamentoDto> = runCatching {
        val med = api.crearMedicamento(
            MedicamentoCreateDto(
                nombre = nombre.trim(),
                dosis = dosis.trim(),
                cantidadStock = cantidadStock
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
