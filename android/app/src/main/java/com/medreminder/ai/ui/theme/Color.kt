package com.medreminder.ai.ui.theme

import androidx.compose.ui.graphics.Color

// ============================================================================
// 1. PALETA CLÍNICA CÁLIDA Y AMIGABLE (WCAG AA/AAA Contrast Enhanced)
// ============================================================================
// Paleta "Aurora" futurista: cian-turquesa luminoso con superficies de neblina fría
val TealPrimary = Color(0xFF007C91)
val TealDark = Color(0xFF05505F)
val TealSoftBg = Color(0xFFDDF6F8)
val TealSoft = Color(0xFFDDF6F8)
val TealBadgeBg = Color(0xFFD0F3F6)
val TealBadgeText = Color(0xFF05505F)
val CyanIconBg = Color(0xFFB5ECFC)
val CyanIconTint = Color(0xFF0B4F60)
val AuroraCyan = Color(0xFF00E5FF)
val AuroraMint = Color(0xFF38EF7D)
val AuroraViolet = Color(0xFF7C4DFF)

// Superficies de neblina fría con leve tinte aqua
val AppBackground = Color(0xFFF1FAFB)
val WarmSurface = Color(0xFFF1FAFB)
val CardBackground = Color(0xFFFFFFFF)
val SoftWarmSurface = Color(0xFFE6F5F7)
val InputBorderColor = Color(0xFFB4D4DA)

// Tipografía con alto contraste real (WCAG AA / AAA)
val TextPrimary = Color(0xFF14181A)
val TextSecondary = Color(0xFF3A454A) // Contraste 9.8:1 (antes #60686C)
val TextMuted = Color(0xFF525E64)     // Contraste 6.6:1 (antes #939B9F ilegible)

// Alertas y estados clínicos
val AlertRedText = Color(0xFF9E2A2B)
val AlertRedBg = Color(0xFFFBE9E7)
val OmitBrownText = Color(0xFF5D3A1A)
val ProgressBrown = Color(0xFF7A4419)

val DangerAccent = Color(0xFFC62828)
val DangerSurface = Color(0xFFFFEBEE)
val CriticalAlertBg = Color(0xFFFFEBEE)
val CriticalAlertText = Color(0xFFB71C1C)

val SuccessBadgeBg = Color(0xFFE6F4EA)
val SuccessBadgeText = Color(0xFF1E6F3D)
val WarningBadgeBg = Color(0xFFFFF3E0)
val WarningBadgeText = Color(0xFFB25000)

// Colores semánticos de estado de toma
val ColorTomado = Color(0xFF1E7E52)
val ColorPospuesto = Color(0xFFD97706)
val ColorOmitido = Color(0xFFC62828)
val ColorPendiente = Color(0xFF286675)

// ============================================================================
// 2. GAMIFICACIÓN: RACHAS DE FUEGO EVOLUTIVO (ESTILO TIKTOK) Y RANGOS DE HONOR
// ============================================================================
val FlameOrange = Color(0xFFFF6B35)      // Racha 1-6 días (Fuego Naranja)
val FlameOrangeGlow = Color(0xFFFF9F1C)
val FlameBlue = Color(0xFF00B4D8)        // Racha 7-13 días (Fuego Azul Intenso)
val FlameBlueGlow = Color(0xFF90E0EF)
val FlamePurpleGold = Color(0xFF9D4EDD)  // Racha 14+ días (Fuego Morado/Dorado Legendario)
val FlameGoldAccent = Color(0xFFFFB703)
val FlameAsh = Color(0xFF8D99AE)         // Racha apagada (0 días / Ceniza)

val HonorIron = Color(0xFF6C757D)        // Hierro (En Riesgo / Penalizado)
val HonorBronze = Color(0xFFB07246)      // Bronce
val HonorSilver = Color(0xFF7A8B99)      // Plata
val HonorGold = Color(0xFFD4AF37)        // Oro
val HonorDiamond = Color(0xFF00B4D8)     // Diamante / Guardián
val HonorDishonorRed = Color(0xFF9E2A2B) // Emblema agrietado

// ============================================================================
// 3. ACCESIBILIDAD: PALETA OKABE-ITO (DALTONISMO SEGURO)
// ============================================================================
val OkabeBlue = Color(0xFF0072B2)        // Reemplaza verde en modo daltonismo (Tomado)
val OkabeAmber = Color(0xFFE69F00)       // Pospuesto / Precaución
val OkabeVermilion = Color(0xFFD55E00)   // Omitido / Alerta
val OkabePurple = Color(0xFFCC79A7)      // Dosis Crítica
val OkabeSky = Color(0xFF56B4E9)         // Pendiente
val OkabeBluishGreen = Color(0xFF009E73) // Secundario seguro

// ============================================================================
// 4. ACCESIBILIDAD: ALTO CONTRASTE DÍA (21:1) Y NOCHE (OLED FOTOFOBIA/CATARATAS)
// ============================================================================
val HighContrastDayBg = Color(0xFFFFFFFF)
val HighContrastDaySurface = Color(0xFFFFFFFF)
val HighContrastDayText = Color(0xFF000000)
val HighContrastDayPrimary = Color(0xFF000000)
val HighContrastDayBorder = Color(0xFF000000)

val HighContrastNightBg = Color(0xFF000000)
val HighContrastNightSurface = Color(0xFF0D1215)
val HighContrastNightText = Color(0xFFFFFFFF)
val HighContrastNightSecondary = Color(0xFFCBD5E1)
val HighContrastNightAccent = Color(0xFFFFD600)
val HighContrastNightTeal = Color(0xFF00E5FF)
val HighContrastNightBorder = Color(0xFF00E5FF)

// Compatibilidad Material 3 plantilla base
val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Pink80 = Color(0xFFEFB8C8)
val Purple40 = Color(0xFF286675)
val PurpleGrey40 = Color(0xFF3A454A)
val Pink40 = Color(0xFF7D5260)