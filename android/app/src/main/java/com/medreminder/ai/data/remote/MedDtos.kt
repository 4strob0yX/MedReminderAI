package com.medreminder.ai.data.remote

import com.google.gson.annotations.SerializedName

data class MedicamentoCreateDto(
    val nombre: String,
    val dosis: String,
    @SerializedName("cantidad_stock") val cantidadStock: Int
)

data class MedicamentoDto(
    @SerializedName("id_medicamento") val idMedicamento: Int,
    val nombre: String,
    val dosis: String,
    @SerializedName("cantidad_stock") val cantidadStock: Int
)

data class TratamientoCreateDto(
    @SerializedName("id_medicamento") val idMedicamento: Int,
    @SerializedName("frecuencia_horas") val frecuenciaHoras: Int,
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
    @SerializedName("veces_pospuesto") val vecesPospuesto: Int
)
