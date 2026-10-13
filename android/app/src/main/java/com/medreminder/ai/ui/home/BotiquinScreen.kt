package com.medreminder.ai.ui.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.Healing
import androidx.compose.material.icons.outlined.MedicalInformation
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.Vaccines
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.ProgressBrown
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealBadgeText
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import com.medreminder.ai.ui.theme.TealSoftBg
import com.medreminder.ai.ui.theme.TextPrimary
import com.medreminder.ai.ui.theme.TextSecondary

/**
 * Pantalla 6: Mi Botiquín (inventario de medicamentos, estado global y botón flotante +).
 */
@Composable
fun BotiquinScreenContent(
    state: HomeUiState,
    onAddMedicamentoClick: () -> Unit
) {
    val totalMeds = state.botiquinItems.size

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 18.dp, bottom = 96.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Cabecera "Mi Botiquín" + badge "• Al día"
            item {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Mi Botiquín",
                            fontSize = 28.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary
                        )
                        Surface(
                            shape = RoundedCornerShape(50),
                            color = TealBadgeBg
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(8.dp)
                                        .clip(CircleShape)
                                        .background(TealPrimary)
                                )
                                Spacer(Modifier.width(6.dp))
                                Text(
                                    text = "Al día",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TealBadgeText
                                )
                            }
                        }
                    }
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = "$totalMeds medicamentos en seguimiento activo",
                        fontSize = 15.sp,
                        color = TextSecondary
                    )
                }
            }

            // Tarjeta "ESTADO GLOBAL - % de suministros asegurados"
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
                    color = SoftWarmSurface,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(20.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "ESTADO GLOBAL",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.ExtraBold,
                                letterSpacing = 0.8.sp,
                                color = TealPrimary
                            )
                            Spacer(Modifier.height(4.dp))
                            Text(
                                text = "${state.porcentajeGlobalSuministros}% de suministros asegurados",
                                fontSize = 17.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = TextPrimary
                            )
                            Spacer(Modifier.height(4.dp))
                            Text(
                                text = "Próxima reposición estimada en ${state.diasReposicionEstimada} días",
                                fontSize = 13.sp,
                                color = TextSecondary
                            )
                        }
                        Spacer(Modifier.width(12.dp))
                        SupplyRingIndicator(
                            count = totalMeds,
                            progress = state.porcentajeGlobalSuministros / 100f
                        )
                    }
                }
            }

            if (state.botiquinItems.isEmpty() && !state.isLoading) {
                item {
                    Surface(
                        shape = RoundedCornerShape(22.dp),
                        color = CardBackground,
                        border = BorderStroke(1.dp, InputBorderColor),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(
                            modifier = Modifier.padding(24.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "Tu botiquín está vacío",
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                            Spacer(Modifier.height(6.dp))
                            Text(
                                text = "Agrega tu primer medicamento para monitorear tus existencias y programar recordatorios.",
                                fontSize = 14.sp,
                                color = TextSecondary,
                                textAlign = TextAlign.Center
                            )
                            Spacer(Modifier.height(16.dp))
                            Button(
                                onClick = onAddMedicamentoClick,
                                shape = RoundedCornerShape(16.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .heightIn(min = 56.dp)
                            ) {
                                Text(
                                    text = "Nuevo Medicamento",
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
            } else {
                itemsIndexed(state.botiquinItems, key = { _, it -> it.idMedicamento }) { index, item ->
                    BotiquinMedCard(item = item, iconIndex = index)
                }
            }
        }

        // Botón flotante circular "+" (>= 56dp)
        FloatingActionButton(
            onClick = onAddMedicamentoClick,
            shape = CircleShape,
            containerColor = TealPrimary,
            contentColor = Color.White,
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(end = 24.dp, bottom = 24.dp)
                .size(64.dp)
        ) {
            Icon(
                imageVector = Icons.Default.Add,
                contentDescription = "Agregar Medicamento",
                modifier = Modifier.size(30.dp)
            )
        }
    }
}

@Composable
private fun SupplyRingIndicator(count: Int, progress: Float) {
    Box(
        modifier = Modifier.size(58.dp),
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val stroke = Stroke(width = 5.dp.toPx(), cap = StrokeCap.Round)
            drawArc(
                color = Color(0xFFDCDAD7),
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                style = stroke
            )
            drawArc(
                color = TealPrimary,
                startAngle = -90f,
                sweepAngle = 360f * progress.coerceIn(0.1f, 1f),
                useCenter = false,
                style = stroke
            )
        }
        Text(
            text = count.toString(),
            fontSize = 16.sp,
            fontWeight = FontWeight.ExtraBold,
            color = TealDark
        )
    }
}

@Composable
private fun BotiquinMedCard(item: BotiquinItemUi, iconIndex: Int) {
    val isBajo = item.nivel == StockNivel.BAJO
    val badgeBg = if (isBajo) AlertRedBg else SoftWarmSurface
    val badgeTextCol = if (isBajo) AlertRedText else TextPrimary
    val progressColor = if (isBajo) ProgressBrown else TealPrimary
    val quedanColor = if (isBajo) ProgressBrown else TealPrimary

    val iconVec = when (iconIndex % 5) {
        0 -> Icons.Outlined.Medication
        1 -> Icons.Outlined.MedicalInformation
        2 -> Icons.Outlined.Vaccines
        3 -> Icons.Outlined.FavoriteBorder
        else -> Icons.Outlined.Healing
    }

    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Top
            ) {
                Surface(
                    shape = CircleShape,
                    color = TealSoftBg,
                    modifier = Modifier.size(48.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = iconVec,
                            contentDescription = null,
                            tint = TealDark,
                            modifier = Modifier.size(22.dp)
                        )
                    }
                }
                Spacer(Modifier.width(14.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = item.nombre,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                    Spacer(Modifier.height(3.dp))
                    Text(
                        text = item.subtituloDosis,
                        fontSize = 14.sp,
                        color = TextSecondary,
                        lineHeight = 19.sp
                    )
                }
                Spacer(Modifier.width(8.dp))
                Surface(
                    shape = RoundedCornerShape(50),
                    color = badgeBg
                ) {
                    Text(
                        text = item.nivel.label,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = badgeTextCol,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp)
                    )
                }
            }

            Spacer(Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = item.textoQuedan,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = quedanColor
                )
                Text(
                    text = "${item.porcentajeRestante}% restante",
                    fontSize = 12.5.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextSecondary
                )
            }

            Spacer(Modifier.height(8.dp))

            // Barra de progreso redondeada
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(RoundedCornerShape(50))
                    .background(SoftWarmSurface)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(fraction = (item.porcentajeRestante / 100f).coerceIn(0.06f, 1f))
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(progressColor)
                )
            }
        }
    }
}
