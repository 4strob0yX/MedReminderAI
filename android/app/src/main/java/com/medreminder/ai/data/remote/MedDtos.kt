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

