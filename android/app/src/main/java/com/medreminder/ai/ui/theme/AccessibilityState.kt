package com.medreminder.ai.ui.theme

import android.content.Context
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

enum class ThemeMode(val label: String, val description: String) {
    CALIDO_AMIGABLE(
        label = "Cálido y Amigable",
        description = "Crema cálido (#FAF7F2) y verde salvia suave sin fatiga visual"
    ),
    ALTO_CONTRASTE_DIA(
        label = "Alto Contraste Día",
        description = "Contraste máximo 21:1 (WCAG AAA) sobre blanco puro y bordes de 2dp"
    ),
    ALTO_CONTRASTE_NOCHE(
        label = "Alto Contraste Noche",
        description = "Modo oscuro OLED (#0D1315) con acentos ámbar/turquesa para fotofobia o cataratas"
    )
}

enum class FontScaleMode(val label: String, val scaleFactor: Float) {
    NORMAL(label = "Normal (100%)", scaleFactor = 1.0f),
    GRANDE(label = "Grande (122%)", scaleFactor = 1.22f),
    EXTRA_GRANDE(label = "Extra Grande (138%)", scaleFactor = 1.38f)
}

@Immutable
data class AccessibilitySettings(
    val themeMode: ThemeMode = ThemeMode.CALIDO_AMIGABLE,
    val fontScaleMode: FontScaleMode = FontScaleMode.NORMAL,
    val daltonismoSeguro: Boolean = false,
    val vozActiva: Boolean = true,
    val onThemeModeChange: (ThemeMode) -> Unit = {},
    val onFontScaleModeChange: (FontScaleMode) -> Unit = {},
    val onDaltonismoChange: (Boolean) -> Unit = {},
    val onVozActivaChange: (Boolean) -> Unit = {}
) {
    val isHighContrast: Boolean
        get() = themeMode == ThemeMode.ALTO_CONTRASTE_DIA || themeMode == ThemeMode.ALTO_CONTRASTE_NOCHE

    val isDarkTheme: Boolean
        get() = themeMode == ThemeMode.ALTO_CONTRASTE_NOCHE

    val borderWidth: Dp
        get() = if (isHighContrast) 2.5.dp else 1.dp

    val adaptiveBackground: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> AppBackground
            ThemeMode.ALTO_CONTRASTE_DIA -> HighContrastDayBg
            ThemeMode.ALTO_CONTRASTE_NOCHE -> HighContrastNightBg
        }

    val adaptiveCardSurface: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> CardBackground
            ThemeMode.ALTO_CONTRASTE_DIA -> HighContrastDaySurface
            ThemeMode.ALTO_CONTRASTE_NOCHE -> HighContrastNightSurface
        }

    val adaptiveSoftSurface: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> SoftWarmSurface
            ThemeMode.ALTO_CONTRASTE_DIA -> Color(0xFFF5F5F5)
            ThemeMode.ALTO_CONTRASTE_NOCHE -> Color(0xFF141C20)
        }

    val adaptivePrimary: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> if (daltonismoSeguro) OkabeBlue else TealPrimary
            ThemeMode.ALTO_CONTRASTE_DIA -> if (daltonismoSeguro) OkabeBlue else HighContrastDayPrimary
            ThemeMode.ALTO_CONTRASTE_NOCHE -> if (daltonismoSeguro) OkabeSky else HighContrastNightTeal
        }

    val adaptiveTextPrimary: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> TextPrimary
            ThemeMode.ALTO_CONTRASTE_DIA -> HighContrastDayText
            ThemeMode.ALTO_CONTRASTE_NOCHE -> HighContrastNightText
        }

    val adaptiveTextSecondary: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> TextSecondary
            ThemeMode.ALTO_CONTRASTE_DIA -> Color(0xFF000000)
            ThemeMode.ALTO_CONTRASTE_NOCHE -> HighContrastNightSecondary
        }

    val adaptiveBorder: Color
        get() = when (themeMode) {
            ThemeMode.CALIDO_AMIGABLE -> InputBorderColor
            ThemeMode.ALTO_CONTRASTE_DIA -> HighContrastDayBorder
            ThemeMode.ALTO_CONTRASTE_NOCHE -> HighContrastNightBorder
        }

    fun resolveStatusColor(estado: String): Color {
        return when (estado.lowercase()) {
            "tomado", "optimo", "óptimo" -> if (daltonismoSeguro) OkabeBlue else ColorTomado
            "pospuesto", "normal" -> if (daltonismoSeguro) OkabeAmber else ColorPospuesto
            "omitido", "bajo", "critico", "crítico" -> if (daltonismoSeguro) OkabeVermilion else ColorOmitido
            else -> if (daltonismoSeguro) OkabeSky else ColorPendiente
        }
    }
}

