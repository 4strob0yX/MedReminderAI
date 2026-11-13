package com.medreminder.ai.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST

interface AuthApi {
    @POST("auth/register")
    suspend fun register(@Body body: RegisterRequest): TokenResponse

    @POST("auth/login")
    suspend fun login(@Body body: LoginRequest): TokenResponse

    @POST("auth/refresh")
    suspend fun refresh(@Body body: RefreshRequest): TokenResponse

    @POST("auth/forgot-password")
    suspend fun forgotPassword(@Body body: ForgotPasswordRequest): ForgotPasswordResponse

    @POST("auth/reset-password")
    suspend fun resetPassword(@Body body: ResetPasswordRequest): ResetPasswordResponse

    @GET("auth/me")
    suspend fun me(): UsuarioDto

    @PATCH("auth/me")
    suspend fun actualizarPerfil(@Body body: UpdatePerfilRequestDto): UsuarioDto

    @POST("auth/change-password")
    suspend fun changePassword(@Body body: ChangePasswordRequestDto): SimpleMensajeResponseDto
}

