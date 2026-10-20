package com.medreminder.ai.ui.theme

import android.app.Activity
import androidx.activity.enableEdgeToEdge
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.unit.Density
import androidx.core.view.WindowCompat

private val MedWarmLightColorScheme = lightColorScheme(
    primary = TealPrimary,
    onPrimary = Color.White,
    primaryContainer = TealSoftBg,
    onPrimaryContainer = TealDark,
    secondary = TealBadgeText,
    onSecondary = Color.White,
    secondaryContainer = TealBadgeBg,
    onSecondaryContainer = TealDark,
    background = AppBackground,
    onBackground = TextPrimary,
    surface = CardBackground,
    onSurface = TextPrimary,
    surfaceVariant = SoftWarmSurface,
    onSurfaceVariant = TextSecondary,
    outline = InputBorderColor,
    error = AlertRedText
)

private val MedHighContrastDayColorScheme = lightColorScheme(
    primary = HighContrastDayPrimary,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFD0E4E8),
    onPrimaryContainer = Color.Black,
    secondary = Color.Black,
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFE6EEF0),
    onSecondaryContainer = Color.Black,
    background = HighContrastDayBg,
    onBackground = HighContrastDayText,
    surface = HighContrastDaySurface,
    onSurface = HighContrastDayText,
    surfaceVariant = Color(0xFFF0F4F5),
    onSurfaceVariant = Color.Black,
    outline = HighContrastDayBorder,
    error = Color(0xFF900000)
)

private val MedHighContrastNightColorScheme = darkColorScheme(
    primary = HighContrastNightTeal,
    onPrimary = Color(0xFF002022),
    primaryContainer = Color(0xFF1B3A40),
    onPrimaryContainer = HighContrastNightText,
    secondary = HighContrastNightAccent,
    onSecondary = Color.Black,
    secondaryContainer = Color(0xFF28383E),
    onSecondaryContainer = HighContrastNightAccent,
    background = HighContrastNightBg,
    onBackground = HighContrastNightText,
    surface = HighContrastNightSurface,
    onSurface = HighContrastNightText,
    surfaceVariant = Color(0xFF1F2D33),
    onSurfaceVariant = HighContrastNightSecondary,
    outline = HighContrastNightBorder,
    error = Color(0xFFFF6B6B)
)

@Composable
fun MedReminderAITheme(
    darkTheme: Boolean = false,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val context = LocalContext.current
    remember(context) {
        AccessibilityPreferences.ensureLoaded(context)
        true
    }

    val rawSettings by AccessibilityPreferences.state.collectAsState()
    val settings = remember(rawSettings, context) {
        rawSettings.copy(
            onThemeModeChange = { AccessibilityPreferences.setThemeMode(context, it) },
            onFontScaleModeChange = { AccessibilityPreferences.setFontScaleMode(context, it) },
            onDaltonismoChange = { AccessibilityPreferences.setDaltonismoSeguro(context, it) },
            onVozActivaChange = { AccessibilityPreferences.setVozActiva(context, it) }
        )
    }

    val baseColorScheme = when {
        settings.themeMode == ThemeMode.ALTO_CONTRASTE_NOCHE || darkTheme -> MedHighContrastNightColorScheme
        settings.themeMode == ThemeMode.ALTO_CONTRASTE_DIA -> MedHighContrastDayColorScheme
        else -> MedWarmLightColorScheme
    }

    val effectiveColorScheme = if (settings.daltonismoSeguro) {
        when (settings.themeMode) {
            ThemeMode.ALTO_CONTRASTE_NOCHE -> baseColorScheme.copy(
                primary = OkabeSky,
                secondary = OkabeAmber,
                error = OkabeVermilion
            )
            else -> baseColorScheme.copy(
                primary = OkabeBlue,
                secondary = OkabeBluishGreen,
                error = OkabeVermilion
            )
        }
    } else {
        baseColorScheme
    }

    val baseDensity = LocalDensity.current
    val scaledDensity = remember(baseDensity, settings.fontScaleMode) {
        Density(
            density = baseDensity.density,
            fontScale = baseDensity.fontScale * settings.fontScaleMode.scaleFactor
        )
    }

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val activity = view.context as? androidx.activity.ComponentActivity
            val isDark = settings.themeMode == ThemeMode.ALTO_CONTRASTE_NOCHE ||
                (darkTheme && settings.themeMode == ThemeMode.CALIDO_AMIGABLE)
            if (activity != null) {
                if (isDark) {
                    activity.enableEdgeToEdge(
                        statusBarStyle = androidx.activity.SystemBarStyle.dark(android.graphics.Color.TRANSPARENT),
                        navigationBarStyle = androidx.activity.SystemBarStyle.dark(android.graphics.Color.TRANSPARENT)
                    )
                } else {
                    activity.enableEdgeToEdge(
                        statusBarStyle = androidx.activity.SystemBarStyle.light(
                            android.graphics.Color.TRANSPARENT,
                            android.graphics.Color.TRANSPARENT
                        ),
                        navigationBarStyle = androidx.activity.SystemBarStyle.light(
                            android.graphics.Color.TRANSPARENT,
                            android.graphics.Color.TRANSPARENT
                        )
                    )
                }
            } else {
                val window = (view.context as? Activity)?.window
                if (window != null) {
                    val insetsController = WindowCompat.getInsetsController(window, view)
                    insetsController.isAppearanceLightStatusBars = !isDark
                    insetsController.isAppearanceLightNavigationBars = !isDark
                }
            }
        }
    }

    CompositionLocalProvider(
        LocalAccessibilitySettings provides settings,
        LocalDensity provides scaledDensity
    ) {
        MaterialTheme(
            colorScheme = effectiveColorScheme,
            typography = Typography,
            content = content
        )
    }
}

@Composable
fun MedReminderTheme(
    darkTheme: Boolean = false,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    MedReminderAITheme(
        darkTheme = darkTheme,
        dynamicColor = dynamicColor,
        content = content
    )
}