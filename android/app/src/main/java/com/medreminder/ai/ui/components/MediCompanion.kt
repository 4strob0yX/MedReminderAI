package com.medreminder.ai.ui.components

import android.content.Context
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
import androidx.compose.animation.core.keyframes
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.ui.graphics.TransformOrigin
import android.speech.RecognizerIntent
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.changedToUp
import androidx.compose.ui.input.pointer.positionChange
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.Send
import androidx.compose.material.icons.automirrored.outlined.VolumeUp
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AccessAlarm
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.HealthAndSafety
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.LocalFireDepartment
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material.icons.outlined.Restaurant
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Warning
import androidx.compose.material.icons.outlined.WaterDrop
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.runtime.collectAsState
import androidx.core.content.ContextCompat
import com.medreminder.ai.notifications.TtsHelper
import com.medreminder.ai.notifications.VoiceInputHelper
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.delay
import com.medreminder.ai.ui.home.MediReaction
import com.medreminder.ai.ui.home.MediReactionKind
import kotlinx.coroutines.launch
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * Estados emocionales y reactivos de Medi.
 */
enum class MediMood {
    NORMAL,      // Mirada curiosa que explora el entorno, respiración serena
    HAPPY,       // Ojos en arco sonriente, aleteo sutil de aletas
    ATTENTIVE,   // Ojos ligeramente dilatados, escucha atenta
    DRAGGING,    // Ojos sorprendidos y abiertos (O_O), inclinación hacia la dirección de arrastre
    TALKING,     // Visor activo con pulsaciones suaves
    CELEBRATING, // Toma completada: ojos felices, destellos y saltos
    SLEEPY,      // Toma pospuesta: ojos relajados y "zzz"
    SAD          // Toma omitida: cejas caídas y lágrima
}

/**
 * Mascota clínica amigable "Medi": un orbe cibernético biomédico orgánico,
 * representativo, icónico y lleno de vida.
 *
 * Características de animación viva:
 * - Respiración orgánica sinusoidal y pulso cardíaco "lub-dub" en su núcleo central.
 * - Flotación armónica en 2D con inercia elástica.
 * - Aletas auditivas magnéticas laterales que flotan y reaccionan al movimiento.
 * - Visor panorámico de cristal curvado con reflejo especular.
 * - Ojos holográficos OLED reactivos que parpadean de forma procedimental y
 *   siguen la mirada del usuario / dirección de arrastre.
 * - CERO EMOJIS: 100% Canvas nativo vectorial de alto rendimiento.
 */
