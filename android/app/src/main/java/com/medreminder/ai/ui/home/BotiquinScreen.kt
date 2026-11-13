package com.medreminder.ai.ui.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AddCircleOutline
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.Healing
import androidx.compose.material.icons.outlined.MedicalInformation
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.PauseCircleOutline
import androidx.compose.material.icons.outlined.PlayCircleOutline
import androidx.compose.material.icons.outlined.Vaccines
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
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
    onAddMedicamentoClick: () -> Unit,
    onEscanearRecetaClick: () -> Unit = {},
    onRecargarStock: (Int, Int) -> Unit = { _, _ -> },
    onEliminarMedicamento: (Int) -> Unit = {},
    onEditarMedicamento: (
        idMedicamento: Int,
        nombre: String,
        principioActivo: String?,
        dosis: String,
        cantidadStock: Int,
        forma: FormaFarmaceutica,
        colorPastilla: String,
        instruccionesToma: String?,
        permitePosponer: Boolean,
        esCritico: Boolean,
        contraindicaciones: String?
    ) -> Unit = { _, _, _, _, _, _, _, _, _, _, _ -> },
    onActualizarTratamiento: (idTratamiento: Int, frecuenciaHoras: Int?, estado: String?) -> Unit = { _, _, _ -> }
) {
    val a11y = LocalAccessibilitySettings.current
    val totalMeds = state.botiquinItems.size
    var refillDialogItem by remember { mutableStateOf<BotiquinItemUi?>(null) }
    var editDialogItem by remember { mutableStateOf<BotiquinItemUi?>(null) }

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 18.dp, bottom = 96.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Cabecera "Mi Botiquín" + botones "Receta IA" y "+ Agregar"
            item {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Mi Botiquín",
                            fontSize = 22.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = a11y.adaptiveTextPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f, fill = false)
                        )
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = TealBadgeBg,
                                border = BorderStroke(1.dp, TealPrimary.copy(alpha = 0.45f)),
                                modifier = Modifier
                                    .clip(RoundedCornerShape(16.dp))
                                    .clickable { onEscanearRecetaClick() }
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 11.dp, vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = "📷 Receta IA",
                                        fontSize = 12.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = TealPrimary
                                    )
                                }
                            }

                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = TealPrimary,
                                modifier = Modifier
                                    .clip(RoundedCornerShape(16.dp))
                                    .clickable { onAddMedicamentoClick() }
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Add,
                                        contentDescription = null,
                                        tint = Color.White,
                                        modifier = Modifier.size(16.dp)
                                    )
                                    Spacer(Modifier.width(4.dp))
                                    Text(
                                        text = "Agregar",
                                        fontSize = 12.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color.White
                                    )
                                }
                            }
                        }
                    }
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = "$totalMeds medicamentos en seguimiento activo",
                        fontSize = 15.sp,
                        color = a11y.adaptiveTextSecondary
                    )
                }
            }

            // Tarjeta "ESTADO GLOBAL - % de suministros asegurados"
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
                    color = a11y.adaptiveSoftSurface,
                    border = BorderStroke(1.dp, a11y.adaptiveBorder),
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
                                color = a11y.adaptiveTextPrimary
                            )
                            Spacer(Modifier.height(4.dp))
                            Text(
                                text = "Próxima reposición estimada en ${state.diasReposicionEstimada} días",
                                fontSize = 13.sp,
                                color = a11y.adaptiveTextSecondary
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
                        color = a11y.adaptiveCardSurface,
                        border = BorderStroke(1.dp, a11y.adaptiveBorder),
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
                                color = a11y.adaptiveTextPrimary
                            )
                            Spacer(Modifier.height(6.dp))
                            Text(
                                text = "Agrega tu primer medicamento para monitorear tus existencias y programar recordatorios.",
                                fontSize = 14.sp,
                                color = a11y.adaptiveTextSecondary,
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
                    BotiquinMedCard(
                        item = item,
                        iconIndex = index,
                        onRecargarStock = { refillDialogItem = item },
                        onEditarMedicamento = { editDialogItem = item },
                        onToggleTratamientoEstado = {
                            val idTrat = item.idTratamiento ?: return@BotiquinMedCard
                            val nextEstado = if (item.tratamientoEstado == "pausado") "activo" else "pausado"
                            onActualizarTratamiento(idTrat, null, nextEstado)
                        },
                        onEliminarMedicamento = { onEliminarMedicamento(item.idMedicamento) }
                    )
                }
            }
        }

        refillDialogItem?.let { target ->
            RecargarStockDialog(
                item = target,
                onDismiss = { refillDialogItem = null },
                onConfirm = { cantidad ->
                    onRecargarStock(target.idMedicamento, cantidad)
                    refillDialogItem = null
                }
            )
        }

        editDialogItem?.let { target ->
            EditarMedicamentoDialog(
                item = target,
                onDismiss = { editDialogItem = null },
                onGuardar = { nombre, principio, dosis, stock, forma, instrucciones, permitePosponer, esCritico, contraindicaciones, nuevaFrec, nuevoEstado ->
                    onEditarMedicamento(
                        target.idMedicamento,
                        nombre,
                        principio,
                        dosis,
                        stock,
                        forma,
                        target.colorPastilla,
                        instrucciones,
                        permitePosponer,
                        esCritico,
                        contraindicaciones
                    )
                    val idTrat = target.idTratamiento
                    if (idTrat != null && (nuevaFrec != target.frecuenciaHoras || nuevoEstado != target.tratamientoEstado)) {
                        onActualizarTratamiento(
                            idTrat,
                            if (nuevaFrec != target.frecuenciaHoras) nuevaFrec else null,
                            if (nuevoEstado != target.tratamientoEstado) nuevoEstado else null
                        )
                    }
                    editDialogItem = null
                }
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

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun BotiquinMedCard(
    item: BotiquinItemUi,
    iconIndex: Int,
    onRecargarStock: () -> Unit = {},
    onEditarMedicamento: () -> Unit = {},
    onToggleTratamientoEstado: () -> Unit = {},
    onEliminarMedicamento: () -> Unit = {}
) {
    val a11y = LocalAccessibilitySettings.current
    val isBajo = item.nivel == StockNivel.BAJO
    val badgeBg = if (isBajo) AlertRedBg else a11y.adaptiveSoftSurface
    val badgeTextCol = if (isBajo) AlertRedText else a11y.adaptiveTextPrimary
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
        color = a11y.adaptiveCardSurface,
        border = BorderStroke(1.dp, a11y.adaptiveBorder),
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
                        color = a11y.adaptiveTextPrimary
                    )
                    Spacer(Modifier.height(3.dp))
                    Text(
                        text = item.subtituloDosis,
                        fontSize = 14.sp,
                        color = a11y.adaptiveTextSecondary,
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
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp)
                    )
                }
            }

            if (item.esCritico || !item.permitePosponer || item.idTratamiento != null) {
                Spacer(Modifier.height(8.dp))
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (item.esCritico || !item.permitePosponer) {
                        Surface(
                            shape = RoundedCornerShape(6.dp),
                            color = Color(0xFFFFEBEE)
                        ) {
                            Text(
                                text = "DOSIS CRÍTICA • NO POSPONIBLE",
                                color = Color(0xFFC62828),
                                fontSize = 10.sp,
                                fontWeight = FontWeight.ExtraBold,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.5.dp)
                            )
                        }
                    }
                    if (item.idTratamiento != null) {
                        val isPaused = item.tratamientoEstado == "pausado"
                        Surface(
                            shape = RoundedCornerShape(6.dp),
                            color = if (isPaused) Color(0xFFFFF8E1) else TealBadgeBg
                        ) {
                            Text(
                                text = if (isPaused) {
                                    "PAUSADO • Cada ${item.frecuenciaHoras} h"
                                } else {
                                    "Cada ${item.frecuenciaHoras} h • Activo"
                                },
                                color = if (isPaused) Color(0xFF9A6700) else TealBadgeText,
                                fontSize = 10.5.sp,
                                fontWeight = FontWeight.ExtraBold,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.5.dp)
                            )
                        }
                    }
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

            Spacer(Modifier.height(14.dp))

            // Acciones: Recargar stock, Editar, Pausar/Reanudar y Eliminar
            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.End),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedButton(
                    onClick = onRecargarStock,
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = TealPrimary),
                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.AddCircleOutline,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(Modifier.width(5.dp))
                    Text(text = "Recargar", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }

                OutlinedButton(
                    onClick = onEditarMedicamento,
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = TealDark),
                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Edit,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(Modifier.width(5.dp))
                    Text(text = "Editar", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }

                if (item.idTratamiento != null) {
                    val isPaused = item.tratamientoEstado == "pausado"
                    OutlinedButton(
                        onClick = onToggleTratamientoEstado,
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.outlinedButtonColors(
                            contentColor = if (isPaused) TealPrimary else Color(0xFF9A6700)
                        ),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        Icon(
                            imageVector = if (isPaused) Icons.Outlined.PlayCircleOutline else Icons.Outlined.PauseCircleOutline,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(Modifier.width(5.dp))
                        Text(
                            text = if (isPaused) "Reanudar" else "Pausar",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                var showConfirmDelete by remember { mutableStateOf(false) }
                IconButton(
                    onClick = { showConfirmDelete = true },
                    modifier = Modifier.size(40.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Delete,
                        contentDescription = "Eliminar",
                        tint = Color(0xFFC62828),
                        modifier = Modifier.size(20.dp)
                    )
                }

                if (showConfirmDelete) {
                    AlertDialog(
                        onDismissRequest = { showConfirmDelete = false },
                        title = { Text("Eliminar medicamento", fontWeight = FontWeight.Bold) },
                        text = { Text("¿Deseas eliminar ${item.nombre} de tu botiquín? Se detendrán sus recordatorios.") },
                        confirmButton = {
                            TextButton(onClick = {
                                showConfirmDelete = false
                                onEliminarMedicamento()
                            }) {
                                Text("Eliminar", color = Color(0xFFC62828), fontWeight = FontWeight.Bold)
                            }
                        },
                        dismissButton = {
                            TextButton(onClick = { showConfirmDelete = false }) {
                                Text("Cancelar")
                            }
                        }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun RecargarStockDialog(
    item: BotiquinItemUi,
    onDismiss: () -> Unit,
    onConfirm: (cantidadExtra: Int) -> Unit
) {
    var cantidadTexto by remember { mutableStateOf("30") }
    val presets = listOf(10, 20, 30, 60)

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Recargar ${item.nombre}", fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(
                    text = "Existencia actual: ${item.stockActual} ${item.unidadTexto}. Elige cuánto deseas agregar:",
                    fontSize = 13.5.sp,
                    color = TextSecondary
                )
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    presets.forEach { preset ->
                        FilterChip(
                            selected = cantidadTexto == preset.toString(),
                            onClick = { cantidadTexto = preset.toString() },
                            label = { Text("+$preset") }
                        )
                    }
                }
                OutlinedTextField(
                    value = cantidadTexto,
                    onValueChange = { cantidadTexto = it.filter { ch -> ch.isDigit() } },
                    label = { Text("Cantidad personalizada (${item.unidadTexto})") },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val qty = cantidadTexto.toIntOrNull()?.coerceAtLeast(1) ?: 30
                    onConfirm(qty)
                },
                colors = ButtonDefaults.buttonColors(containerColor = TealPrimary)
            ) {
                Text("Agregar", fontWeight = FontWeight.Bold, color = Color.White)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancelar") }
        }
    )
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun EditarMedicamentoDialog(
    item: BotiquinItemUi,
    onDismiss: () -> Unit,
    onGuardar: (
        nombre: String,
        principioActivo: String?,
        dosis: String,
        cantidadStock: Int,
        forma: FormaFarmaceutica,
        instrucciones: String?,
        permitePosponer: Boolean,
        esCritico: Boolean,
        contraindicaciones: String?,
        frecuenciaHoras: Int,
        estadoTratamiento: String?
    ) -> Unit
) {
    var nombre by remember { mutableStateOf(item.nombre) }
    var principio by remember { mutableStateOf(item.principioActivo ?: "") }
    var dosis by remember { mutableStateOf(item.dosis) }
    var stockTexto by remember { mutableStateOf(item.stockActual.toString()) }
    var forma by remember { mutableStateOf(item.formaFarmaceutica) }
    var instrucciones by remember { mutableStateOf(item.instruccionesToma ?: "") }
    var esCritico by remember { mutableStateOf(item.esCritico) }
    var permitePosponer by remember { mutableStateOf(item.permitePosponer) }
    var contraindicaciones by remember { mutableStateOf(item.contraindicaciones ?: "") }
    var frecuenciaHoras by remember { mutableStateOf(item.frecuenciaHoras) }
    var estadoTrat by remember { mutableStateOf(item.tratamientoEstado ?: "activo") }

    Dialog(onDismissRequest = onDismiss, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(
            shape = RoundedCornerShape(24.dp),
            color = CardBackground,
            modifier = Modifier
                .fillMaxWidth(0.93f)
                .padding(14.dp)
        ) {
            Column(
                modifier = Modifier
                    .padding(20.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Editar Medicamento",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Cerrar")
                    }
                }

                OutlinedTextField(
                    value = nombre,
                    onValueChange = { nombre = it },
                    label = { Text("Nombre comercial") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )
                OutlinedTextField(
                    value = principio,
                    onValueChange = { principio = it },
                    label = { Text("Principio activo (genérico)") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    OutlinedTextField(
                        value = dosis,
                        onValueChange = { dosis = it },
                        label = { Text("Dosis") },
                        singleLine = true,
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(14.dp)
                    )
                    OutlinedTextField(
                        value = stockTexto,
                        onValueChange = { stockTexto = it.filter { c -> c.isDigit() } },
                        label = { Text("Existencias") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(0.7f),
                        shape = RoundedCornerShape(14.dp)
                    )
                }

                Text("Forma farmacéutica:", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FormaFarmaceutica.entries.forEach { f ->
                        FilterChip(
                            selected = forma == f,
                            onClick = { forma = f },
                            label = { Text(f.shortLabel) }
                        )
                    }
                }

                OutlinedTextField(
                    value = instrucciones,
                    onValueChange = { instrucciones = it },
                    label = { Text("Instrucciones de toma") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                if (item.idTratamiento != null) {
                    Text("Frecuencia del recordatorio:", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        listOf(4, 6, 8, 12, 24).forEach { h ->
                            FilterChip(
                                selected = frecuenciaHoras == h,
                                onClick = { frecuenciaHoras = h },
                                label = { Text("Cada ${h}h") }
                            )
                        }
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = if (estadoTrat == "pausado") "Recordatorios pausados" else "Tratamiento activo",
                            fontSize = 13.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Switch(
                            checked = estadoTrat == "activo",
                            onCheckedChange = { checked ->
                                estadoTrat = if (checked) "activo" else "pausado"
                            },
                            colors = SwitchDefaults.colors(checkedThumbColor = Color.White, checkedTrackColor = TealPrimary)
                        )
                    }
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Medicamento crítico (alerta urgente)", fontSize = 13.5.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                    Switch(
                        checked = esCritico,
                        onCheckedChange = {
                            esCritico = it
                            if (it) permitePosponer = false
                        }
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Permitir posponer", fontSize = 13.5.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                    Switch(
                        checked = permitePosponer,
                        onCheckedChange = { if (!esCritico) permitePosponer = it }
                    )
                }

                OutlinedTextField(
                    value = contraindicaciones,
                    onValueChange = { contraindicaciones = it },
                    label = { Text("Contraindicaciones / Notas médicas") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                Spacer(Modifier.height(4.dp))
                Button(
                    onClick = {
                        if (nombre.isNotBlank()) {
                            onGuardar(
                                nombre.trim(),
                                principio.trim().ifBlank { null },
                                dosis.trim().ifBlank { "1 comprimido" },
                                stockTexto.toIntOrNull()?.coerceAtLeast(0) ?: item.stockActual,
                                forma,
                                instrucciones.trim().ifBlank { null },
                                permitePosponer,
                                esCritico,
                                contraindicaciones.trim().ifBlank { null },
                                frecuenciaHoras,
                                estadoTrat
                            )
                        }
                    },
                    shape = RoundedCornerShape(14.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                    modifier = Modifier.fillMaxWidth().height(50.dp)
                ) {
                    Text("Guardar Cambios", fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
        }
    }
}
