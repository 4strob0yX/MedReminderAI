package com.medreminder.ai.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface AuthApi {
    @POST("auth/register")
    suspend fun register(@Body body: RegisterRequest): TokenResponse

    @POST("auth/login")
    suspend fun login(@Body body: LoginRequest): TokenResponse

    @POST("auth/refresh")
    suspend fun refresh(@Body body: RefreshRequest): TokenResponse

    @POST("auth/reset-password")
    suspend fun resetPassword(@Body body: ResetPasswordRequest): ResetPasswordResponse

    @GET("auth/me")
    suspend fun me(): UsuarioDto
}