val LocalAccessibilitySettings = staticCompositionLocalOf { AccessibilitySettings() }

/**
 * Gestor reactivo y persistente en SharedPreferences de las preferencias de accesibilidad
 * (Tema visual, Escala tipográfica, Modo Daltonismo Okabe-Ito y Lectura por Voz TTS).
 */
object AccessibilityPreferences {
    private const val PREFS_NAME = "medreminder_accessibility_prefs"
    private const val KEY_THEME_MODE = "theme_mode"
    private const val KEY_FONT_SCALE = "font_scale_mode"
    private const val KEY_DALTONISMO = "daltonismo_seguro"
    private const val KEY_VOZ_ACTIVA = "voz_activa"

    private val _state = MutableStateFlow(AccessibilitySettings())
    val state: StateFlow<AccessibilitySettings> = _state.asStateFlow()

    @Volatile
    private var initialized = false

    fun ensureLoaded(context: Context) {
        if (initialized) return
        synchronized(this) {
            if (initialized) return
            val prefs = context.applicationContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            val themeName = prefs.getString(KEY_THEME_MODE, ThemeMode.CALIDO_AMIGABLE.name)
            val scaleName = prefs.getString(KEY_FONT_SCALE, FontScaleMode.NORMAL.name)
            val daltonismo = prefs.getBoolean(KEY_DALTONISMO, false)
            val voz = prefs.getBoolean(KEY_VOZ_ACTIVA, true)

            val theme = runCatching { ThemeMode.valueOf(themeName ?: ThemeMode.CALIDO_AMIGABLE.name) }
                .getOrDefault(ThemeMode.CALIDO_AMIGABLE)
            val scale = runCatching { FontScaleMode.valueOf(scaleName ?: FontScaleMode.NORMAL.name) }
                .getOrDefault(FontScaleMode.NORMAL)

            _state.value = AccessibilitySettings(
                themeMode = theme,
                fontScaleMode = scale,
                daltonismoSeguro = daltonismo,
                vozActiva = voz
            )
            initialized = true
        }
    }

    fun setThemeMode(context: Context, mode: ThemeMode) {
        ensureLoaded(context)
        context.applicationContext
            .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_THEME_MODE, mode.name)
            .apply()
        _state.update { it.copy(themeMode = mode) }
    }

    fun setFontScaleMode(context: Context, scaleMode: FontScaleMode) {
        ensureLoaded(context)
        context.applicationContext
            .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_FONT_SCALE, scaleMode.name)
            .apply()
        _state.update { it.copy(fontScaleMode = scaleMode) }
    }

    fun setDaltonismoSeguro(context: Context, enabled: Boolean) {
        ensureLoaded(context)
        context.applicationContext
            .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit()
            .putBoolean(KEY_DALTONISMO, enabled)
            .apply()
        _state.update { it.copy(daltonismoSeguro = enabled) }
    }

    fun setVozActiva(context: Context, enabled: Boolean) {
        ensureLoaded(context)
        context.applicationContext
            .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            .edit()
            .putBoolean(KEY_VOZ_ACTIVA, enabled)
            .apply()
        _state.update { it.copy(vozActiva = enabled) }
    }
}
