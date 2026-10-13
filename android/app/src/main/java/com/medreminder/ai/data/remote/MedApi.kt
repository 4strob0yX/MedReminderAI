package com.medreminder.ai.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface MedApi {

    @POST("medicamentos")
    suspend fun crearMedicamento(@Body body: MedicamentoCreateDto): MedicamentoDto

    @GET("medicamentos")
    suspend fun listarMedicamentos(): List<MedicamentoDto>

    @POST("tratamientos")
    suspend fun crearTratamiento(@Body body: TratamientoCreateDto): TratamientoDto

    @GET("tratamientos")
    suspend fun listarTratamientos(): List<TratamientoDto>

    @GET("recordatorios")
    suspend fun listarRecordatorios(@Query("fecha") fecha: String? = null): List<RecordatorioDto>

    @POST("recordatorios/{id}/tomar")
    suspend fun tomarRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto

    @POST("recordatorios/{id}/posponer")
    suspend fun posponerRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto

    @POST("recordatorios/{id}/omitir")
    suspend fun omitirRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto
}
