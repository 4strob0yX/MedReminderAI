package com.medreminder.ai.di

import android.content.Context
import com.medreminder.ai.data.local.TokenStore
import com.medreminder.ai.data.remote.NetworkModule
import com.medreminder.ai.data.repository.AuthRepository

/** Contenedor de dependencias manual (instanciar en Application). */
class AppContainer(context: Context) {
    private val tokenStore = TokenStore(context)
    private val network = NetworkModule(tokenStore)
    val authRepository = AuthRepository(network.authApi, tokenStore)
}
