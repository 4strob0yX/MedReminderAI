package com.medreminder.ai.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.EaseInOutSine
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import kotlinx.coroutines.delay

/**
 * Pantalla de entrada animada (Splash Screen estilo YouTube) protagonizada por Medi,
 * la mascota clínica inteligente de MedReminder AI.
 *
 * Incluye:
 * - Entrada con resorte elástico (pop-in bounce) de Medi.
 * - Ondas de pulso biomédico / sonar concéntricas en expansión.
 * - Tipografía institucional con entrada secuencial escalonada.
 * - Microbarra de progreso con destello de sincronización clínica.
 * - Transición de salida suave estilo YouTube (zoom sutil + fade out hacia la app precargada).
 */
@Composable
fun MediSplashScreen(
    onSplashFinished: () -> Unit,
    modifier: Modifier = Modifier,
    minDisplayTimeMillis: Long = 1500L
) {
    val a11y = LocalAccessibilitySettings.current
    val isDark = a11y.isDarkTheme

    // Fondo adaptable: blanco clínico suave en claro o slate profundo en oscuro
    val backgroundColor = if (isDark) Color(0xFF0B132B) else Color(0xFFF8FAFC)
    val textPrimaryColor = if (isDark) Color(0xFFE2E8F0) else Color(0xFF0F172A)
    val textSecondaryColor = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B)

    // Estados de animación
    val entranceScale = remember { Animatable(0.72f) }
    val entranceAlpha = remember { Animatable(1f) }
    var showTexts by remember { mutableStateOf(true) }
    var isExiting by remember { mutableStateOf(false) }

    // Salida suave estilo YouTube: zoom ligero (1.06f) y desvanecimiento ágil (200ms)
    val exitAlpha by animateFloatAsState(
        targetValue = if (isExiting) 0f else 1f,
        animationSpec = tween(durationMillis = 200, easing = FastOutSlowInEasing),
        label = "splash_exit_alpha"
    )
    val exitScale by animateFloatAsState(
        targetValue = if (isExiting) 1.06f else 1f,
        animationSpec = tween(durationMillis = 200, easing = FastOutSlowInEasing),
        label = "splash_exit_scale"
    )

    // Ondas de pulso bio-acústico concéntricas en loop
    val pulseTransition = rememberInfiniteTransition(label = "pulse_rings")
    val pulseProgress1 by pulseTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "ring_1"
    )
    val pulseProgress2 by pulseTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, delayMillis = 600, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "ring_2"
    )

    // Destello de la barra de carga
    val shimmerOffset by pulseTransition.animateFloat(
        initialValue = -1f,
        targetValue = 2f,
        animationSpec = infiniteRepeatable(
            animation = tween(1400, easing = EaseInOutSine),
            repeatMode = RepeatMode.Restart
        ),
        label = "shimmer_bar"
    )

    LaunchedEffect(Unit) {
        // 1. Pop-in elástico rápido con resorte de Medi
        entranceScale.animateTo(
            targetValue = 1f,
            animationSpec = spring(
                dampingRatio = Spring.DampingRatioMediumBouncy,
                stiffness = Spring.StiffnessMedium
            )
        )

        // 2. Mantener tiempo ágil para precargar datos en segundo plano
        delay(minDisplayTimeMillis)

        // 3. Iniciar salida rápida estilo YouTube
        isExiting = true
        delay(200)

        // 4. Notificar finalización para desmontar el splash
        onSplashFinished()
    }

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(backgroundColor)
            .scale(exitScale)
            .alpha(exitAlpha),
        contentAlignment = Alignment.Center
    ) {
        // Ondas biomédicas en expansión concéntrica detrás de Medi
        Canvas(modifier = Modifier.size(260.dp)) {
            val cx = size.width / 2f
            val cy = size.height / 2f
            val maxRadius = size.width * 0.48f

            // Onda 1
            if (pulseProgress1 > 0f) {
                val r1 = maxRadius * pulseProgress1
                val a1 = (1f - pulseProgress1).coerceIn(0f, 1f) * 0.35f
                drawCircle(
                    color = Color(0xFF2DD4BF).copy(alpha = a1),
                    radius = r1,
                    center = Offset(cx, cy),
                    style = Stroke(width = (2.2.dp * (1f - pulseProgress1 * 0.5f)).toPx())
                )
            }

            // Onda 2
            if (pulseProgress2 > 0f) {
                val r2 = maxRadius * pulseProgress2
                val a2 = (1f - pulseProgress2).coerceIn(0f, 1f) * 0.30f
                drawCircle(
                    color = TealPrimary.copy(alpha = a2),
                    radius = r2,
                    center = Offset(cx, cy),
                    style = Stroke(width = (2.2.dp * (1f - pulseProgress2 * 0.5f)).toPx())
                )
            }
        }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.padding(horizontal = 24.dp)
        ) {
            // Mascota Medi en alta resolución con animación de vida
            Box(
                modifier = Modifier
                    .size(116.dp)
                    .scale(entranceScale.value)
                    .alpha(entranceAlpha.value),
                contentAlignment = Alignment.Center
            ) {
                MediMascotView(
                    size = 110.dp,
                    mood = MediMood.NORMAL,
                    animateHover = true
                )
            }

            Spacer(Modifier.height(28.dp))

            // Nombre institucional MedReminder AI
            AnimatedVisibility(
                visible = showTexts,
                enter = fadeIn(tween(400)) + slideInVertically(tween(400)) { 24 }
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "MedReminder",
                            fontSize = 30.sp,
                            fontWeight = FontWeight.Black,
                            color = textPrimaryColor,
                            letterSpacing = (-0.5).sp
                        )
                        Spacer(Modifier.width(6.dp))
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = TealPrimary
                        ) {
                            Text(
                                text = "AI",
                                fontSize = 16.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = Color.White,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                            )
                        }
                    }

                    Spacer(Modifier.height(8.dp))

                    Text(
                        text = "Tu copiloto clínico inteligente",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium,
                        color = textSecondaryColor,
                        textAlign = TextAlign.Center,
                        letterSpacing = 0.2.sp
                    )
                }
            }

            Spacer(Modifier.height(34.dp))

            // Micro-indicador de progreso estilo YouTube
            AnimatedVisibility(
                visible = showTexts,
                enter = fadeIn(tween(500, delayMillis = 200))
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .width(130.dp)
                            .height(4.dp)
                            .clip(RoundedCornerShape(50))
                            .background(if (isDark) Color(0xFF1E293B) else Color(0xFFE2E8F0))
                    ) {
                        // Resplandor de desplazamiento
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(
                                    Brush.horizontalGradient(
                                        colors = listOf(
                                            TealPrimary.copy(alpha = 0.2f),
                                            Color(0xFF2DD4BF),
                                            TealPrimary.copy(alpha = 0.2f)
                                        ),
                                        startX = shimmerOffset * 300f,
                                        endX = (shimmerOffset + 1f) * 300f
                                    )
                                )
                        )
                    }

                    Text(
                        text = "Sincronizando plan de salud...",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Medium,
                        color = textSecondaryColor.copy(alpha = 0.75f)
                    )
                }
            }
        }

        // Firma clínica en la parte inferior de la pantalla
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 32.dp),
            contentAlignment = Alignment.BottomCenter
        ) {
            AnimatedVisibility(
                visible = showTexts,
                enter = fadeIn(tween(600, delayMillis = 300))
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Surface(
                        shape = CircleShape,
                        color = Color(0xFF10B981),
                        modifier = Modifier.size(6.dp)
                    ) {}
                    Text(
                        text = "Motor de bioseguridad activo",
                        fontSize = 10.5.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = textSecondaryColor.copy(alpha = 0.65f),
                        letterSpacing = 0.4.sp
                    )
                }
            }
        }
    }
}
