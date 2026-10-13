package com.medreminder.ai.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Logo oficial de MedReminder AI:
 * Recuadro redondeado azul profundo (#165684), círculo interior (#3A6D94),
 * cruz médica blanca de extremos redondeados y estrella de 4 puntas lavanda (#A2ACFA).
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

        // 1. Fondo redondeado azul profundo
        drawRoundRect(
            color = Color(0xFF165684),
            size = Size(w, h),
            cornerRadius = CornerRadius(cornerRadius.toPx(), cornerRadius.toPx())
        )

        // 2. Círculo central azul medio
        drawCircle(
            color = Color(0xFF3A6D94),
            radius = w * 0.34f,
            center = Offset(w * 0.5f, h * 0.5f)
        )

        // 3. Cruz blanca con bordes redondeados
        val barThickness = w * 0.145f
        val barLength = w * 0.48f
        val barRadius = CornerRadius(barThickness / 2f, barThickness / 2f)

        // Barra vertical
        drawRoundRect(
            color = Color.White,
            topLeft = Offset((w - barThickness) / 2f, (h - barLength) / 2f),
            size = Size(barThickness, barLength),
            cornerRadius = barRadius
        )

        // Barra horizontal
        drawRoundRect(
            color = Color.White,
            topLeft = Offset((w - barLength) / 2f, (h - barThickness) / 2f),
            size = Size(barLength, barThickness),
            cornerRadius = barRadius
        )

        // 4. Estrella de 4 puntas lavanda arriba a la derecha
        val sx = w * 0.70f
        val sy = h * 0.31f
        val outer = w * 0.125f
        val inner = w * 0.032f

        val starPath = Path().apply {
            moveTo(sx, sy - outer)
            lineTo(sx + inner, sy - inner)
            lineTo(sx + outer, sy)
            lineTo(sx + inner, sy + inner)
            lineTo(sx, sy + outer)
            lineTo(sx - inner, sy + inner)
            lineTo(sx - outer, sy)
            lineTo(sx - inner, sy - inner)
            close()
        }
        drawPath(path = starPath, color = Color(0xFFA2ACFA))
    }
}