@Composable
fun MediMascotView(
    modifier: Modifier = Modifier,
    size: Dp = 64.dp,
    mood: MediMood = MediMood.NORMAL,
    animateHover: Boolean = true,
    lookTargetX: Float = 0f, // -1f (mira izquierda) a 1f (mira derecha)
    lookTargetY: Float = 0f, // -1f (mira arriba) a 1f (mira abajo)
    tiltAngle: Float = 0f,   // Inclinación corporal en grados
    squashStretchX: Float = 1f,
    squashStretchY: Float = 1f
) {
    val a11y = LocalAccessibilitySettings.current
    val transition = rememberInfiniteTransition(label = "medi_life_cycle")

    // 1. Flotación armónica orgánica (combinación de dos frecuencias para simular levitación real)
    val hoverY by if (animateHover) {
        transition.animateFloat(
            initialValue = -6.5f,
            targetValue = 6.5f,
            animationSpec = infiniteRepeatable(
                animation = tween(1500, easing = EaseInOutSine),
                repeatMode = RepeatMode.Reverse
            ),
            label = "medi_hover_y"
        )
    } else {
        remember { mutableFloatStateOf(0f) }
    }

    val hoverX by if (animateHover) {
        transition.animateFloat(
            initialValue = -2.6f,
            targetValue = 2.6f,
            animationSpec = infiniteRepeatable(
                animation = tween(2300, easing = EaseInOutSine),
                repeatMode = RepeatMode.Reverse
            ),
            label = "medi_hover_x"
        )
    } else {
        remember { mutableFloatStateOf(0f) }
    }

    // 2. Respiración sutil del cuerpo
    val breathScale by transition.animateFloat(
        initialValue = 0.985f,
        targetValue = 1.025f,
        animationSpec = infiniteRepeatable(
            animation = tween(2200, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "medi_breath"
    )

    // 3. Latido cardíaco real (lub-dub) en el núcleo médico
    val heartPulse by transition.animateFloat(
        initialValue = 1f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = keyframes {
                durationMillis = 1400
                1.0f at 0 using FastOutSlowInEasing
                1.26f at 100 using FastOutSlowInEasing  // Primer latido (lub)
                1.04f at 220 using FastOutSlowInEasing
                1.18f at 340 using FastOutSlowInEasing  // Segundo latido (dub)
                1.0f at 480 using EaseInOutSine
                1.0f at 1400
            },
            repeatMode = RepeatMode.Restart
        ),
        label = "medi_heartbeat"
    )

    // 4. Parpadeo procedimental con doble parpadeo orgánico
    var isBlinking by remember { mutableStateOf(false) }
    var idleLookX by remember { mutableFloatStateOf(0f) }
    var idleLookY by remember { mutableFloatStateOf(0f) }

    LaunchedEffect(Unit) {
        while (true) {
            delay((2800..4600).random().toLong())
            isBlinking = true
            delay(130)
            isBlinking = false

            // Ocasional mirada curiosa espontánea
            if ((0..3).random() == 0) {
                idleLookX = listOf(-0.35f, 0.35f, 0f).random()
                idleLookY = listOf(-0.2f, 0.2f, 0f).random()
            } else {
                idleLookX = 0f
                idleLookY = 0f
            }

            // Doble parpadeo rápido ocasional
            if ((0..2).random() == 0) {
                delay(120)
                isBlinking = true
                delay(110)
                isBlinking = false
            }
        }
    }

    val eyeScaleY by animateFloatAsState(
        targetValue = if (isBlinking) 0.08f else 1f,
        animationSpec = tween(70, easing = FastOutSlowInEasing),
        label = "medi_eyelid"
    )

    // Gaze suavizado combinando target externo + curiosidad idle
    val finalLookX = if (mood == MediMood.DRAGGING) lookTargetX else (lookTargetX + idleLookX).coerceIn(-1f, 1f)
    val finalLookY = if (mood == MediMood.DRAGGING) lookTargetY else (lookTargetY + idleLookY).coerceIn(-1f, 1f)

    val smoothLookX by animateFloatAsState(
        targetValue = finalLookX,
        animationSpec = spring(dampingRatio = Spring.DampingRatioLowBouncy, stiffness = Spring.StiffnessMedium),
        label = "medi_gaze_x"
    )
    val smoothLookY by animateFloatAsState(
        targetValue = finalLookY,
        animationSpec = spring(dampingRatio = Spring.DampingRatioLowBouncy, stiffness = Spring.StiffnessMedium),
        label = "medi_gaze_y"
    )

    // 5. Aleteo inercial de las aletas/orejas magnéticas laterales
    val earWave by transition.animateFloat(
        initialValue = -5f,
        targetValue = 5f,
        animationSpec = infiniteRepeatable(
            animation = tween(900, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "medi_ear_wave"
    )

    // 6. Balanceo corporal suave (nunca está "clavada")
    val sway by transition.animateFloat(
        initialValue = -3.2f,
        targetValue = 3.2f,
        animationSpec = infiniteRepeatable(
            animation = tween(2100, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "medi_sway"
    )

    // 7. Reloj para destellos / zzz / lágrima
    val sparkleT by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1100, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "medi_sparkle"
    )

    val primaryColor = a11y.adaptivePrimary
    val isHighContrast = a11y.isHighContrast
    val isDark = a11y.isDarkTheme

    Box(
        modifier = modifier
            .size(size)
            .graphicsLayer {
                translationY = hoverY * density
                translationX = hoverX * density
                rotationZ = tiltAngle + sway
                scaleX = breathScale * squashStretchX
                scaleY = breathScale * squashStretchY
            },
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawIconicMedi(
                mood = mood,
                eyeScaleY = eyeScaleY,
                lookX = smoothLookX,
                lookY = smoothLookY,
                earAngle = earWave,
                heartPulse = heartPulse,
                sparkleT = sparkleT,
                isHighContrast = isHighContrast,
                isDark = isDark
            )
        }
    }
}

/**
 * Trazado vectorial de alta gama para la mascota Medi.
 * Un diseño biomédico distintivo, con aletas magnéticas, visor 3D,
 * núcleo pulsante y ojos holográficos expresivos.
 */
private fun DrawScope.drawIconicMedi(
    mood: MediMood,
    eyeScaleY: Float,
    lookX: Float,
    lookY: Float,
    earAngle: Float,
    heartPulse: Float,
    sparkleT: Float,
    isHighContrast: Boolean,
    isDark: Boolean
) {
    val w = size.width
    val h = size.height
    val cx = w / 2f
    val cy = h / 2f

    // 0. Sombra / Aura de Levitación Magnética inferior
    val shadowW = w * 0.46f
    val shadowH = h * 0.10f
    val shadowY = h * 0.93f
    val shadowColor = if (isHighContrast) {
        if (isDark) Color(0xFF2DD4BF).copy(alpha = 0.25f) else Color.Black.copy(alpha = 0.18f)
    } else {
        TealPrimary.copy(alpha = 0.22f)
    }
    drawOval(
        color = shadowColor,
        topLeft = Offset(cx - shadowW / 2f, shadowY - shadowH / 2f),
        size = Size(shadowW, shadowH)
    )

    // 1. Aletas Magnéticas Flotantes Laterales (Orejas Sensoriales)
    val earW = w * 0.14f
    val earH = h * 0.24f
    val earOffsetY = h * 0.34f

    val earBrush = Brush.verticalGradient(
        colors = if (isHighContrast && isDark) {
            listOf(Color(0xFF2DD4BF), Color(0xFF005662))
        } else if (isHighContrast) {
            listOf(Color.White, Color(0xFFEEEEEE))
        } else {
            listOf(Color(0xFFE0F2F1), Color(0xFF80CBC4))
        }
    )
    val earBorderColor = if (isHighContrast) {
        if (isDark) Color(0xFF2DD4BF) else Color.Black
    } else {
        TealDark
    }

    // Aleta izquierda
    val leftEarPath = Path().apply {
        addRoundRect(
            RoundRect(
                left = cx - w * 0.48f,
                top = earOffsetY - earH / 2f + earAngle,
                right = cx - w * 0.35f,
                bottom = earOffsetY + earH / 2f + earAngle,
                cornerRadius = CornerRadius(earW, earW)
            )
        )
    }
    drawPath(leftEarPath, brush = earBrush)
    drawPath(leftEarPath, color = earBorderColor, style = Stroke(width = 1.4.dp.toPx()))

    // Aleta derecha
    val rightEarPath = Path().apply {
        addRoundRect(
            RoundRect(
                left = cx + w * 0.35f,
                top = earOffsetY - earH / 2f - earAngle,
                right = cx + w * 0.48f,
                bottom = earOffsetY + earH / 2f - earAngle,
                cornerRadius = CornerRadius(earW, earW)
            )
        )
    }
    drawPath(rightEarPath, brush = earBrush)
    drawPath(rightEarPath, color = earBorderColor, style = Stroke(width = 1.4.dp.toPx()))

    // 2. Baliza / Sensor de Levity superior
    val beaconY = h * 0.08f
    val beaconRadius = w * 0.055f
    val beaconGlowRadius = beaconRadius * 1.8f
    val beaconColor = if (isHighContrast && isDark) {
        Color(0xFF2DD4BF)
    } else if (isHighContrast) {
        Color.Black
    } else if (mood == MediMood.SAD) {
        Color(0xFFFF7043)
    } else if (mood == MediMood.SLEEPY) {
        Color(0xFFB39DDB)
    } else if (mood == MediMood.DRAGGING || mood == MediMood.HAPPY || mood == MediMood.CELEBRATING) {
        Color(0xFFFFB703)
    } else {
        Color(0xFF14B8A6)
    }

    drawCircle(
        color = beaconColor.copy(alpha = 0.30f),
        radius = beaconGlowRadius,
        center = Offset(cx, beaconY)
    )
    drawCircle(
        color = beaconColor,
        radius = beaconRadius,
        center = Offset(cx, beaconY)
    )

    // Tallo de la baliza
    drawLine(
        color = earBorderColor,
        start = Offset(cx, beaconY + beaconRadius),
        end = Offset(cx, h * 0.15f),
        strokeWidth = 2.dp.toPx(),
        cap = StrokeCap.Round
    )

    // 3. Cuerpo Principal de Cápsula Orgánica
    val bodyW = w * 0.72f
    val bodyH = h * 0.74f
    val bodyLeft = cx - bodyW / 2f
    val bodyTop = h * 0.15f
    val bodyRadius = bodyW / 2f

    val bodyPath = Path().apply {
        addRoundRect(
            RoundRect(
                left = bodyLeft,
                top = bodyTop,
                right = bodyLeft + bodyW,
                bottom = bodyTop + bodyH,
                cornerRadius = CornerRadius(bodyRadius, bodyRadius)
            )
        )
    }

    val bodyBrush = Brush.verticalGradient(
        colors = if (isHighContrast && isDark) {
            listOf(Color(0xFF001B20), Color(0xFF002C33))
        } else if (isHighContrast) {
            listOf(Color.White, Color.White)
        } else {
            listOf(
                Color(0xFFFFFFFF),
                Color(0xFFF6FAF9),
                Color(0xFFE0F2F1)
            )
        },
        startY = bodyTop,
        endY = bodyTop + bodyH
    )

    drawPath(bodyPath, brush = bodyBrush)
    drawPath(
        bodyPath,
        color = if (isHighContrast) (if (isDark) Color(0xFF2DD4BF) else Color.Black) else TealDark,
        style = Stroke(width = if (isHighContrast) 2.4.dp.toPx() else 1.8.dp.toPx())
    )

    // Anillo sutil divisorio de cintura
    val waistY = bodyTop + bodyH * 0.54f
    drawLine(
        color = if (isHighContrast) (if (isDark) Color(0xFF2DD4BF) else Color.Black) else Color(0xFF80CBC4),
        start = Offset(bodyLeft + 4.dp.toPx(), waistY),
        end = Offset(bodyLeft + bodyW - 4.dp.toPx(), waistY),
        strokeWidth = 1.2.dp.toPx()
    )

    // 4. Visor Panorámico Oscuro Curvado
    val visorW = bodyW * 0.82f
    val visorH = bodyH * 0.38f
    val visorLeft = cx - visorW / 2f
    val visorTop = bodyTop + bodyH * 0.10f
    val visorRadius = visorH / 2f

    val visorPath = Path().apply {
        addRoundRect(
            RoundRect(
                left = visorLeft,
                top = visorTop,
                right = visorLeft + visorW,
                bottom = visorTop + visorH,
                cornerRadius = CornerRadius(visorRadius, visorRadius)
            )
        )
    }

    val visorBg = if (isHighContrast && isDark) Color(0xFF000E11) else Color(0xFF0D171A)
    drawPath(visorPath, color = visorBg)

    // Reflejo especular brillante superior de cristal
    val highlightPath = Path().apply {
        addRoundRect(
            RoundRect(
                left = visorLeft + visorW * 0.14f,
                top = visorTop + 2.5.dp.toPx(),
                right = visorLeft + visorW * 0.86f,
                bottom = visorTop + visorH * 0.28f,
                cornerRadius = CornerRadius(visorRadius, visorRadius)
            )
        )
    }
    drawPath(
        highlightPath,
        color = Color.White.copy(alpha = if (isHighContrast) 0.15f else 0.22f)
    )

    // 5. Ojos Holográficos Digitales OLED Reactivos
    val eyeW = visorW * 0.19f
    val eyeH = (visorH * 0.48f) * eyeScaleY * (if (mood == MediMood.SAD) 0.8f else 1f)
    val eyeSpacing = visorW * 0.23f

    val gazeShiftX = lookX * (visorW * 0.14f)
    val gazeShiftY = lookY * (visorH * 0.14f)

    val leftEyeCenter = Offset(cx - eyeSpacing + gazeShiftX, visorTop + visorH * 0.52f + gazeShiftY)
    val rightEyeCenter = Offset(cx + eyeSpacing + gazeShiftX, visorTop + visorH * 0.52f + gazeShiftY)

    val eyeGlowColor = when {
        isHighContrast && isDark -> Color(0xFF2DD4BF)
        isHighContrast -> Color.White
        mood == MediMood.HAPPY || mood == MediMood.CELEBRATING -> Color(0xFF10B981)
        mood == MediMood.SAD -> Color(0xFF82B1FF)
        mood == MediMood.SLEEPY -> Color(0xFFB39DDB)
        mood == MediMood.DRAGGING -> Color(0xFF2DD4BF)
        else -> Color(0xFF14B8A6)
    }

    if (mood == MediMood.SLEEPY) {
        // Ojos cerrados relajados ‿ ‿
        val calmStroke = Stroke(width = 2.6.dp.toPx(), cap = StrokeCap.Round)
        listOf(leftEyeCenter, rightEyeCenter).forEach { c ->
            drawArc(
                color = eyeGlowColor,
                startAngle = 0f,
                sweepAngle = 180f,
                useCenter = false,
                topLeft = Offset(c.x - eyeW / 2f, c.y - eyeW * 0.4f),
                size = Size(eyeW, eyeW * 0.8f),
                style = calmStroke
            )
        }
    } else if (mood == MediMood.HAPPY || mood == MediMood.CELEBRATING) {
        // Ojos en arco sonriente ^ ^
        val smileStroke = Stroke(width = 2.6.dp.toPx(), cap = StrokeCap.Round)
        drawArc(
            color = eyeGlowColor,
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(leftEyeCenter.x - eyeW / 2f, leftEyeCenter.y - eyeW * 0.4f),
            size = Size(eyeW, eyeW * 0.8f),
            style = smileStroke
        )
        drawArc(
            color = eyeGlowColor,
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = false,
            topLeft = Offset(rightEyeCenter.x - eyeW / 2f, rightEyeCenter.y - eyeW * 0.4f),
            size = Size(eyeW, eyeW * 0.8f),
            style = smileStroke
        )
    } else if (mood == MediMood.DRAGGING) {
        // Ojos amplios y asombrados O O al ser arrastrado
        drawCircle(color = eyeGlowColor.copy(alpha = 0.35f), radius = eyeW * 0.65f, center = leftEyeCenter)
        drawCircle(color = eyeGlowColor.copy(alpha = 0.35f), radius = eyeW * 0.65f, center = rightEyeCenter)
        drawCircle(color = eyeGlowColor, radius = eyeW * 0.48f, center = leftEyeCenter)
        drawCircle(color = eyeGlowColor, radius = eyeW * 0.48f, center = rightEyeCenter)
        // Destello pupilar
        drawCircle(color = Color.White, radius = eyeW * 0.18f, center = leftEyeCenter - Offset(eyeW * 0.12f, eyeW * 0.12f))
        drawCircle(color = Color.White, radius = eyeW * 0.18f, center = rightEyeCenter - Offset(eyeW * 0.12f, eyeW * 0.12f))
    } else {
        // Ojos cápsula expresivos con parpadeo y reflejo pupilar
        val eyeCorner = CornerRadius(eyeW / 2f, eyeW / 2f)
        val eyeSize = Size(eyeW, eyeH.coerceAtLeast(1.dp.toPx()))

        // Glow externo sutil
        if (eyeScaleY > 0.4f && !isHighContrast) {
            drawRoundRect(
                color = eyeGlowColor.copy(alpha = 0.30f),
                topLeft = Offset(leftEyeCenter.x - eyeW * 0.6f, leftEyeCenter.y - eyeH * 0.6f),
                size = Size(eyeW * 1.2f, eyeH * 1.2f),
                cornerRadius = eyeCorner
            )
            drawRoundRect(
                color = eyeGlowColor.copy(alpha = 0.30f),
                topLeft = Offset(rightEyeCenter.x - eyeW * 0.6f, rightEyeCenter.y - eyeH * 0.6f),
                size = Size(eyeW * 1.2f, eyeH * 1.2f),
                cornerRadius = eyeCorner
            )
        }

        // Ojo izquierdo
        drawRoundRect(
            color = eyeGlowColor,
            topLeft = Offset(leftEyeCenter.x - eyeW / 2f, leftEyeCenter.y - eyeH / 2f),
            size = eyeSize,
            cornerRadius = eyeCorner
        )
        // Ojo derecho
        drawRoundRect(
            color = eyeGlowColor,
            topLeft = Offset(rightEyeCenter.x - eyeW / 2f, rightEyeCenter.y - eyeH / 2f),
            size = eyeSize,
            cornerRadius = eyeCorner
        )

        // Reflejos especulares en las pupilas
        if (eyeScaleY > 0.6f) {
            drawCircle(
                color = Color.White,
                radius = eyeW * 0.20f,
                center = Offset(leftEyeCenter.x - eyeW * 0.14f, leftEyeCenter.y - eyeH * 0.20f)
            )
            drawCircle(
                color = Color.White,
                radius = eyeW * 0.20f,
                center = Offset(rightEyeCenter.x - eyeW * 0.14f, rightEyeCenter.y - eyeH * 0.20f)
            )
        }
    }

    if (mood == MediMood.SAD) {
        val browStroke = 2.2.dp.toPx()
        // Cejas caídas (extremo interior elevado)
        drawLine(
            color = eyeGlowColor,
            start = Offset(leftEyeCenter.x - eyeW * 0.6f, leftEyeCenter.y - eyeH * 0.75f),
            end = Offset(leftEyeCenter.x + eyeW * 0.5f, leftEyeCenter.y - eyeH * 1.05f),
            strokeWidth = browStroke,
            cap = StrokeCap.Round
        )
        drawLine(
            color = eyeGlowColor,
            start = Offset(rightEyeCenter.x + eyeW * 0.6f, rightEyeCenter.y - eyeH * 0.75f),
            end = Offset(rightEyeCenter.x - eyeW * 0.5f, rightEyeCenter.y - eyeH * 1.05f),
            strokeWidth = browStroke,
            cap = StrokeCap.Round
        )
        // Lágrima que cae
        drawCircle(
            color = Color(0xFF80D8FF).copy(alpha = (1f - sparkleT) * 0.9f),
            radius = eyeW * 0.14f,
            center = Offset(leftEyeCenter.x - eyeW * 0.2f, leftEyeCenter.y + eyeH * 0.5f + visorH * 0.35f * sparkleT)
        )
    }

    if (mood == MediMood.CELEBRATING) {
        val colors = listOf(Color(0xFFFFB703), Color(0xFF14B8A6), Color(0xFF10B981))
        for (i in 0 until 6) {
            val t = (sparkleT + i / 6f) % 1f
            val ang = Math.toRadians((i * 60 + 15).toDouble())
            val dist = w * (0.40f + 0.24f * t)
            drawSparkle(
                center = Offset(cx + (cos(ang) * dist).toFloat(), cy + (sin(ang) * dist).toFloat()),
                r = w * 0.10f * sin(Math.PI.toFloat() * t),
                color = colors[i % colors.size],
                alpha = 1f - t * 0.6f
            )
        }
    }

    if (mood == MediMood.SLEEPY) {
        for (i in 0 until 3) {
            val t = (sparkleT + i / 3f) % 1f
            val s = w * (0.05f + 0.05f * t)
            val zx = cx + w * 0.26f + w * 0.14f * t
            val zy = h * 0.12f - h * 0.14f * t
            val zc = Color(0xFFB39DDB).copy(alpha = sin(Math.PI.toFloat() * t).coerceIn(0f, 1f))
            val zPath = Path().apply {
                moveTo(zx - s, zy - s)
                lineTo(zx + s, zy - s)
                lineTo(zx - s, zy + s)
                lineTo(zx + s, zy + s)
            }
            drawPath(zPath, color = zc, style = Stroke(width = 1.8.dp.toPx(), cap = StrokeCap.Round))
        }
    }

    // 6. Rubor amigable en las mejillas
    if (!isHighContrast && eyeScaleY > 0.4f) {
        val blushColor = Color(0xFFFF8A80).copy(alpha = 0.35f)
        drawCircle(
            color = blushColor,
            radius = eyeW * 0.36f,
            center = Offset(visorLeft + visorW * 0.10f, visorTop + visorH * 0.80f)
        )
        drawCircle(
            color = blushColor,
            radius = eyeW * 0.36f,
            center = Offset(visorLeft + visorW * 0.90f, visorTop + visorH * 0.80f)
        )
    }

    // 7. Núcleo Biomédico de Vida (Corazón Pulsante en el Pecho)
    val coreY = waistY + bodyH * 0.22f
    val coreBaseRadius = bodyW * 0.16f
    val coreGlowRadius = coreBaseRadius * heartPulse

    val coreGlowColor = if (isHighContrast && isDark) {
        Color(0xFF2DD4BF)
    } else if (isHighContrast) {
        Color.Black
    } else {
        TealPrimary
    }

    // Halo pulsante radial
    drawCircle(
        color = coreGlowColor.copy(alpha = 0.25f),
        radius = coreGlowRadius,
        center = Offset(cx, coreY)
    )

    // Cristal del núcleo
    drawCircle(
        color = if (isHighContrast && isDark) Color(0xFF00363A) else Color(0xFFE0F2F1),
        radius = coreBaseRadius,
        center = Offset(cx, coreY)
    )
    drawCircle(
        color = if (isHighContrast) coreGlowColor else TealDark,
        radius = coreBaseRadius,
        center = Offset(cx, coreY),
        style = Stroke(width = 1.2.dp.toPx())
    )

    // Emblema médico interior del núcleo (Cruz sutil o pulso)
    val crossArm = coreBaseRadius * 0.55f
    val crossThick = 2.2.dp.toPx()
    val crossColor = if (isHighContrast) coreGlowColor else TealDark

    drawLine(
        color = crossColor,
        start = Offset(cx - crossArm, coreY),
        end = Offset(cx + crossArm, coreY),
        strokeWidth = crossThick,
        cap = StrokeCap.Round
    )
    drawLine(
        color = crossColor,
        start = Offset(cx, coreY - crossArm),
        end = Offset(cx, coreY + crossArm),
        strokeWidth = crossThick,
        cap = StrokeCap.Round
    )
}

private fun DrawScope.drawSparkle(center: Offset, r: Float, color: Color, alpha: Float) {
    if (r <= 0.5f) return
    val p = Path().apply {
        moveTo(center.x, center.y - r)
        quadraticBezierTo(center.x, center.y, center.x + r, center.y)
        quadraticBezierTo(center.x, center.y, center.x, center.y + r)
        quadraticBezierTo(center.x, center.y, center.x - r, center.y)
        quadraticBezierTo(center.x, center.y, center.x, center.y - r)
        close()
    }
    drawPath(p, color = color.copy(alpha = alpha.coerceIn(0f, 1f)))
}

@Composable
private fun Modifier.bounceClick(scaleDown: Float = 0.94f): Modifier {
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (isPressed) scaleDown else 1f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        label = "bounce_scale"
    )
    return this.graphicsLayer {
        scaleX = scale
        scaleY = scale
    }
}

/**
 * Mascota Flotante Draggable Magnética ("Living Medi Companion").
 * Permite al usuario tocar y arrastrar a Medi libremente por cualquier parte de la pantalla.
 * Al soltarlo, se magnetiza suavemente hacia el borde más cercano (izquierdo o derecho)
 * con física de muelle elástica (spring physics) y animación de rebote squash & stretch.
 * Al hacer tap, despliega su diálogo inteligente de asistente médico.
 */
@Composable
fun DraggableMediCompanion(
    onClick: () -> Unit = {},
    modifier: Modifier = Modifier,
    safeTopPadding: Dp = 16.dp,
    safeBottomPadding: Dp = 24.dp,
    isChatOpen: Boolean = false,
    onDismissChat: () -> Unit = {},
    reaction: MediReaction? = null,
    nombreUsuario: String = "Paciente",
    contextoPantalla: String = "Hoy"
) {
    BoxWithConstraints(
        modifier = modifier.fillMaxSize()
    ) {
        val density = LocalDensity.current
        val uiScope = rememberCoroutineScope()

        val widthPx = constraints.maxWidth.toFloat()
        val heightPx = constraints.maxHeight.toFloat()

        val mascotSize = 70.dp
        val mascotSizePx = with(density) { mascotSize.toPx() }

        val minX = with(density) { 14.dp.toPx() }
        val maxX = (widthPx - mascotSizePx - with(density) { 14.dp.toPx() }).coerceAtLeast(minX)
        val minY = with(density) { safeTopPadding.toPx() }
        val maxY = (heightPx - mascotSizePx - with(density) { safeBottomPadding.toPx() }).coerceAtLeast(minY)

        // Posición animada libre (arranca acoplada al borde derecho visible y persiste entre recomposiciones)
        val offsetX = remember { Animatable(-1f) }
        val offsetY = remember { Animatable(-1f) }

        var dragAccumX by remember { mutableFloatStateOf(-1f) }
        var dragAccumY by remember { mutableFloatStateOf(-1f) }

        LaunchedEffect(maxX, maxY) {
            if (offsetX.value < 0f) {
                val initialX = maxX
                val initialY = (maxY - with(density) { 70.dp.toPx() }).coerceIn(minY, maxY)
                offsetX.snapTo(initialX)
                offsetY.snapTo(initialY)
                dragAccumX = initialX
                dragAccumY = initialY
            } else {
                // Mantener acoplado a los límites si cambió el tamaño de pantalla
                if (offsetX.value > maxX) offsetX.snapTo(maxX)
                if (offsetY.value > maxY) offsetY.snapTo(maxY)
            }
        }

        // Estados de interacción física
        var isDragging by remember { mutableStateOf(false) }
        var dragVelocityX by remember { mutableFloatStateOf(0f) }
        var dragVelocityY by remember { mutableFloatStateOf(0f) }
        var currentMood by remember { mutableStateOf(MediMood.NORMAL) }

        // Squash & Stretch físico, saltos, giros y balanceos
        val squashX = remember { Animatable(1f) }
        val squashY = remember { Animatable(1f) }
        val hopY = remember { Animatable(0f) }
        val spin = remember { Animatable(0f) }
        val wobble = remember { Animatable(0f) }
        val flightScale = remember { Animatable(1f) }

        // Vuelo hacia el chat y anclaje
        var isFlying by remember { mutableStateOf(false) }
        var atChat by remember { mutableStateOf(false) }
        var homeX by remember { mutableFloatStateOf(0f) }
        var homeY by remember { mutableFloatStateOf(0f) }

        // Globo de diálogo reactivo
        var speech by remember { mutableStateOf<String?>(null) }
        var lastSpeech by remember { mutableStateOf("") }
        val say: (String?) -> Unit = { t ->
            if (t != null) lastSpeech = t
            speech = t
        }

        val hopHeightPx = with(density) { 26.dp.toPx() }

        suspend fun doHop(heightPx: Float) {
            coroutineScope {
                launch { hopY.animateTo(-heightPx, tween(190, easing = FastOutSlowInEasing)) }
                launch { squashY.animateTo(1.14f, tween(190)) }
                launch { squashX.animateTo(0.92f, tween(190)) }
            }
            coroutineScope {
                launch { hopY.animateTo(0f, tween(170, easing = FastOutSlowInEasing)) }
                launch { squashY.animateTo(1f, tween(170)) }
                launch { squashX.animateTo(1f, tween(170)) }
            }
            coroutineScope {
                launch { squashY.animateTo(0.86f, tween(70)) }
                launch { squashX.animateTo(1.12f, tween(70)) }
            }
            coroutineScope {
                launch { squashY.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium)) }
                launch { squashX.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium)) }
            }
        }

        suspend fun doShake(amplitude: Float) {
            for (v in listOf(-amplitude, amplitude, -amplitude * 0.75f, amplitude * 0.75f, -amplitude * 0.4f, 0f)) {
                wobble.animateTo(v, tween(110))
            }
        }

        suspend fun resetPose() {
            hopY.snapTo(0f)
            wobble.snapTo(0f)
            spin.snapTo(0f)
            squashX.snapTo(1f)
            squashY.snapTo(1f)
        }

        val dismissChat: () -> Unit = {
            if (atChat && !isFlying) {
                atChat = false
                uiScope.launch {
                    VoiceInputHelper.stopListening()
                    TtsHelper.stop()
                    // Pausa breve para permitir que el cuadro de texto se repliegue hacia la mascota
                    delay(190)
                    isFlying = true
                    currentMood = MediMood.HAPPY
                    val j1 = launch { flightScale.animateTo(1f, spring(0.7f, 130f)) }
                    val j2 = launch { offsetX.animateTo(homeX, spring(0.62f, 110f)) }
                    val j3 = launch { offsetY.animateTo(homeY, spring(0.62f, 110f)) }
                    val j4 = launch { spin.animateTo(-360f, tween(700, easing = FastOutSlowInEasing)); spin.snapTo(0f) }
                    j1.join(); j2.join(); j3.join(); j4.join()
                    dragAccumX = offsetX.value
                    dragAccumY = offsetY.value
                    isFlying = false
                    delay(350)
                    currentMood = MediMood.NORMAL
                    onDismissChat()
                }
            }
        }

        val triggerMediTap: () -> Unit = {
            if (atChat) {
                dismissChat()
            } else if (!isFlying) {
                uiScope.launch {
                    isFlying = true
                    say(null)
                    homeX = offsetX.value.let { if (it < 0f) maxX else it }
                    homeY = offsetY.value.let { if (it < 0f) maxY else it }
                    currentMood = MediMood.HAPPY
                    resetPose()

                    val targetX = ((widthPx - mascotSizePx) / 2f).coerceIn(minX, maxX)
                    val targetY = with(density) { 34.dp.toPx() }.coerceIn(minY, maxY)

                    // 1. Anticipación elástica: se comprime con energía
                    coroutineScope {
                        launch { squashY.animateTo(0.68f, tween(110)) }
                        launch { squashX.animateTo(1.30f, tween(110)) }
                    }
                    // 2. Vuelo propulsado en curva hacia el centro-superior con estela de giro
                    val flightJobs = listOf(
                        launch { squashY.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessLow)) },
                        launch { squashX.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessLow)) },
                        launch { flightScale.animateTo(1.28f, spring(0.62f, 110f)) },
                        launch { spin.animateTo(360f, tween(750, easing = FastOutSlowInEasing)); spin.snapTo(0f) },
                        launch { offsetX.animateTo(targetX, spring(0.60f, 105f)) },
                        launch { offsetY.animateTo(targetY, spring(0.60f, 105f)) }
                    )
                    flightJobs.forEach { it.join() }

                    // 3. Aterrizaje amortiguado sobre la posición del chat
                    coroutineScope {
                        launch { squashY.animateTo(0.80f, tween(85)) }
                        launch { squashX.animateTo(1.18f, tween(85)) }
                    }
                    coroutineScope {
                        launch { squashY.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium)) }
                        launch { squashX.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium)) }
                    }

                    atChat = true
                    isFlying = false
                    currentMood = MediMood.TALKING
                    onClick()
                }
            }
        }

        // Reacciones expresivas y prolongadas a eventos de toma (tomada / pospuesta / omitida)
        LaunchedEffect(reaction) {
            val r = reaction ?: return@LaunchedEffect
            if (isFlying || atChat || isDragging) return@LaunchedEffect
            when (r.kind) {
                MediReactionKind.TAKEN -> {
                    currentMood = MediMood.CELEBRATING
                    say(listOf(
                        "¡Excelente! +25 XP • Dosis registrada con éxito ✨",
                        "¡Así se hace! Manteniendo tu salud protegida 🌟",
                        "¡Dosis confirmada! Racha de salud en aumento 🚀"
                    ).random())
                    coroutineScope {
                        launch {
                            spin.animateTo(360f, tween(850, easing = FastOutSlowInEasing))
                            spin.snapTo(0f)
                        }
                        launch {
                            doHop(hopHeightPx * 1.5f)
                            delay(60)
                            doHop(hopHeightPx * 1.1f)
                            delay(60)
                            doHop(hopHeightPx * 0.8f)
                        }
                    }
                    delay(3200)
                }
                MediReactionKind.SNOOZED -> {
                    currentMood = MediMood.SLEEPY
                    say("Entendido • Te recordaré esta toma en 30 min zZz")
                    coroutineScope {
                        launch { doShake(7f) }
                        launch {
                            squashY.animateTo(0.90f, tween(600, easing = EaseInOutSine))
                            delay(1200)
                            squashY.animateTo(1f, tween(600, easing = EaseInOutSine))
                        }
                    }
                    delay(3000)
                }
                MediReactionKind.SKIPPED -> {
                    currentMood = MediMood.SAD
                    say("Oh no... Cuidemos tu salud, procura no omitir tus tomas")
                    coroutineScope {
                        launch { doShake(14f) }
                        launch {
                            squashY.animateTo(0.88f, tween(500, easing = EaseInOutSine))
                            delay(1400)
                            squashY.animateTo(1f, tween(500, easing = EaseInOutSine))
                        }
                    }
                    delay(3000)
                }
            }
            say(null)
            currentMood = MediMood.NORMAL
        }

        // Vida propia constante: micro-movimientos orgánicos frecuentes para que nunca se sienta rígida
        LaunchedEffect(isDragging, isFlying, atChat) {
            if (isDragging || isFlying || atChat) return@LaunchedEffect
            while (true) {
                delay((2200..4200).random().toLong())
                if (currentMood != MediMood.NORMAL) continue
                when ((0..4).random()) {
                    0 -> doHop(hopHeightPx * 0.85f)
                    1 -> doShake(8f)
                    2 -> {
                        coroutineScope {
                            launch {
                                wobble.animateTo(6f, tween(150))
                                wobble.animateTo(-6f, tween(150))
                                wobble.animateTo(0f, tween(150))
                            }
                            launch {
                                squashX.animateTo(1.08f, tween(180))
                                squashX.animateTo(1f, tween(180))
                            }
                        }
                    }
                    3 -> {
                        doHop(hopHeightPx * 0.5f)
                        delay(90)
                        doHop(hopHeightPx * 0.6f)
                    }
                    else -> {
                        squashY.animateTo(0.92f, tween(160))
                        squashY.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium))
                    }
                }
            }
        }

        // Sincronización con estado externo isChatOpen
        LaunchedEffect(isChatOpen) {
            if (isChatOpen && !atChat && !isFlying) {
                triggerMediTap()
            } else if (!isChatOpen && atChat) {
                dismissChat()
            }
        }

        // Dirección hacia la que mira cuando está anclado a un borde
        val currentX = if (offsetX.value < 0f) maxX else offsetX.value
        val dockedOnLeft = currentX < widthPx / 2f
        val edgeLookTargetX = if (isDragging) {
            (dragVelocityX / 40f).coerceIn(-1f, 1f)
        } else if (atChat || isFlying) {
            0f
        } else {
            if (dockedOnLeft) 0.65f else -0.65f
        }
        val tiltAngle = if (isDragging) {
            (dragVelocityX * 0.45f).coerceIn(-18f, 18f)
        } else {
            0f
        }

        // 1. Atenuación sutil de fondo (Backdrop Dim) al interactuar con el chat
        AnimatedVisibility(
            visible = atChat,
            enter = fadeIn(tween(240)),
            exit = fadeOut(tween(180))
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0x66000000))
                    .clickable(
                        interactionSource = remember { MutableInteractionSource() },
                        indication = null
                    ) {
                        dismissChat()
                    }
            )
        }

        // 2. Cuadro de Texto Holográfico: Emerge y brota directamente desde el cuerpo de la mascota
        val chatTopY = (offsetY.value + mascotSizePx * flightScale.value - with(density) { 10.dp.toPx() })
        AnimatedVisibility(
            visible = atChat,
            enter = fadeIn(tween(260)) +
                scaleIn(
                    initialScale = 0.05f,
                    transformOrigin = TransformOrigin(0.5f, 0f),
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioMediumBouncy,
                        stiffness = Spring.StiffnessMediumLow
                    )
                ) +
                expandVertically(
                    expandFrom = Alignment.Top,
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioMediumBouncy,
                        stiffness = Spring.StiffnessMediumLow
                    )
                ),
            exit = fadeOut(tween(160)) +
                scaleOut(
                    targetScale = 0.05f,
                    transformOrigin = TransformOrigin(0.5f, 0f),
                    animationSpec = tween(160)
                ) +
                shrinkVertically(
                    shrinkTowards = Alignment.Top,
                    animationSpec = tween(160)
                ),
            modifier = Modifier
                .align(Alignment.TopCenter)
                .offset { IntOffset(0, chatTopY.roundToInt().coerceAtLeast(0)) }
                .padding(horizontal = 14.dp)
                .fillMaxWidth()
        ) {
            MediDirectEmergentChatCard(
                nombreUsuario = nombreUsuario,
                contextoPantalla = contextoPantalla,
                onDismiss = dismissChat,
                onMoodChange = { currentMood = it }
            )
        }

        // 3. Mascota Viva Medi: Dibujada por encima del chat como cabeza y corona
        Box(
            modifier = Modifier
                .offset {
                    IntOffset(
                        (if (offsetX.value < 0f) maxX else offsetX.value).roundToInt(),
                        ((if (offsetY.value < 0f) maxY else offsetY.value) + hopY.value).roundToInt()
                    )
                }
                .graphicsLayer {
                    scaleX = flightScale.value
                    scaleY = flightScale.value
                }
                .size(mascotSize)
                .pointerInput(isFlying, atChat) {
                    if (isFlying) return@pointerInput
                    val touchSlop = viewConfiguration.touchSlop
                    awaitEachGesture {
                        val down = awaitFirstDown(requireUnconsumed = false)
                        var isDraggingInternal = false

                        while (true) {
                            val event = awaitPointerEvent()
                            val change = event.changes.firstOrNull { it.id == down.id } ?: break

                            if (change.changedToUp()) {
                                change.consume()
                                if (!isDraggingInternal) {
                                    triggerMediTap()
                                } else {
                                    isDragging = false
                                    val targetX = if (dragAccumX + mascotSizePx / 2f < widthPx / 2f) minX else maxX
                                    uiScope.launch {
                                        offsetX.animateTo(
                                            targetValue = targetX,
                                            animationSpec = spring(
                                                dampingRatio = Spring.DampingRatioMediumBouncy,
                                                stiffness = Spring.StiffnessLow
                                            )
                                        )
                                        dragAccumX = targetX
                                        currentMood = MediMood.HAPPY
                                        launch {
                                            squashX.animateTo(1.18f, tween(90))
                                            squashX.animateTo(1.0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessLow))
                                        }
                                        launch {
                                            squashY.animateTo(0.84f, tween(90))
                                            squashY.animateTo(1.0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessLow))
                                        }
                                        delay(1200)
                                        currentMood = MediMood.NORMAL
                                    }
                                }
                                break
                            }

                            if (!atChat) {
                                val totalMovement = (change.position - down.position).getDistance()
                                if (!isDraggingInternal && totalMovement > touchSlop) {
                                    isDraggingInternal = true
                                    isDragging = true
                                    currentMood = MediMood.DRAGGING
                                    say(null)
                                    dragAccumX = offsetX.value
                                    dragAccumY = offsetY.value
                                    uiScope.launch { resetPose() }
                                }

                                if (isDraggingInternal) {
                                    val delta = change.positionChange()
                                    change.consume()
                                    dragVelocityX = delta.x
                                    dragVelocityY = delta.y
                                    dragAccumX = (dragAccumX + delta.x).coerceIn(0f, widthPx - mascotSizePx)
                                    dragAccumY = (dragAccumY + delta.y).coerceIn(minY, maxY)

                                    uiScope.launch {
                                        offsetX.snapTo(dragAccumX)
                                        offsetY.snapTo(dragAccumY)
                                    }
                                }
                            }
                        }

                        if (isDraggingInternal && isDragging) {
                            isDragging = false
                            currentMood = MediMood.NORMAL
                            val targetX = if (dragAccumX + mascotSizePx / 2f < widthPx / 2f) minX else maxX
                            uiScope.launch {
                                offsetX.animateTo(
                                    targetValue = targetX,
                                    animationSpec = spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessLow)
                                )
                                dragAccumX = targetX
                            }
                        }
                    }
                },
            contentAlignment = Alignment.Center
        ) {
            // Halo de elevación translúcido flotante
            Box(
                modifier = Modifier
                    .size(mascotSize + 10.dp)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            colors = listOf(
                                TealPrimary.copy(
                                    alpha = if (isDragging || isFlying || atChat) 0.32f else 0.14f
                                ),
                                Color.Transparent
                            )
                        )
                    )
            )

            // La mascota viva con física activa
            MediMascotView(
                size = mascotSize,
                mood = if (atChat && currentMood == MediMood.NORMAL) MediMood.TALKING else currentMood,
                animateHover = !isDragging,
                lookTargetX = edgeLookTargetX,
                lookTargetY = if (isDragging) (dragVelocityY / 40f).coerceIn(-1f, 1f) else 0f,
                tiltAngle = tiltAngle + spin.value + wobble.value,
                squashStretchX = squashX.value,
                squashStretchY = squashY.value
            )
        }

        // Globo de diálogo flotante junto a Medi (cuando está acoplado al borde)
        val bubbleMascotX = if (offsetX.value < 0f) maxX else offsetX.value
        val bubbleMascotY = (if (offsetY.value < 0f) maxY else offsetY.value) + hopY.value
        val bubbleHeightPx = with(density) { 46.dp.toPx() }
        val bubbleAbove = bubbleMascotY > bubbleHeightPx + with(density) { 8.dp.toPx() }
        val bubbleY = if (bubbleAbove) bubbleMascotY - bubbleHeightPx else bubbleMascotY + mascotSizePx
        val bubbleAlign = if (dockedOnLeft) Alignment.TopStart else Alignment.TopEnd
        val bubbleOffsetX = if (dockedOnLeft) bubbleMascotX else -(widthPx - bubbleMascotX - mascotSizePx)

        AnimatedVisibility(
            visible = speech != null && !isFlying && !atChat && !isDragging,
            enter = fadeIn(tween(180)) + scaleIn(spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium)),
            exit = fadeOut(tween(220)) + scaleOut(tween(220)),
            modifier = Modifier
                .align(bubbleAlign)
                .offset { IntOffset(bubbleOffsetX.roundToInt(), bubbleY.roundToInt()) }
        ) {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = Color(0xEE0B1519),
                border = BorderStroke(
                    1.dp,
                    Brush.linearGradient(listOf(Color(0xFF2DD4BF), Color(0xFF0F766E)))
                ),
                shadowElevation = 8.dp,
                modifier = Modifier.widthIn(max = 230.dp)
            ) {
                Text(
                    text = lastSpeech,
                    color = Color.White,
                    fontSize = 12.5.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp)
                )
            }
        }
    }
}

