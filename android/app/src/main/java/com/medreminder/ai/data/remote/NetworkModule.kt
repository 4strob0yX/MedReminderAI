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
        val BASE_CANDIDATES = listOf(
            "127.0.0.1",     // Conexión mediante adb reverse sobre USB
            "192.168.1.20",  // Mac host en red Wi-Fi actual
            "172.20.10.2",   // Mac host en Hotspot
            "192.168.0.228", // Mac host en red de hogar
            "192.168.0.242",
            "10.0.2.2"       // Loopback estándar del emulador de Android Studio
        )

        @Volatile
        var activeHost: String? = null

        /** Detecta dinámicamente el prefijo de la subred local (ej. 172.20.10. o 192.168.0.) para probar IPs comunes. */
        fun detectSubnetCandidates(): List<String> {
            val list = mutableListOf<String>()
            try {
                val interfaces = java.net.NetworkInterface.getNetworkInterfaces() ?: return list
                for (intf in interfaces) {
                    if (!intf.isUp || intf.isLoopback) continue
                    val addrs = intf.inetAddresses ?: continue
                    for (addr in addrs) {
                        if (!addr.isLoopbackAddress && addr is java.net.Inet4Address) {
                            val ip = addr.hostAddress ?: continue
                            if (ip.startsWith("192.168.") || ip.startsWith("172.") || ip.startsWith("10.")) {
                                val dot = ip.lastIndexOf('.')
                                if (dot != -1) {
                                    val prefix = ip.substring(0, dot + 1)
                                    list.add("${prefix}20")
                                    list.add("${prefix}2")
                                    list.add("${prefix}1")
                                    list.add("${prefix}228")
                                    list.add("${prefix}242")
                                    list.add("${prefix}100")
                                }
                            }
                        }
                    }
                }
            } catch (_: Exception) {}
            return list
        }

        fun getAllCandidates(): List<String> {
            return (listOf("127.0.0.1", "192.168.1.20", "172.20.10.2", "10.0.2.2") + detectSubnetCandidates() + BASE_CANDIDATES).distinct()
        }
    }

    init {
        if (activeHost == null) {
            activeHost = tokenStore.lastWorkingHost ?: "127.0.0.1"
        }
    }

    private val dynamicHostInterceptor = Interceptor { chain ->
        val originalRequest = chain.request()
        val originalUrl = originalRequest.url
        val currentHost = originalUrl.host

        val allCandidates = getAllCandidates()
        val isLocalDev = currentHost in allCandidates || currentHost == "localhost"
        if (!isLocalDev) {
            return@Interceptor chain.proceed(originalRequest)
        }

        val hostsToTry = linkedSetOf<String>()
        // Priorizar el host manual o el último funcional
        activeHost?.let { hostsToTry.add(it) }
        tokenStore.lastWorkingHost?.let { hostsToTry.add(it) }
        hostsToTry.addAll(allCandidates)

        var lastException: IOException? = null
        for (candidate in hostsToTry) {
            val candidateUrl = originalUrl.newBuilder().host(candidate).build()
            val candidateRequest = originalRequest.newBuilder().url(candidateUrl).build()
            try {
                // Timeout rápido de conexión (1.4s) al sondear candidatos alternativos para no colgar la UI
                val candidateChain = if (candidate == activeHost) chain else chain.withConnectTimeout(1400, TimeUnit.MILLISECONDS)
                val response = candidateChain.proceed(candidateRequest)
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
        .readTimeout(28, TimeUnit.SECONDS)
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
