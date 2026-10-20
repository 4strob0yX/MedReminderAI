package com.medreminder.ai.data.remote

import com.google.gson.JsonParser
import com.google.gson.annotations.SerializedName

data class LoginRequest(
    val email: String,
    val password: String
)

data class RegisterRequest(
    val nombre: String,
    val email: String,
    val password: String
)

data class RefreshRequest(
    @SerializedName("refresh_token") val refreshToken: String
)

data class ResetPasswordRequest(
    val email: String,
    @SerializedName("new_password") val newPassword: String
)

data class ResetPasswordResponse(
    val message: String? = null,
    val detail: String? = null
)

data class UsuarioDto(
    @SerializedName("id_usuario") val idUsuario: Int,
    val nombre: String,
    val email: String
)

data class TokenResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("refresh_token") val refreshToken: String,
    @SerializedName("token_type") val tokenType: String = "bearer"
)

/**
 * Formato de error por defecto de FastAPI:
 * - 400/401/404/409: {"detail": "Mensaje de error"}
 * - 422 Validación Pydantic: {"detail": [{"loc": ["body", "campo"], "msg": "...", "type": "..."}]}
 */
data class ApiError(val detail: Any?)

fun parseApiErrorDetail(rawJson: String?): String? {
    if (rawJson.isNullOrBlank()) return null
    return runCatching {
        val root = JsonParser.parseString(rawJson)
        if (!root.isJsonObject) return@runCatching null
        val detailEl = root.asJsonObject.get("detail") ?: return@runCatching null
        when {
            detailEl.isJsonPrimitive -> detailEl.asString
            detailEl.isJsonArray -> {
                val messages = detailEl.asJsonArray.mapNotNull { item ->
                    if (item.isJsonObject) {
                        val obj = item.asJsonObject
                        val msg = obj.get("msg")?.takeIf { it.isJsonPrimitive }?.asString
                        val loc = obj.get("loc")?.takeIf { it.isJsonArray }?.asJsonArray
                            ?.lastOrNull()?.takeIf { it.isJsonPrimitive }?.asString
                        if (msg != null && loc != null && loc != "body") "$loc: $msg" else msg
                    } else if (item.isJsonPrimitive) {
                        item.asString
                    } else null
                }
                messages.joinToString("; ").ifBlank { null }
            }
            else -> detailEl.toString()
        }
    }.getOrNull()
}