/**
 * Compatibilidad con invocaciones previas de MediFloatingCompanion:
 * Ahora utiliza directamente el sistema libre de arrastre magnético a los bordes.
 */
@Composable
fun MediFloatingCompanion(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    hasUnreadTip: Boolean = false
) {
    DraggableMediCompanion(
        onClick = onClick,
        modifier = modifier
    )
}

data class MediChatMessage(
    val id: String,
    val isFromUser: Boolean,
    val text: String,
    val timestamp: String
)

data class DossierPoint(
    val icon: ImageVector,
    val label: String,
    val description: String
)

data class MediClinicalDossier(
    val queryId: String,
    val title: String,
    val category: String,
    val riskLevel: String,
    val riskColor: Color,
    val riskScore: Float,
    val keyInsight: String,
    val points: List<DossierPoint>,
    val goldenRule: String,
    val fullVoiceScript: String
)

fun buildClinicalDossier(query: String, nombreUsuario: String): MediClinicalDossier {
    val q = query.lowercase().trim()
    return when {
        q.contains("café") || q.contains("cafe") || q.contains("cafeina") || q.contains("cafeína") -> {
            MediClinicalDossier(
                queryId = "cafe",
                title = "Interacción con Cafeína y Taninos",
                category = "FARMACOCINÉTICA Y METABOLISMO",
                riskLevel = "MODERADO · PRECAUCIÓN",
                riskColor = Color(0xFFF59E0B),
                riskScore = 0.65f,
                keyInsight = "La cafeína y los taninos aceleran el vaciado gástrico, interfieren con la absorción intestinal y desestabilizan temporalmente la glucemia.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.AccessAlarm,
                        label = "Ventana de Espera Clave",
                        description = "Espera entre 45 y 60 minutos antes o después de ingerir café para tomar cualquier medicamento."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Warning,
                        label = "Impacto en Insulina Glargina",
                        description = "La cafeína estimula la liberación de cortisol y adrenalina, alterando la curva basal de glucosa."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.WaterDrop,
                        label = "Vehículo Seguro Universal",
                        description = "Toma siempre tus comprimidos con un vaso completo de agua natural fresca a temperatura ambiente."
                    )
                ),
                goldenRule = "Nunca tomes tus comprimidos con café caliente ni té negro.",
                fullVoiceScript = "El café contiene cafeína y taninos que interfieren con la absorción gastrointestinal de ciertos medicamentos y alteran temporalmente la presión y glucemia. Con fármacos basales como Insulina Glargina la cafeína puede desestabilizar la curva de glucosa. Te recomiendo tomar siempre tus medicamentos con agua natural fresca y esperar al menos 45 a 60 minutos antes de beber café."
            )
        }
        q.contains("olvid") || q.contains("posp") || (q.contains("pasar") && q.contains("toma")) -> {
            MediClinicalDossier(
                queryId = "olvido",
                title = "Protocolo ante Dosis Omitida",
                category = "SEGURIDAD CLÍNICA VITAL",
                riskLevel = "CRÍTICO · NO DUPLICAR",
                riskColor = Color(0xFFEF4444),
                riskScore = 0.95f,
                keyInsight = "Bajo ninguna circunstancia compenses una omisión duplicando la dosis en la siguiente toma; el riesgo de hipoglucemia severa o toxicidad es extremo.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.Shield,
                        label = "Regla de Oro Anti-Duplicado",
                        description = "Duplicar la dosis no recupera el tiempo perdido y puede provocar un choque metabólico agudo."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.AccessAlarm,
                        label = "Regla de Mitad del Intervalo",
                        description = "En pastillas convencionales, tómala solo si falta más de la mitad del tiempo para la próxima dosis."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Phone,
                        label = "Alerta con Insulina Crítica",
                        description = "Si olvidaste tu Insulina Glargina, notifica de inmediato a Dra. Elena Ramos para reajustar el horario."
                    )
                ),
                goldenRule = "Nunca compenses una dosis olvidada ingiriendo dos tomas juntas.",
                fullVoiceScript = "En fármacos críticos como Insulina Glargina, nunca dupliques la dosis en la siguiente toma bajo ninguna circunstancia por alto riesgo de hipoglucemia severa. Si han pasado pocas horas de tu horario habitual, revisa tus registros y notifica a tu contacto médico Dra. Elena Ramos. En pastillas convencionales, tómala solo si falta más de la mitad del intervalo para la siguiente."
            )
        }
        q.contains("alcohol") || q.contains("cerveza") || q.contains("vino") || q.contains("licor") -> {
            MediClinicalDossier(
                queryId = "alcohol",
                title = "Contraindicación con Alcohol",
                category = "TOXICOLOGÍA FARMACOLÓGICA",
                riskLevel = "ALTO RIESGO · CONTRAINDICADO",
                riskColor = Color(0xFFEF4444),
                riskScore = 0.90f,
                keyInsight = "El etanol bloquea la gluconeogénesis hepática provocando hipoglucemias impredecibles y potencia la toxicidad de analgésicos.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.Warning,
                        label = "Hipoglucemia Severa",
                        description = "El hígado se ocupa de metabolizar el alcohol e interrumpe la liberación normal de glucosa."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Medication,
                        label = "Toxicidad con Paracetamol",
                        description = "La mezcla de alcohol y paracetamol satura el citocromo P450 y genera metabolitos hepatotóxicos."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Shield,
                        label = "Conducta Médica Obligatoria",
                        description = "Suspende totalmente bebidas alcohólicas durante tratamientos con fármacos activos."
                    )
                ),
                goldenRule = "El alcohol y los medicamentos activos nunca deben combinarse.",
                fullVoiceScript = "El alcohol bloquea la gluconeogénesis hepática provocando hipoglucemias impredecibles y severas en pacientes con insulina. Además, al metabolizarse en el hígado, sobrecarga las enzimas hepáticas e incrementa la toxicidad de analgésicos como el Paracetamol. Está contraindicado ingerir bebidas alcohólicas durante tu tratamiento."
            )
        }
        q.contains("insulina") || q.contains("critica") || q.contains("crítica") || q.contains("posponer") -> {
            MediClinicalDossier(
                queryId = "insulina",
                title = "Cobertura Basal de Insulina Glargina",
                category = "FARMACOTERAPIA BASAL CONTINUA",
                riskLevel = "CRÍTICO · VITAL ININTERRUMPIDO",
                riskColor = Color(0xFFEF4444),
                riskScore = 0.98f,
                keyInsight = "La Insulina Glargina mantiene una meseta de cobertura basal durante 24 horas continuas; postergarla rompe el equilibrio glucémico.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.LocalFireDepartment,
                        label = "Sin Pico de Concentración",
                        description = "Formulada para liberarse gradualmente; cualquier demora descontrola la glucosa nocturna y matutina."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Shield,
                        label = "Bloqueo Clínico en la App",
                        description = "Por tu seguridad médica, MedReminder AI no permite posponer ni omitir dosis críticas."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.CheckCircle,
                        label = "Horario Nocturno Fijo",
                        description = "Aplica tu dosis a la misma hora cada noche para mantener tu organismo protegido."
                    )
                ),
                goldenRule = "Tu dosis crítica basal no admite omisión para salvaguardar tu estabilidad metabólica.",
                fullVoiceScript = "Tu Insulina Glargina es de acción prolongada y mantiene una cobertura basal continua durante 24 horas. Posponer su toma desestabiliza tus niveles de glucosa en sangre durante la noche y el día siguiente, exponiéndote a descompensaciones metabólicas. Por esa razón clínica, el sistema bloquea su postergación para resguardar tu salud."
            )
        }
        q.contains("agua") || q.contains("vaso") || q.contains("liquido") || q.contains("líquido") || q.contains("hidrata") -> {
            MediClinicalDossier(
                queryId = "agua",
                title = "Guía de Hidratación y Disolución",
                category = "ADMINISTRACIÓN EFICAZ",
                riskLevel = "INFORMATIVO · RECOMENDADO",
                riskColor = Color(0xFF14B8A6),
                riskScore = 0.25f,
                keyInsight = "El volumen y tipo de líquido determinan la velocidad de disolución y protegen la mucosa del esófago y estómago.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.WaterDrop,
                        label = "Volumen Indicado",
                        description = "Bebe un vaso completo de 200 a 250 ml de agua natural simple para asegurar el tránsito gástrico."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Warning,
                        label = "Evitar Jugos Cítricos",
                        description = "El jugo de toronja inhibe el enzima CYP3A4 y altera desproporcionadamente las concentraciones plasmáticas."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.CheckCircle,
                        label = "Evitar Leche Inmediata",
                        description = "El calcio lácteo puede quelar ciertos principios activos disminuyendo su tasa de absorción."
                    )
                ),
                goldenRule = "El agua simple fresca es el único vehículo 100% seguro para tus dosis.",
                fullVoiceScript = "Toma siempre tus comprimidos con al menos un vaso lleno de agua simple a temperatura ambiente. No utilices jugo de toronja ni leche al momento de la toma, ya que contienen flavonoides y calcio que alteran la absorción de múltiples principios activos."
            )
        }
        q.contains("paracetamol") || q.contains("dolor") || q.contains("fiebre") -> {
            MediClinicalDossier(
                queryId = "paracetamol",
                title = "Margen de Seguridad de Paracetamol",
                category = "FARMACOVIGILANCIA HEPÁTICA",
                riskLevel = "PRECAUCIÓN · TOXICIDAD",
                riskColor = Color(0xFFF59E0B),
                riskScore = 0.50f,
                keyInsight = "El Paracetamol es seguro en dosis terapéuticas pero hepatotóxico en sobredosis acumulativas inadvertidas.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.Medication,
                        label = "Límite Máximo Diario",
                        description = "Nunca superes de 3 a 4 gramos en 24 horas para evitar daño hepático fulminante."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.AccessAlarm,
                        label = "Espaciado Clínico",
                        description = "Mantén un intervalo riguroso de 6 a 8 horas entre cada toma para depuración metabólica."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Warning,
                        label = "Antigripales Combinados",
                        description = "Revisa fórmulas compuestas para no sumar paracetamol sin darte cuenta."
                    )
                ),
                goldenRule = "Respeta los horarios pautados y jamás dupliques tomas ante dolor persistente.",
                fullVoiceScript = "El Paracetamol es un analgésico eficaz y seguro si se respetan las dosis pautadas. Nunca superes los 3 a 4 gramos diarios para prevenir sobrecarga y toxicidad hepática. Respeta siempre el intervalo mínimo de 6 a 8 horas entre tomas."
            )
        }
        else -> {
            MediClinicalDossier(
                queryId = "general",
                title = "Diagnóstico Personalizado de Tratamiento",
                category = "INTELIGENCIA CLÍNICA VITAL",
                riskLevel = "MONITOREO ACTIVO",
                riskColor = Color(0xFF10B981),
                riskScore = 0.30f,
                keyInsight = "Monitoreando activamente tus tratamientos. Cumplir tus horarios pautados reduce el riesgo de complicaciones crónicas.",
                points = listOf(
                    DossierPoint(
                        icon = Icons.Outlined.CheckCircle,
                        label = "Adherencia Terapéutica",
                        description = "Registrar tus dosis a tiempo fortalece tu racha y asegura la biodisponibilidad del fármaco."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.HealthAndSafety,
                        label = "Validación Farmacológica",
                        description = "Tus medicamentos se contrastan con alergias registradas para evitar reacciones adversas."
                    ),
                    DossierPoint(
                        icon = Icons.Outlined.Phone,
                        label = "Contacto Clínico de Apoyo",
                        description = "Dra. Elena Ramos se encuentra vinculada para emergencias o dudas de ajuste."
                    )
                ),
                goldenRule = "Registra puntualmente cada toma para mantener tu salud protegida.",
                fullVoiceScript = "He analizado tu consulta sobre tu medicación. Como tu compañero clínico inteligente, te aconsejo registrar puntualmente cada toma en la app para mantener tu racha y proteger tu organismo. Ante dudas diagnósticas o ajustes de dosis, consulta con tu médico tratante Dra. Elena Ramos."
            )
        }
    }
}

