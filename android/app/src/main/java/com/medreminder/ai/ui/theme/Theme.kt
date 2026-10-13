package com.medreminder.ai.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val MedLightColorScheme = lightColorScheme(
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
    error = AlertRedText
)

@Composable
fun MedReminderAITheme(
    darkTheme: Boolean = false,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = MedLightColorScheme,
        typography = Typography,
        content = content
    )
}