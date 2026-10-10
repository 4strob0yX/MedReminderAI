package com.medreminder.ai.data.repository

import com.google.gson.Gson
import com.medreminder.ai.data.local.TokenStore
import com.medreminder.ai.data.remote.ApiError
import com.medreminder.ai.data.remote.AuthApi
import com.medreminder.ai.data.remote.LoginRequest
import com.medreminder.ai.data.remote.RegisterRequest
import com.medreminder.ai.data.remote.TokenResponse
import retrofit2.HttpException
import java.io.IOException

class AuthRepository(
    private val api: AuthApi,
    private val tokenStore: TokenStore
) {
    fun isLoggedIn(): Boolean = tokenStore.accessToken != null

    suspend fun login(email: String, password: String): Result<Unit> =
        call { api.login(LoginRequest(email, password)) }

    suspend fun register(nombre: String, email: String, password: String): Result<Unit> =
        call { api.register(RegisterRequest(nombre, email, password)) }

    fun logout() = tokenStore.clear()

    private suspend fun call(block: suspend () -> TokenResponse): Result<Unit> =
        try {
            val tokens = block()
            tokenStore.save(tokens.accessToken, tokens.refreshToken)
            Result.success(Unit)
        } catch (e: HttpException) {
            val detail = runCatching {
                Gson().fromJson(e.response()?.errorBody()?.string(), ApiError::class.java)?.detail
            }.getOrNull()
            Result.failure(AuthException(detail ?: "Error del servidor (${e.code()})"))
        } catch (e: IOException) {
            Result.failure(AuthException("Se requiere conexión a internet."))
        }
}

class AuthException(message: String) : Exception(message)
