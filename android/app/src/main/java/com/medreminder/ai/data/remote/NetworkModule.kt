package com.medreminder.ai.data.remote

import com.google.gson.Gson
import com.medreminder.ai.BuildConfig
import com.medreminder.ai.data.local.TokenStore
import okhttp3.Authenticator
import okhttp3.Interceptor
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import okhttp3.Route
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.IOException
import java.util.concurrent.TimeUnit

/** Configuración de Retrofit con Authenticator para auto-refresco de JWT y conmutación inteligente de host (USB / Wi-Fi / Emulador). */
class NetworkModule(private val tokenStore: TokenStore) {

    private val gson = Gson()
    private val refreshLock = Any()

    companion object {
        // Direcciones candidatas en red local de desarrollo:
        // 192.168.0.242: IP Wi-Fi de la máquina host (permite usar el móvil sin cable USB)
        // 127.0.0.1: Conexión mediante adb reverse sobre USB
        // 10.0.2.2: Loopback estándar del emulador de Android Studio
        val CANDIDATE_HOSTS = listOf("192.168.0.242", "127.0.0.1", "10.0.2.2")
        @Volatile
        var activeHost: String? = null
    }

    init {
        if (activeHost == null) {
            activeHost = tokenStore.lastWorkingHost ?: "192.168.0.242"
        }
    }

    private val dynamicHostInterceptor = Interceptor { chain ->
        val originalRequest = chain.request()
        val originalUrl = originalRequest.url
        val currentHost = originalUrl.host

        val isLocalDev = currentHost in CANDIDATE_HOSTS || currentHost == "localhost"
        if (!isLocalDev) {
            return@Interceptor chain.proceed(originalRequest)
        }

        val hostsToTry = linkedSetOf<String>()
        activeHost?.let { hostsToTry.add(it) }
        tokenStore.lastWorkingHost?.let { hostsToTry.add(it) }
        hostsToTry.addAll(CANDIDATE_HOSTS)

        var lastException: IOException? = null
        for (candidate in hostsToTry) {
            val candidateUrl = originalUrl.newBuilder().host(candidate).build()
            val candidateRequest = originalRequest.newBuilder().url(candidateUrl).build()
            try {
                val response = chain.proceed(candidateRequest)
                if (activeHost != candidate) {
                    activeHost = candidate
                    tokenStore.lastWorkingHost = candidate
                }
                return@Interceptor response
            } catch (e: IOException) {
                lastException = e
            }
        }
        throw lastException ?: IOException("Sin conexión con el servidor. Verifica tu red Wi-Fi o conexión USB.")
    }

    private val authInterceptor = Interceptor { chain ->
        val builder = chain.request().newBuilder()
        tokenStore.accessToken?.let { builder.addHeader("Authorization", "Bearer $it") }
        chain.proceed(builder.build())
    }

    private val refreshClient: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(6, TimeUnit.SECONDS)
        .readTimeout(8, TimeUnit.SECONDS)
        .addInterceptor(dynamicHostInterceptor)
        .build()

    private val tokenAuthenticator = Authenticator { _: Route?, response: Response ->
        val path = response.request.url.encodedPath
        if (path.endsWith("/auth/login") ||
            path.endsWith("/auth/register") ||
            path.endsWith("/auth/refresh") ||
            path.endsWith("/auth/reset-password") ||
            responseCount(response) >= 2
        ) {
            return@Authenticator null
        }

        synchronized(refreshLock) {
            val currentAccess = tokenStore.accessToken
            val requestAccess = response.request.header("Authorization")?.removePrefix("Bearer ")?.trim()

            // Si otro hilo ya refrescó el token, reintentar con el nuevo access token
            if (!currentAccess.isNullOrBlank() && currentAccess != requestAccess) {
                return@Authenticator response.request.newBuilder()
                    .header("Authorization", "Bearer $currentAccess")
                    .build()
            }

            val refreshTok = tokenStore.refreshToken ?: return@Authenticator null
            val refreshUrl = BuildConfig.API_BASE_URL.trimEnd('/') + "/auth/refresh"
            val bodyJson = gson.toJson(RefreshRequest(refreshToken = refreshTok))
            val refreshReq = Request.Builder()
                .url(refreshUrl)
                .post(bodyJson.toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()

            val newTokens = runCatching {
                refreshClient.newCall(refreshReq).execute().use { refreshResp ->
                    if (refreshResp.isSuccessful) {
                        val raw = refreshResp.body?.string()
                        gson.fromJson(raw, TokenResponse::class.java)
                    } else {
                        if (refreshResp.code == 401 || refreshResp.code == 403) {
                            tokenStore.clear()
                        }
                        null
                    }
                }
            }.getOrNull()

            if (newTokens != null && newTokens.accessToken.isNotBlank()) {
                tokenStore.save(newTokens.accessToken, newTokens.refreshToken.ifBlank { refreshTok })
                response.request.newBuilder()
                    .header("Authorization", "Bearer ${newTokens.accessToken}")
                    .build()
            } else {
                null
            }
        }
    }

    private fun responseCount(response: Response): Int {
        var count = 1
        var prior = response.priorResponse
        while (prior != null) {
            count++
            prior = prior.priorResponse
        }
        return count
    }

    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.SECONDS)
        .addInterceptor(dynamicHostInterceptor)
        .addInterceptor(authInterceptor)
        .authenticator(tokenAuthenticator)
        .apply {
            if (BuildConfig.DEBUG) {
                // Nunca registrar BODY: contiene credenciales y datos médicos.
                addInterceptor(HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BASIC))
            }
        }
        .build()

    private val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .client(client)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    val authApi: AuthApi = retrofit.create(AuthApi::class.java)
    val medApi: MedApi = retrofit.create(MedApi::class.java)
}
