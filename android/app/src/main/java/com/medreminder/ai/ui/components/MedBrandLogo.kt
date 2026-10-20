package com.medreminder.ai.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Logo minimalista y orgánico de MedReminder AI:
 * Silueta squircle suave en degradado Teal Clínico (#1A4B56 -> #286675 -> #347B8B),
 * halo orgánico menta (#A8E6CF) y cápsula inclinada bicolor minimalista (#FFFFFF / #A8E6CF)
 * con curva vital suave.
 */
@Composable
fun MedBrandLogo(
    size: Dp = 40.dp,
    cornerRadius: Dp = 11.dp,
    modifier: Modifier = Modifier
) {
    Canvas(modifier = modifier.size(size)) {
        val w = this.size.width
        val h = this.size.height
        val center = Offset(w * 0.5f, h * 0.5f)

        // Curvatura más orgánica y amigable (mínimo 36% del tamaño para evitar aspecto cuadrado rígido)
        val organicRadius = maxOf(cornerRadius.toPx(), w * 0.36f)

        // 1. Base squircle suave con degradado cálido Teal
        drawRoundRect(
            brush = Brush.linearGradient(
                colors = listOf(
                    Color(0xFF1A4B56),
                    Color(0xFF286675),
                    Color(0xFF357F90)
                ),
                start = Offset(0f, 0f),
                end = Offset(w, h)
            ),
            size = Size(w, h),
            cornerRadius = CornerRadius(organicRadius, organicRadius)
        )

        // 2. Halo orgánico suave interior en verde salvia / menta
        drawCircle(
            color = Color(0xFFA8E6CF).copy(alpha = 0.16f),
            radius = w * 0.36f,
            center = Offset(w * 0.48f, h * 0.52f)
        )

        // 3. Cápsula minimalista inclinada (-36°) dividida en dos tonos (Blanco Cálido + Menta Suave)
        val pillWidth = w * 0.27f
        val pillHeight = h * 0.56f
        val pillLeft = (w - pillWidth) / 2f
        val pillTop = (h - pillHeight) / 2f
        val pillRadius = pillWidth / 2f

        withTransform({
            rotate(degrees = -36f, pivot = center)
        }) {
            val pillPath = Path().apply {
                addRoundRect(
                    RoundRect(
                        rect = Rect(
                            offset = Offset(pillLeft, pillTop),
                            size = Size(pillWidth, pillHeight)
                        ),
                        cornerRadius = CornerRadius(pillRadius, pillRadius)
                    )
                )
            }

            clipPath(pillPath) {
                // Mitad superior: Crema/Blanco puro luminoso
                drawRect(
                    color = Color(0xFFFFFFFF),
                    topLeft = Offset(pillLeft, pillTop),
                    size = Size(pillWidth, pillHeight * 0.5f)
                )
                // Mitad inferior: Verde menta / salvia orgánico (#A8E6CF)
                drawRect(
                    color = Color(0xFFA8E6CF),
                    topLeft = Offset(pillLeft, pillTop + pillHeight * 0.5f),
                    size = Size(pillWidth, pillHeight * 0.5f)
                )
            }

            // Sutil brillo lateral en la cápsula para volumen minimalista
            drawLine(
                color = Color.White.copy(alpha = 0.45f),
                start = Offset(pillLeft + pillWidth * 0.28f, pillTop + pillHeight * 0.20f),
                end = Offset(pillLeft + pillWidth * 0.28f, pillTop + pillHeight * 0.43f),
                strokeWidth = w * 0.032f,
                cap = StrokeCap.Round
            )
        }

        // 4. Punto orgánico / hoja vital en menta cálido arriba a la derecha
        val leafCenter = Offset(w * 0.73f, h * 0.27f)
        drawCircle(
            color = Color(0xFFA8E6CF),
            radius = w * 0.065f,
            center = leafCenter
        )

        // 5. Arco de pulso vital minimalista alrededor del borde inferior derecho
        val arcPath = Path().apply {
            moveTo(w * 0.62f, h * 0.76f)
            quadraticTo(
                w * 0.77f,
                h * 0.75f,
                w * 0.78f,
                h * 0.60f
            )
        }
        drawPath(
            path = arcPath,
            color = Color(0xFFA8E6CF).copy(alpha = 0.75f),
            style = Stroke(width = w * 0.042f, cap = StrokeCap.Round)
        )
    }
}