fun answerClinicalQuery(query: String, nombreUsuario: String): String {
    return buildClinicalDossier(query, nombreUsuario).fullVoiceScript
}

/**
 * Espectro animado de ondas de voz ("Living Voice Waveform").
 */
@Composable
fun LivingVoiceWaveform(
    isSpeaking: Boolean,
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "waveform_anim")
    val phase1 by infiniteTransition.animateFloat(
        initialValue = 0.2f, targetValue = 1.0f,
        animationSpec = infiniteRepeatable(tween(380, easing = EaseInOutSine), RepeatMode.Reverse),
        label = "w1"
    )
    val phase2 by infiniteTransition.animateFloat(
        initialValue = 0.9f, targetValue = 0.25f,
        animationSpec = infiniteRepeatable(tween(510, easing = EaseInOutSine), RepeatMode.Reverse),
        label = "w2"
    )
    val phase3 by infiniteTransition.animateFloat(
        initialValue = 0.35f, targetValue = 1.0f,
        animationSpec = infiniteRepeatable(tween(340, easing = EaseInOutSine), RepeatMode.Reverse),
        label = "w3"
    )
    val phase4 by infiniteTransition.animateFloat(
        initialValue = 0.85f, targetValue = 0.2f,
        animationSpec = infiniteRepeatable(tween(460, easing = EaseInOutSine), RepeatMode.Reverse),
        label = "w4"
    )
    val phase5 by infiniteTransition.animateFloat(
        initialValue = 0.4f, targetValue = 0.95f,
        animationSpec = infiniteRepeatable(tween(410, easing = EaseInOutSine), RepeatMode.Reverse),
        label = "w5"
    )

    Row(
        modifier = modifier.height(20.dp),
        horizontalArrangement = Arrangement.spacedBy(2.5.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        val phases = listOf(phase1, phase2, phase3, phase4, phase5)
        phases.forEach { p ->
            val barHeight = if (isSpeaking) (5.dp + 15.dp * p) else (3.dp + 3.dp * p)
            Box(
                modifier = Modifier
                    .width(2.5.dp)
                    .height(barHeight)
                    .clip(RoundedCornerShape(50))
                    .background(
                        Brush.verticalGradient(
                            listOf(
                                TealPrimary,
                                Color(0xFF0F766E)
                            )
                        )
                    )
            )
        }
    }
}

