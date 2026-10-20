package com.medreminder.ai.data.local

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

/** Almacenamiento cifrado de JWT (access + refresh) con recuperación ante corrupción de Keystore. */
class TokenStore(context: Context) {

    private val prefs: SharedPreferences = createSafePrefs(context)

    private fun createSafePrefs(context: Context): SharedPreferences {
        return try {
            createEncryptedPrefs(context)
        } catch (_: Exception) {
            runCatching { context.deleteSharedPreferences(PREFS_FILE) }
            try {
                createEncryptedPrefs(context)
            } catch (_: Exception) {
                context.getSharedPreferences("${PREFS_FILE}_fallback", Context.MODE_PRIVATE)
            }
        }
    }

    private fun createEncryptedPrefs(context: Context): SharedPreferences {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
        return EncryptedSharedPreferences.create(
            context,
            PREFS_FILE,
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    var accessToken: String?
        get() = prefs.getString(KEY_ACCESS, null)
        private set(value) = prefs.edit().putString(KEY_ACCESS, value).apply()

    var refreshToken: String?
        get() = prefs.getString(KEY_REFRESH, null)
        private set(value) = prefs.edit().putString(KEY_REFRESH, value).apply()

    var lastWorkingHost: String?
        get() = prefs.getString(KEY_LAST_HOST, null)
        set(value) = prefs.edit().putString(KEY_LAST_HOST, value).apply()

    fun save(access: String, refresh: String) {
        prefs.edit()
            .putString(KEY_ACCESS, access)
            .putString(KEY_REFRESH, refresh)
            .apply()
    }

    fun clear() = prefs.edit().clear().apply()

    private companion object {
        const val PREFS_FILE = "secure_auth_prefs"
        const val KEY_ACCESS = "access_token"
        const val KEY_REFRESH = "refresh_token"
        const val KEY_LAST_HOST = "last_working_host"
    }
}

