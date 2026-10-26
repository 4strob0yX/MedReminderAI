package com.medreminder.ai.data.repository

import com.medreminder.ai.data.local.TokenStore
import com.medreminder.ai.data.remote.AuthApi
import com.medreminder.ai.data.remote.LoginRequest
import com.medreminder.ai.data.remote.RegisterRequest
import com.medreminder.ai.data.remote.ResetPasswordRequest
import com.medreminder.ai.data.remote.TokenResponse
import com.medreminder.ai.data.remote.parseApiErrorDetail
import kotlinx.coroutines.CancellationException
import retrofit2.HttpException
import java.io.IOException

class AuthRepository(
    private val api: AuthApi,
    private val tokenStore: TokenStore
) {
    fun isLoggedIn(): Boolean = tokenStore.accessToken != null

    suspend fun login(email: String, password: String): Result<Unit> =
        call { api.login(LoginRequest(email, password)) }

    suspend fun register(
        nombre: String,
        email: String,
        password: String,
        fechaNacimiento: String? = null,
        rol: String = "paciente"
    ): Result<Unit> =
        call {
            api.register(
                RegisterRequest(
                    nombre = nombre,
                    email = email,
                    password = password,
                    fechaNacimiento = fechaNacimiento?.trim()?.ifBlank { null },
                    rol = rol
                )
            )
        }

    suspend fun resetPassword(email: String, newPassword: String): Result<String> =
        try {
            val res = api.resetPassword(ResetPasswordRequest(email = email.trim(), newPassword = newPassword))
            Result.success(res.message ?: res.detail ?: "Contraseña actualizada correctamente.")
        } catch (e: CancellationException) {
            throw e
        } catch (e: HttpException) {
            val detail = parseApiErrorDetail(e.response()?.errorBody()?.string())
            Result.failure(AuthException(detail ?: "No se pudo restablecer la contraseña (${e.code()})"))
        } catch (e: IOException) {
            Result.failure(AuthException("Se requiere conexión a internet."))
        } catch (e: Exception) {
            Result.failure(AuthException(e.message ?: "Error al restablecer la contraseña"))
        }

    fun logout() = tokenStore.clear()

    private suspend fun call(block: suspend () -> TokenResponse): Result<Unit> =
        try {
            val tokens = block()
            tokenStore.save(tokens.accessToken, tokens.refreshToken)
            Result.success(Unit)
        } catch (e: CancellationException) {
            throw e
        } catch (e: HttpException) {
            val detail = parseApiErrorDetail(e.response()?.errorBody()?.string())
            Result.failure(AuthException(detail ?: "Error del servidor (${e.code()})"))
        } catch (e: IOException) {
            Result.failure(AuthException("Se requiere conexión a internet."))
        } catch (e: Exception) {
            Result.failure(AuthException(e.message ?: "Error inesperado de autenticación"))
        }
}

class AuthException(message: String) : Exception(message)