data class QuickClinicalTopic(
    val query: String,
    val label: String,
    val icon: ImageVector
)

private val QUICK_CLINICAL_TOPICS = listOf(
    QuickClinicalTopic("¿Puedo tomar café con mi medicamento?", "Café y fármacos", Icons.Outlined.AccessAlarm),
    QuickClinicalTopic("¿Qué hago si olvidé mi dosis?", "Dosis olvidada", Icons.Outlined.Shield),
    QuickClinicalTopic("¿Puedo tomar alcohol con mis medicamentos?", "Alcohol y peligro", Icons.Outlined.Warning),
    QuickClinicalTopic("¿Por qué la Insulina es crítica?", "Insulina Crítica", Icons.Outlined.LocalFireDepartment),
    QuickClinicalTopic("¿Cómo debo tomar con agua?", "Toma con agua", Icons.Outlined.WaterDrop),
    QuickClinicalTopic("Margen de seguridad paracetamol", "Paracetamol Seguro", Icons.Outlined.Medication)
)

/**
 * Diálogo interactivo amigable con Medi:
 * Diseño cálido (no neón), flotante sin abarcar toda la pantalla, con saludo cercano
 * y expansión animada orgánica (animateContentSize) a medida que el texto se va generando.
 */
/**
 * Cuadro de Texto Emergente Directo de Medi:
 * Emerge directamente desde la mascota flotante con animación elástica (TransformOrigin(0.5f, 0f)).
 * Dispone de dictado por voz local continuo con fallback automático a dictado de Google nativo,
 * lectura en voz alta TTS interactiva con 1 toque, respuestas clínicas tipo dossier y selector de tópicos.
 */
