package com.medreminder.ai.data.remote

import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.Query

interface MedApi {

    @GET("auth/me")
    suspend fun obtenerPerfil(): UsuarioDto

    @PATCH("auth/me/edad")
    suspend fun actualizarPerfilEdad(@Body body: UpdatePerfilEdadRequestDto): UsuarioDto

    // --- Vista del Cuidador y Alertas Geriátricas ---
    @GET("cuidador/panel")
    suspend fun obtenerPanelCuidador(
        @Query("tz_offset_minutes") tzOffsetMinutes: Int? = null
    ): CuidadorPanelResponseDto

    @POST("cuidador/alertas")
    suspend fun dispararAlertaCuidador(@Body body: AlertaCuidadorCreateDto): AlertaCuidadorDto

    @PATCH("cuidador/alertas/{id}/atender")
    suspend fun marcarAlertaCuidadorAtendida(@Path("id") idAlerta: Int): AlertaCuidadorDto

    @POST("medicamentos")
    suspend fun crearMedicamento(@Body body: MedicamentoCreateDto): MedicamentoDto

    @GET("medicamentos")
    suspend fun listarMedicamentos(): List<MedicamentoDto>

    @PUT("medicamentos/{id}")
    suspend fun actualizarMedicamento(
        @Path("id") idMedicamento: Int,
        @Body body: MedicamentoCreateDto
    ): MedicamentoDto

    @PATCH("medicamentos/{id}/stock")
    suspend fun actualizarStock(
        @Path("id") idMedicamento: Int,
        @Body body: StockUpdateDto
    ): MedicamentoDto

    @DELETE("medicamentos/{id}")
    suspend fun eliminarMedicamento(@Path("id") idMedicamento: Int): Response<Unit>

    @GET("medicamentos/catalogo")
    suspend fun buscarCatalogo(@Query("q") query: String? = null): List<MedicamentoCatalogoItemDto>

    @POST("medicamentos/verificar-alergias")
    suspend fun verificarAlergias(@Body body: VerificarAlergiasInDto): VerificarAlergiasOutDto

    @POST("tratamientos")
    suspend fun crearTratamiento(@Body body: TratamientoCreateDto): TratamientoDto

    @GET("tratamientos")
    suspend fun listarTratamientos(): List<TratamientoDto>

    @GET("recordatorios")
    suspend fun listarRecordatorios(
        @Query("fecha") fecha: String? = null,
        @Query("tz_offset_minutes") tzOffsetMinutes: Int? = null
    ): List<RecordatorioDto>

    @POST("recordatorios/{id}/tomar")
    suspend fun tomarRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto

    @POST("recordatorios/{id}/posponer")
    suspend fun posponerRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto

    @POST("recordatorios/{id}/omitir")
    suspend fun omitirRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto

    @POST("recordatorios/{id}/revertir")
    suspend fun revertirRecordatorio(@Path("id") idRecordatorio: Int): RecordatorioDto

    // --- Sistema de Alergias ---
    @GET("alergias")
    suspend fun listarAlergias(): List<AlergiaDto>

    @POST("alergias")
    suspend fun agregarAlergia(@Body body: AlergiaCreateDto): AlergiaDto

    @DELETE("alergias/{id}")
    suspend fun eliminarAlergia(@Path("id") idAlergia: Int): Response<Unit>

    // --- Contactos de Apoyo / Emergencia ---
    @GET("contactos-apoyo")
    suspend fun listarContactos(): List<ContactoApoyoDto>

    @POST("contactos-apoyo")
    suspend fun agregarContacto(@Body body: ContactoApoyoCreateDto): ContactoApoyoDto

    @PUT("contactos-apoyo/{id}")
    suspend fun actualizarContacto(
        @Path("id") idContacto: Int,
        @Body body: ContactoApoyoCreateDto
    ): ContactoApoyoDto

    @DELETE("contactos-apoyo/{id}")
    suspend fun eliminarContacto(@Path("id") idContacto: Int): Response<Unit>

    // --- Motor IA Clínico Ollama (medi-clinico) ---
    @POST("ai/chat")
    suspend fun consultarMediAi(@Body body: AiChatRequestDto): AiChatResponseDto

    @POST("ai/sugerir-medicamento")
    suspend fun sugerirMedicamentoAi(@Body body: AiMedicationSuggestRequestDto): AiMedicationSuggestResponseDto

    @POST("ai/analizar-receta")
    suspend fun analizarRecetaAi(@Body body: AiPrescriptionScanRequestDto): AiPrescriptionScanResponseDto
}