@Composable
fun MediDirectEmergentChatCard(
    nombreUsuario: String = "Paciente",
    contextoPantalla: String = "Hoy",
    onDismiss: () -> Unit,
    onMoodChange: (MediMood) -> Unit = {}
) {
    val context = LocalContext.current
    val a11y = LocalAccessibilitySettings.current
    val coroutineScope = rememberCoroutineScope()

    var userPrompt by remember { mutableStateOf("") }
    var isSpeaking by remember { mutableStateOf(false) }
    var isGenerating by remember { mutableStateOf(false) }

    val isListening by VoiceInputHelper.isListening.collectAsState()
    val liveSpokenText by VoiceInputHelper.liveSpokenText.collectAsState()
    val soundLevel by VoiceInputHelper.soundLevel.collectAsState()
    val sttError by VoiceInputHelper.lastError.collectAsState()

    val initialGreeting = "¡Hola, $nombreUsuario! ¿En qué puedo apoyarte hoy? Puedes consultarme sobre tus medicamentos, tomas olvidadas o cuidados de salud."
    var displayedText by remember { mutableStateOf(initialGreeting) }
    var activeGoldenRule by remember { mutableStateOf("") }
    var activeCategory by remember { mutableStateOf("CONSEJO CLÍNICO") }

    val askQuestion: (String) -> Unit = { query ->
        VoiceInputHelper.stopListening()
        val dossier = buildClinicalDossier(query, nombreUsuario)
        activeGoldenRule = dossier.goldenRule
        activeCategory = dossier.category
        onMoodChange(MediMood.TALKING)
        isSpeaking = true

        coroutineScope.launch {
            isGenerating = true
            displayedText = ""
            val fullText = "${dossier.keyInsight}\n\n${dossier.goldenRule}\n\n" +
                dossier.points.joinToString("\n") { pt -> "• ${pt.label}: ${pt.description}" }

            val words = fullText.split(" ")
            for (i in words.indices) {
                displayedText = words.take(i + 1).joinToString(" ")
                delay(30)
            }
            isGenerating = false

            TtsHelper.speak(context, dossier.fullVoiceScript, key = "medi_emergent_answer")
            delay(5500)
            isSpeaking = false
            onMoodChange(MediMood.NORMAL)
        }
    }

    val systemSpeechLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            val spoken = result.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull()?.trim()
            if (!spoken.isNullOrBlank()) {
                userPrompt = spoken
                askQuestion(spoken)
            }
        }
    }

    val micPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            TtsHelper.stop()
            VoiceInputHelper.startListening(
                context = context,
                onError = { err ->
                    android.util.Log.i("MedReminderSTT", "Error local STT ($err) -> abriendo diálogo nativo del sistema")
                    runCatching {
                        systemSpeechLauncher.launch(
                            VoiceInputHelper.createSystemSpeechIntent("Habla con Medi...")
                        )
                    }
                },
                onResult = { spokenText ->
                    if (spokenText.isNotBlank()) {
                        userPrompt = spokenText
                        askQuestion(spokenText)
                    }
                }
            )
        }
    }

    // Saludo amigable con voz al desplegarse
    LaunchedEffect(Unit) {
        delay(250)
        TtsHelper.speak(context, "¡Hola $nombreUsuario! ¿En qué puedo apoyarte hoy?", key = "medi_emergent_greeting")
    }

    // Si el usuario dicta por voz, sincronizar el texto en vivo
    LaunchedEffect(liveSpokenText) {
        if (isListening && liveSpokenText.isNotBlank()) {
            userPrompt = liveSpokenText
        }
    }

    val safeDismiss: () -> Unit = {
        VoiceInputHelper.stopListening()
        TtsHelper.stop()
        onDismiss()
    }

    val startVoiceListening = {
        val hasMicPermission = ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED
        if (hasMicPermission) {
            TtsHelper.stop()
            VoiceInputHelper.startListening(
                context = context,
                onError = { err ->
                    android.util.Log.i("MedReminderSTT", "Error local STT ($err) -> Fallback automático a diálogo nativo")
                    runCatching {
                        systemSpeechLauncher.launch(
                            VoiceInputHelper.createSystemSpeechIntent("Habla con Medi...")
                        )
                    }
                },
                onResult = { spokenText ->
                    if (spokenText.isNotBlank()) {
                        userPrompt = spokenText
                        askQuestion(spokenText)
                    }
                }
            )
        } else {
            micPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null
            ) { /* Consumir eventos dentro de la tarjeta */ },
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Pico superior orgánico que conecta físicamente con la mascota
        Canvas(
            modifier = Modifier
                .size(18.dp, 9.dp)
                .offset(y = 1.dp)
        ) {
            val path = Path().apply {
                moveTo(size.width / 2f, 0f)
                lineTo(size.width, size.height)
                lineTo(0f, size.height)
                close()
            }
            drawPath(path, color = if (a11y.isDarkTheme) Color(0xFF1E293B) else Color.White)
        }

        Surface(
            shape = RoundedCornerShape(26.dp),
            color = if (a11y.isDarkTheme) Color(0xFF1E293B) else Color.White,
            border = BorderStroke(1.2.dp, if (a11y.isDarkTheme) Color(0xFF334155) else TealPrimary.copy(alpha = 0.28f)),
            shadowElevation = 20.dp,
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(max = 500.dp)
                .imePadding()
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 18.dp, vertical = 14.dp)
            ) {
                // Cabecera: Nombre + Badge IA + Estado + Botón Cerrar
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f, fill = false)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "Medi",
                                fontSize = 18.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = a11y.adaptiveTextPrimary
                            )
                            Spacer(Modifier.width(8.dp))
                            Surface(
                                shape = RoundedCornerShape(50),
                                color = TealBadgeBg
                            ) {
                                Text(
                                    text = activeCategory,
                                    fontSize = 9.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TealDark,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                                )
                            }
                        }
                        Spacer(Modifier.height(2.dp))
                        Text(
                            text = if (isListening) "Te estoy escuchando..." else if (isGenerating) "Analizando respuesta médica..." else if (isSpeaking) "Hablando contigo..." else "¿En qué puedo apoyarte hoy?",
                            fontSize = 11.5.sp,
                            color = if (isListening) Color(0xFFEF4444) else if (isGenerating || isSpeaking) TealPrimary else a11y.adaptiveTextSecondary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }

                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        LivingVoiceWaveform(isSpeaking = isSpeaking || isListening)

                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(CircleShape)
                                .background(a11y.adaptiveSoftSurface)
                                .bounceClick()
                                .clickable { safeDismiss() },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Close,
                                contentDescription = "Cerrar diálogo",
                                tint = a11y.adaptiveTextPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                }

                Spacer(Modifier.height(10.dp))

                // Contenido escroleable
                Column(
                    modifier = Modifier
                        .weight(1f, fill = false)
                        .verticalScroll(rememberScrollState())
                ) {
                    // Tarjeta de Respuesta Clínica
                    Surface(
                        shape = RoundedCornerShape(18.dp),
                        color = if (a11y.isDarkTheme) Color(0xFF0F172A) else Color(0xFFF8FAFC),
                        border = BorderStroke(1.dp, if (a11y.isDarkTheme) Color(0xFF334155) else a11y.adaptiveBorder),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(14.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.Top
                            ) {
                                Row(modifier = Modifier.weight(1f)) {
                                    Icon(
                                        imageVector = Icons.Outlined.AutoAwesome,
                                        contentDescription = null,
                                        tint = TealPrimary,
                                        modifier = Modifier
                                            .size(17.dp)
                                            .padding(top = 2.dp)
                                    )
                                    Spacer(Modifier.width(8.dp))
                                    Text(
                                        text = displayedText,
                                        fontSize = 13.5.sp,
                                        lineHeight = 20.sp,
                                        color = a11y.adaptiveTextPrimary,
                                        fontWeight = FontWeight.Medium
                                    )
                                }
                                IconButton(
                                    onClick = {
                                        if (isSpeaking) {
                                            TtsHelper.stop()
                                            isSpeaking = false
                                        } else {
                                            TtsHelper.speak(context, displayedText, key = "medi_card_answer")
                                            isSpeaking = true
                                        }
                                    },
                                    modifier = Modifier.size(32.dp)
                                ) {
                                    if (isSpeaking) {
                                        LivingVoiceWaveform(isSpeaking = true, modifier = Modifier.size(16.dp))
                                    } else {
                                        Icon(
                                            imageVector = Icons.AutoMirrored.Outlined.VolumeUp,
                                            contentDescription = "Escuchar respuesta",
                                            tint = TealPrimary,
                                            modifier = Modifier.size(18.dp)
                                        )
                                    }
                                }
                            }

                            if (!isGenerating && activeGoldenRule.isNotBlank()) {
                                Spacer(Modifier.height(8.dp))
                                Surface(
                                    shape = RoundedCornerShape(12.dp),
                                    color = TealBadgeBg,
                                    border = BorderStroke(1.dp, TealPrimary.copy(alpha = 0.25f))
                                ) {
                                    Row(
                                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Icon(
                                            imageVector = Icons.Outlined.Shield,
                                            contentDescription = null,
                                            tint = TealPrimary,
                                            modifier = Modifier.size(13.dp)
                                        )
                                        Spacer(Modifier.width(5.dp))
                                        Text(
                                            text = activeGoldenRule,
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.SemiBold,
                                            color = TealDark
                                        )
                                    }
                                }
                            }
                        }
                    }

                    Spacer(Modifier.height(10.dp))

                    // Chips rápidos de preguntas frecuentes
                    LazyRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        items(QUICK_CLINICAL_TOPICS) { q ->
                            Surface(
                                shape = RoundedCornerShape(50),
                                color = a11y.adaptiveSoftSurface,
                                border = BorderStroke(0.8.dp, a11y.adaptiveBorder),
                                modifier = Modifier
                                    .bounceClick()
                                    .clickable { askQuestion(q.query) }
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = q.icon,
                                        contentDescription = null,
                                        tint = TealPrimary,
                                        modifier = Modifier.size(13.dp)
                                    )
                                    Spacer(Modifier.width(4.dp))
                                    Text(
                                        text = q.label,
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = a11y.adaptiveTextPrimary
                                    )
                                }
                            }
                        }
                    }
                }

                // Indicador de escucha activa en vivo
                if (isListening) {
                    Spacer(Modifier.height(8.dp))
                    Surface(
                        shape = RoundedCornerShape(14.dp),
                        color = Color(0xFFEF4444).copy(alpha = 0.10f),
                        border = BorderStroke(1.dp, Color(0xFFEF4444).copy(alpha = 0.35f)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 12.dp, vertical = 6.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                (0..4).forEach { i ->
                                    val mod = 1f - kotlin.math.abs(2 - i) * 0.18f
                                    val barHeight = (8f + (soundLevel * 18f * mod)).coerceIn(6f, 24f).dp
                                    Box(
                                        modifier = Modifier
                                            .width(3.dp)
                                            .height(barHeight)
                                            .clip(RoundedCornerShape(50))
                                            .background(Color(0xFFEF4444))
                                    )
                                }
                                Spacer(Modifier.width(4.dp))
                                Text(
                                    text = if (liveSpokenText.isNotBlank()) liveSpokenText else "Escuchando... habla ahora",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = if (liveSpokenText.isNotBlank()) a11y.adaptiveTextPrimary else Color(0xFFEF4444),
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }

                            Surface(
                                shape = RoundedCornerShape(50),
                                color = Color(0xFFEF4444),
                                modifier = Modifier
                                    .clip(RoundedCornerShape(50))
                                    .clickable {
                                        VoiceInputHelper.stopListening()
                                        if (userPrompt.isNotBlank()) {
                                            val q = userPrompt
                                            userPrompt = ""
                                            askQuestion(q)
                                        }
                                    }
                            ) {
                                Text(
                                    text = "Listo",
                                    fontSize = 10.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color.White,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }
                        }
                    }
                }

                Spacer(Modifier.height(10.dp))

                // Barra de entrada inferior: Input + Micrófono + Botón Dictado de Voz Nativo + Enviar
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    OutlinedTextField(
                        value = userPrompt,
                        onValueChange = { userPrompt = it },
                        placeholder = {
                            Text(
                                text = if (isListening) "Escuchando tu voz..." else "Pregúntale a Medi...",
                                fontSize = 12.5.sp,
                                color = if (isListening) Color(0xFFEF4444) else a11y.adaptiveTextSecondary
                            )
                        },
                        shape = RoundedCornerShape(50),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = if (isListening) Color(0xFFEF4444) else TealPrimary,
                            unfocusedBorderColor = if (isListening) Color(0xFFEF4444) else a11y.adaptiveBorder,
                            focusedTextColor = a11y.adaptiveTextPrimary,
                            unfocusedTextColor = a11y.adaptiveTextPrimary,
                            focusedContainerColor = a11y.adaptiveSoftSurface,
                            unfocusedContainerColor = a11y.adaptiveSoftSurface
                        ),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )

                    // Botón Micrófono Continuo
                    Surface(
                        shape = CircleShape,
                        color = if (isListening) Color(0xFFEF4444) else a11y.adaptiveSoftSurface,
                        border = BorderStroke(1.2.dp, if (isListening) Color(0xFFEF4444) else a11y.adaptiveBorder),
                        modifier = Modifier
                            .size(44.dp)
                            .clip(CircleShape)
                            .bounceClick()
                            .clickable {
                                if (isListening) {
                                    VoiceInputHelper.stopListening()
                                    if (userPrompt.isNotBlank()) {
                                        val query = userPrompt
                                        userPrompt = ""
                                        askQuestion(query)
                                    }
                                } else {
                                    startVoiceListening()
                                }
                            }
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Outlined.Mic,
                                contentDescription = if (isListening) "Detener escucha" else "Hablar por voz",
                                tint = if (isListening) Color.White else a11y.adaptiveTextPrimary,
                                modifier = Modifier.size(19.dp)
                            )
                        }
                    }

                    // Botón Dictado Nativo del Sistema (Google Voice Launcher)
                    Surface(
                        shape = CircleShape,
                        color = a11y.adaptiveSoftSurface,
                        border = BorderStroke(1.dp, TealPrimary.copy(alpha = 0.5f)),
                        modifier = Modifier
                            .size(44.dp)
                            .clip(CircleShape)
                            .bounceClick()
                            .clickable {
                                TtsHelper.stop()
                                runCatching {
                                    systemSpeechLauncher.launch(
                                        VoiceInputHelper.createSystemSpeechIntent("Habla con Medi...")
                                    )
                                }
                            }
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Outlined.AutoAwesome,
                                contentDescription = "Dictado de voz del sistema",
                                tint = TealDark,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }

                    // Botón Enviar
                    Surface(
                        shape = CircleShape,
                        color = TealPrimary,
                        modifier = Modifier
                            .size(44.dp)
                            .clip(CircleShape)
                            .bounceClick()
                            .clickable {
                                if (userPrompt.isNotBlank()) {
                                    val text = userPrompt
                                    userPrompt = ""
                                    askQuestion(text)
                                }
                            }
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.AutoMirrored.Outlined.Send,
                                contentDescription = "Enviar",
                                tint = Color.White,
                                modifier = Modifier.size(17.dp)
                            )
                        }
                    }
                }

                if (sttError != null) {
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = sttError ?: "",
                        fontSize = 10.5.sp,
                        color = Color(0xFFEF4444),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}

@Composable
fun FriendlyMediChatCard(
    onDismiss: () -> Unit,
    contextoPantalla: String = "Hoy",
    nombreUsuario: String = "Paciente"
) {
    MediDirectEmergentChatCard(
        nombreUsuario = nombreUsuario,
        contextoPantalla = contextoPantalla,
        onDismiss = onDismiss
    )
}

@Composable
fun MediAssistantDialog(
    onDismiss: () -> Unit,
    contextoPantalla: String = "Hoy",
    nombreUsuario: String = "Paciente"
) {
    FriendlyMediChatCard(
        onDismiss = onDismiss,
        contextoPantalla = contextoPantalla,
        nombreUsuario = nombreUsuario
    )
}


