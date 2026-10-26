package com.medreminder.ai.ui.home

import android.content.Intent
import android.net.Uri
import androidx.compose.animation.core.EaseInOutSine
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AccessAlarm
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.HealthAndSafety
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.NotificationImportant
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material.icons.outlined.Refresh
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Sms
import androidx.compose.material.icons.outlined.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.data.remote.AlertaCuidadorDto
import com.medreminder.ai.data.remote.TomaSupervisadaItemDto
import com.medreminder.ai.notifications.ActiveNativeAlarmEvent
import com.medreminder.ai.notifications.NotificationHelper
import com.medreminder.ai.notifications.ReminderAlarmScheduler
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealBadgeText
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import com.medreminder.ai.ui.theme.TealSoftBg
import com.medreminder.ai.ui.theme.TextPrimary
import com.medreminder.ai.ui.theme.TextSecondary

/**
 * Vista dedicada para el Cuidador / Familiar Supervisor:
 * Muestra el estado de adherencia en vivo del adulto mayor, alertas críticas enviadas
 * automáticamente, advertencias por posposición/omisión de medicamentos normales y bitácora de tomas.
 */
@Composable
fun CuidadorScreen(
    state: HomeUiState,
    onBack: () -> Unit,
    onRefresh: () -> Unit,
    onAtenderAlerta: (Int) -> Unit,
    onSimularAlertaCritica: () -> Unit,
    onCambiarRangoEdadDemo: (Boolean) -> Unit
) {
    val a11y = LocalAccessibilitySettings.current
    val context = LocalContext.current
    val panel = state.cuidadorPanel
    val alertasActivas = panel?.alertasActivas?.filter { !it.atendida } ?: emptyList()
    val tieneCriticaActiva = alertasActivas.any { it.esCritico || it.tipoAlerta == "critica_automatica" }
    val estadoRiesgo = panel?.estadoRiesgo ?: when {
        tieneCriticaActiva || state.tomasCriticasOmitidasHoy > 0 -> "alerta_critica"
        alertasActivas.isNotEmpty() || state.vecesOmitidasHoy > 0 -> "atencion_requerida"
        else -> "estable"
    }

    val (semaforoBg, semaforoBorder, semaforoText, semaforoLabel) = when (estadoRiesgo) {
        "alerta_critica" -> QuadColors(
            Color(0xFFFFEBEE),
            Color(0xFFEF5350),
            Color(0xFFB71C1C),
            "ALERTA CRÍTICA ACTIVA • INTERVENCIÓN INMEDIATA"
        )
        "atencion_requerida" -> QuadColors(
            Color(0xFFFFF8E1),
            Color(0xFFFFB300),
            Color(0xFFE65100),
            "ATENCIÓN REQUERIDA • OMISIÓN O RETRASO DETECTADO"
        )
        else -> QuadColors(
            Color(0xFFE8F5E9),
            Color(0xFF66BB6A),
            Color(0xFF1B5E20),
            "PACIENTE ESTABLE • PLAN AL DÍA"
        )
    }

    Scaffold(
        containerColor = a11y.adaptiveBackground,
        topBar = {
            Surface(
                color = a11y.adaptiveCardSurface,
                border = BorderStroke(0.8.dp, a11y.adaptiveBorder),
                shadowElevation = 3.dp
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        IconButton(onClick = onBack) {
                            Icon(
                                imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                                contentDescription = "Volver",
                                tint = a11y.adaptiveTextPrimary
                            )
                        }
                        Spacer(Modifier.width(4.dp))
                        Column {
                            Text(
                                text = "Vista del Cuidador",
                                fontSize = 19.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = a11y.adaptiveTextPrimary
                            )
                            Text(
                                text = "Supervisión Geriátrica y Alertas en Vivo",
                                fontSize = 12.sp,
                                color = a11y.adaptiveTextSecondary
                            )
                        }
                    }

                    IconButton(onClick = onRefresh) {
                        Icon(
                            imageVector = Icons.Outlined.Refresh,
                            contentDescription = "Actualizar panel",
                            tint = TealPrimary
                        )
                    }
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .navigationBarsPadding(),
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 14.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            // 1. Tarjeta de Semáforo Clínico del Paciente Supervisado
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
                    color = a11y.adaptiveCardSurface,
                    border = BorderStroke(1.5.dp, semaforoBorder),
                    shadowElevation = 3.dp,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Surface(
                            shape = RoundedCornerShape(50),
                            color = semaforoBg
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = if (estadoRiesgo == "estable") Icons.Outlined.CheckCircle else Icons.Outlined.NotificationImportant,
                                    contentDescription = null,
                                    tint = semaforoText,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(Modifier.width(6.dp))
                                Text(
                                    text = semaforoLabel,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = semaforoText
                                )
                            }
                        }

                        Spacer(Modifier.height(12.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.weight(1f)
                            ) {
                                Surface(
                                    shape = CircleShape,
                                    color = TealSoftBg,
                                    modifier = Modifier.size(50.dp)
                                ) {
                                    Box(contentAlignment = Alignment.Center) {
                                        Icon(
                                            imageVector = Icons.Outlined.Person,
                                            contentDescription = null,
                                            tint = TealDark,
                                            modifier = Modifier.size(28.dp)
                                        )
                                    }
                                }
                                Spacer(Modifier.width(12.dp))
                                Column {
                                    Text(
                                        text = panel?.nombrePaciente ?: state.nombreUsuario,
                                        fontSize = 19.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = a11y.adaptiveTextPrimary
                                    )
                                    val edad = panel?.edadPaciente ?: state.edadUsuario
                                    val esSenior = panel?.esAdultoMayor ?: state.esAdultoMayor
                                    Text(
                                        text = "$edad años • ${if (esSenior) "Adulto Mayor (Castigo y Supervisión Activos)" else "Joven / Adulto (Racha y Honor)"}",
                                        fontSize = 12.5.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        color = a11y.adaptiveTextSecondary
                                    )
                                }
                            }

                            // Porcentaje de adherencia hoy
                            val adhPct = panel?.adherenciaHoyPct ?: if (state.tomasHoy.isNotEmpty()) {
                                (state.tomasCompletadasCount * 100) / state.tomasHoy.size
                            } else 100

                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = TealBadgeBg
                            ) {
                                Column(
                                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = "$adhPct%",
                                        fontSize = 18.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = TealDark
                                    )
                                    Text(
                                        text = "Adherencia",
                                        fontSize = 10.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = TealBadgeText
                                    )
                                }
                            }
                        }

                        Spacer(Modifier.height(14.dp))
                        HorizontalDivider(color = a11y.adaptiveBorder)
                        Spacer(Modifier.height(12.dp))

                        // Métricas rápidas del día para el cuidador
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            CuidadorStatChip(
                                title = "Completadas",
                                value = "${panel?.tomasCompletadasHoy ?: state.tomasCompletadasCount}/${panel?.tomasTotalesHoy ?: state.tomasHoy.size}",
                                color = Color(0xFF15803D),
                                modifier = Modifier.weight(1f)
                            )
                            CuidadorStatChip(
                                title = "Omitidas Hoy",
                                value = "${panel?.tomasOmitidasHoy ?: state.vecesOmitidasHoy}",
                                color = if ((panel?.tomasOmitidasHoy ?: state.vecesOmitidasHoy) > 0) Color(0xFFE65100) else TextSecondary,
                                modifier = Modifier.weight(1f)
                            )
                            CuidadorStatChip(
                                title = "Críticas Sin Tomar",
                                value = "${panel?.tomasCriticasOmitidasHoy ?: state.tomasCriticasOmitidasHoy}",
                                color = if ((panel?.tomasCriticasOmitidasHoy ?: state.tomasCriticasOmitidasHoy) > 0) Color(0xFFB71C1C) else TextSecondary,
                                modifier = Modifier.weight(1f)
                            )
                        }

                        Spacer(Modifier.height(12.dp))

                        // Selector rápido de rango de edad para demostrar ambos modos
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            OutlinedButton(
                                onClick = { onCambiarRangoEdadDemo(true) },
                                shape = RoundedCornerShape(12.dp),
                                border = BorderStroke(
                                    1.2.dp,
                                    if (state.esAdultoMayor) Color(0xFFE65100) else InputBorderColor
                                ),
                                modifier = Modifier.weight(1f)
                            ) {
                                Text(
                                    text = "Modo 69 años (Mayor)",
                                    fontSize = 11.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (state.esAdultoMayor) Color(0xFFE65100) else a11y.adaptiveTextSecondary
                                )
                            }
                            OutlinedButton(
                                onClick = { onCambiarRangoEdadDemo(false) },
                                shape = RoundedCornerShape(12.dp),
                                border = BorderStroke(
                                    1.2.dp,
                                    if (!state.esAdultoMayor) TealPrimary else InputBorderColor
                                ),
                                modifier = Modifier.weight(1f)
                            ) {
                                Text(
                                    text = "Modo 28 años (Racha)",
                                    fontSize = 11.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (!state.esAdultoMayor) TealPrimary else a11y.adaptiveTextSecondary
                                )
                            }
                        }
                    }
                }
            }

            // 2. Acciones Rápidas de Supervisión y Prueba de Alarma / Alerta Crítica
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Button(
                        onClick = {
                            onSimularAlertaCritica()
                            NotificationHelper.showCaregiverAlertNotification(
                                context = context,
                                titulo = "🚨 ALERTA CRÍTICA AUTOMÁTICA AL CUIDADOR",
                                mensaje = "${state.nombreUsuario} omitió un medicamento CRÍTICO. Se requiere intervención inmediata del cuidador.",
                                esCritico = true
                            )
                        },
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFC62828)),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 50.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.NotificationImportant,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "Simular Alerta Crítica",
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }

                    Button(
                        onClick = {
                            val primeraToma = state.tomasHoy.firstOrNull { it.estado == "pendiente" }
                                ?: state.tomasHoy.firstOrNull()
                            ReminderAlarmScheduler.triggerImmediateNativeAlarm(
                                context = context,
                                idRecordatorio = primeraToma?.idRecordatorio ?: 777,
                                nombreMedicamento = primeraToma?.nombreMedicamento ?: "Losartán Potásico",
                                dosisDetalle = primeraToma?.dosisDetalle ?: "50 mg • 1 comprimido",
                                horaFormateada = primeraToma?.horaFormateada ?: "Ahora",
                                esCritico = primeraToma?.esCritico ?: true,
                                permitePosponer = primeraToma?.permitePosponer ?: false
                            )
                        },
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 50.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.AccessAlarm,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "Probar Alarma Nativa",
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }
                }
            }

            // 3. Bandeja de Alertas Recibidas por el Cuidador (Críticas Automáticas vs Advertencias Normales)
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Alertas al Cuidador (${alertasActivas.size} activas)",
                        fontSize = 17.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = a11y.adaptiveTextPrimary
                    )
                    if (state.cargandoPanelCuidador) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(18.dp),
                            color = TealPrimary,
                            strokeWidth = 2.dp
                        )
                    }
                }
            }

            if (alertasActivas.isEmpty()) {
                item {
                    Surface(
                        shape = RoundedCornerShape(18.dp),
                        color = a11y.adaptiveCardSurface,
                        border = BorderStroke(1.dp, a11y.adaptiveBorder),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Surface(
                                shape = CircleShape,
                                color = Color(0xFFE8F5E9),
                                modifier = Modifier.size(42.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = Icons.Outlined.CheckCircle,
                                        contentDescription = null,
                                        tint = Color(0xFF2E7D32),
                                        modifier = Modifier.size(22.dp)
                                    )
                                }
                            }
                            Spacer(Modifier.width(12.dp))
                            Column {
                                Text(
                                    text = "Sin alertas pendientes de atención",
                                    fontSize = 14.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = a11y.adaptiveTextPrimary
                                )
                                Text(
                                    text = "Cuando el adulto mayor posponga u omita un medicamento normal o crítico, la alerta aparecerá aquí en tiempo real.",
                                    fontSize = 12.5.sp,
                                    color = a11y.adaptiveTextSecondary,
                                    lineHeight = 17.sp
                                )
                            }
                        }
                    }
                }
            } else {
                items(alertasActivas, key = { it.idAlerta }) { alerta ->
                    AlertaCuidadorCard(
                        alerta = alerta,
                        onAtender = { onAtenderAlerta(alerta.idAlerta) }
                    )
                }
            }

            // 4. Bitácora de Tomas Supervisadas de Hoy
            item {
                Spacer(Modifier.height(4.dp))
                Text(
                    text = "Bitácora de Tomas Supervisadas Hoy",
                    fontSize = 17.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = a11y.adaptiveTextPrimary
                )
            }

            val listaSupervisada: List<TomaSupervisadaItemDto> = panel?.tomasHoy?.takeIf { it.isNotEmpty() }
                ?: state.tomasHoy.map {
                    TomaSupervisadaItemDto(
                        idRecordatorio = it.idRecordatorio,
                        nombreMedicamento = it.nombreMedicamento,
                        dosis = it.dosisDetalle,
                        horaProgramada = it.horaFormateada,
                        estado = it.estado,
                        esCritico = it.esCritico,
                        vecesPospuesto = it.vecesPospuesto
                    )
                }

            items(listaSupervisada, key = { it.idRecordatorio }) { item ->
                TomaSupervisadaRowCard(item = item)
            }

            item {
                Spacer(Modifier.height(24.dp))
            }
        }
    }
}

private data class QuadColors(
    val bg: Color,
    val border: Color,
    val text: Color,
    val label: String
)

@Composable
private fun CuidadorStatChip(
    title: String,
    value: String,
    color: Color,
    modifier: Modifier = Modifier
) {
    val a11y = LocalAccessibilitySettings.current
    Surface(
        shape = RoundedCornerShape(14.dp),
        color = a11y.adaptiveSoftSurface,
        modifier = modifier
    ) {
        Column(
            modifier = Modifier.padding(vertical = 8.dp, horizontal = 8.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = value,
                fontSize = 16.sp,
                fontWeight = FontWeight.ExtraBold,
                color = color
            )
            Text(
                text = title,
                fontSize = 10.5.sp,
                fontWeight = FontWeight.Medium,
                color = a11y.adaptiveTextSecondary,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun AlertaCuidadorCard(
    alerta: AlertaCuidadorDto,
    onAtender: () -> Unit
) {
    val esCritica = alerta.esCritico || alerta.tipoAlerta == "critica_automatica"
    val bgColor = if (esCritica) Color(0xFFFFEBEE) else Color(0xFFFFF8E1)
    val borderColor = if (esCritica) Color(0xFFE53935) else Color(0xFFFFB300)
    val accentColor = if (esCritica) Color(0xFFB71C1C) else Color(0xFFE65100)

    Surface(
        shape = RoundedCornerShape(20.dp),
        color = bgColor,
        border = BorderStroke(1.5.dp, borderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    shape = RoundedCornerShape(50),
                    color = accentColor
                ) {
                    Text(
                        text = if (esCritica) {
                            "🚨 ALERTA CRÍTICA AUTOMÁTICA"
                        } else {
                            "⚠️ AVISO PREVENTIVO (${alerta.accion.uppercase()})"
                        },
                        fontSize = 10.5.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color.White,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                    )
                }

                Text(
                    text = "${alerta.nombrePaciente} (${alerta.edadPaciente} años)",
                    fontSize = 11.5.sp,
                    fontWeight = FontWeight.Bold,
                    color = accentColor
                )
            }

            Spacer(Modifier.height(10.dp))

            Text(
                text = "${alerta.medicamentoNombre} • ${alerta.dosis}",
                fontSize = 16.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFF1E293B)
            )

            Spacer(Modifier.height(4.dp))

            Text(
                text = alerta.mensaje,
                fontSize = 13.sp,
                color = Color(0xFF334155),
                lineHeight = 18.sp
            )

            Spacer(Modifier.height(12.dp))

            Button(
                onClick = onAtender,
                shape = RoundedCornerShape(14.dp),
                colors = ButtonDefaults.buttonColors(containerColor = accentColor),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 44.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Check,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(17.dp)
                )
                Spacer(Modifier.width(6.dp))
                Text(
                    text = "Confirmar Enterado / Marcar Atendida",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }
        }
    }
}

@Composable
private fun TomaSupervisadaRowCard(item: TomaSupervisadaItemDto) {
    val a11y = LocalAccessibilitySettings.current
    val (badgeBg, badgeText, badgeLabel) = when (item.estado) {
        "tomado" -> Triple(Color(0xFFDCFCE7), Color(0xFF15803D), "✓ Tomado")
        "omitido" -> Triple(Color(0xFFFFEBEE), Color(0xFFB71C1C), "✕ Omitido")
        "pospuesto" -> Triple(Color(0xFFFFF8E1), Color(0xFFE65100), "⏰ Pospuesto (${item.vecesPospuesto})")
        else -> Triple(TealBadgeBg, TealDark, "Pendiente")
    }

    Surface(
        shape = RoundedCornerShape(16.dp),
        color = a11y.adaptiveCardSurface,
        border = BorderStroke(1.dp, a11y.adaptiveBorder),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = item.nombreMedicamento,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold,
                        color = a11y.adaptiveTextPrimary
                    )
                    if (item.esCritico) {
                        Spacer(Modifier.width(6.dp))
                        Surface(
                            shape = RoundedCornerShape(6.dp),
                            color = Color(0xFFFFEBEE)
                        ) {
                            Text(
                                text = "CRÍTICO",
                                fontSize = 9.5.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = Color(0xFFB71C1C),
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                }
                Spacer(Modifier.height(2.dp))
                Text(
                    text = "${item.dosis} ${if (item.vecesPospuesto > 0) "• Pospuesto ${item.vecesPospuesto}x" else ""}",
                    fontSize = 12.5.sp,
                    color = a11y.adaptiveTextSecondary
                )
            }

            Surface(
                shape = RoundedCornerShape(50),
                color = badgeBg
            ) {
                Text(
                    text = badgeLabel,
                    fontSize = 11.5.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = badgeText,
                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp)
                )
            }
        }
    }
}

/**
 * Modal de Castigo / Supervisión para Adultos Mayores cuando omiten o posponen un medicamento:
 * - Si `isCriticalAutoSent == false` (Medicamento Normal): Muestra una alerta advirtiendo al adulto mayor
 *   que se notificará a su cuidador por omitir o posponer la toma.
 * - Si `isCriticalAutoSent == true` (Medicamento Crítico): Informa que la alerta crítica YA SE ENVIÓ
 *   AUTOMÁTICAMENTE al cuidador.
 */
@Composable
fun SeniorCaregiverPenaltyModal(
    penalty: SeniorPenaltyModalState,
    onDismiss: () -> Unit,
    onCorregirYTomarAhora: () -> Unit,
    onAbrirVistaCuidador: () -> Unit
) {
    val context = LocalContext.current
    val isCritico = penalty.isCriticalAutoSent
    val headerBg = if (isCritico) Color(0xFFB71C1C) else Color(0xFFE65100)
    val badgeBg = if (isCritico) Color(0xFFFFEBEE) else Color(0xFFFFF3E0)

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            shape = RoundedCornerShape(28.dp),
            color = CardBackground,
            shadowElevation = 14.dp,
            modifier = Modifier
                .fillMaxWidth(0.92f)
                .padding(16.dp)
        ) {
            Column(
                modifier = Modifier
                    .verticalScroll(rememberScrollState())
                    .padding(22.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Surface(
                    shape = CircleShape,
                    color = badgeBg,
                    border = BorderStroke(2.dp, headerBg),
                    modifier = Modifier.size(64.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = if (isCritico) Icons.Outlined.NotificationImportant else Icons.Outlined.Warning,
                            contentDescription = null,
                            tint = headerBg,
                            modifier = Modifier.size(34.dp)
                        )
                    }
                }

                Spacer(Modifier.height(14.dp))

                Surface(
                    shape = RoundedCornerShape(50),
                    color = badgeBg
                ) {
                    Text(
                        text = if (isCritico) {
                            "🚨 ALERTA CRÍTICA ENVIADA AUTOMÁTICAMENTE"
                        } else {
                            "⚠️ PROTOCOLO DE SUPERVISIÓN ADULTO MAYOR"
                        },
                        fontSize = 11.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = headerBg,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp)
                    )
                }

                Spacer(Modifier.height(10.dp))

                Text(
                    text = if (isCritico) {
                        "Se ha enviado una alerta automática a tu cuidador"
                    } else {
                        "Se notificará a tu cuidador por ${if (penalty.accionIntentada == "posponer") "posponer" else "omitir"} tu dosis"
                    },
                    fontSize = 20.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary,
                    textAlign = TextAlign.Center
                )

                Spacer(Modifier.height(8.dp))

                Text(
                    text = penalty.mensajeAlerta,
                    fontSize = 14.sp,
                    color = TextSecondary,
                    textAlign = TextAlign.Center,
                    lineHeight = 20.sp
                )

                Spacer(Modifier.height(14.dp))

                Surface(
                    shape = RoundedCornerShape(16.dp),
                    color = badgeBg,
                    border = BorderStroke(1.dp, headerBg.copy(alpha = 0.35f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Text(
                            text = "Medicamento: ${penalty.medicamentoNombre} (${penalty.dosisDetalle})",
                            fontSize = 13.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "Cuidador responsable: ${penalty.cuidadorNombre}",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = headerBg
                        )
                    }
                }

                Spacer(Modifier.height(18.dp))

                // Opción 1: Corregir y tomar el medicamento ahora mismo
                if (penalty.idRecordatorio > 0) {
                    Button(
                        onClick = onCorregirYTomarAhora,
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 52.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Check,
                            contentDescription = null,
                            tint = Color.White
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(
                            text = "Tomar ${penalty.medicamentoNombre} Ahora",
                            fontSize = 14.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }
                    Spacer(Modifier.height(10.dp))
                }

                // Opción 2: Ver en Vista del Cuidador o Enviar SMS directo
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedButton(
                        onClick = {
                            onDismiss()
                            onAbrirVistaCuidador()
                        },
                        shape = RoundedCornerShape(14.dp),
                        border = BorderStroke(1.2.dp, headerBg),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 48.dp)
                    ) {
                        Text(
                            text = "Ver Vista Cuidador",
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = headerBg
                        )
                    }

                    if (penalty.cuidadorTelefono.isNotBlank()) {
                        OutlinedButton(
                            onClick = {
                                val smsIntent = Intent(Intent.ACTION_SENDTO).apply {
                                    data = Uri.parse("smsto:${penalty.cuidadorTelefono}")
                                    putExtra("sms_body", penalty.mensajeAlerta)
                                }
                                runCatching { context.startActivity(smsIntent) }
                            },
                            shape = RoundedCornerShape(14.dp),
                            border = BorderStroke(1.2.dp, InputBorderColor),
                            modifier = Modifier
                                .weight(1f)
                                .heightIn(min = 48.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Sms,
                                contentDescription = null,
                                tint = TextPrimary,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(Modifier.width(4.dp))
                            Text(
                                text = "SMS Cuidador",
                                fontSize = 12.5.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        }
                    }
                }

                Spacer(Modifier.height(8.dp))

                TextButton(
                    onClick = onDismiss,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = "Cerrar aviso",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextSecondary
                    )
                }
            }
        }
    }
}

/**
 * Modal de Alarma Nativa de Medicamento:
 * Salta automáticamente en pantalla cuando un medicamento ya se tiene que tomar,
 * permitiendo confirmar la toma o posponerla en 1 toque.
 */
@Composable
fun NativeMedicationAlarmModal(
    alarmEvent: ActiveNativeAlarmEvent,
    esAdultoMayor: Boolean,
    onTomarAhora: () -> Unit,
    onPosponer30Min: () -> Unit,
    onDismiss: () -> Unit
) {
    val transition = rememberInfiniteTransition(label = "native_alarm_pulse")
    val pulseScale by transition.animateFloat(
        initialValue = 0.94f,
        targetValue = 1.12f,
        animationSpec = infiniteRepeatable(
            animation = tween(550, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "alarm_ring_scale"
    )

    val accentColor = if (alarmEvent.esCritico) Color(0xFFB71C1C) else TealPrimary

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            shape = RoundedCornerShape(28.dp),
            color = CardBackground,
            border = BorderStroke(2.dp, accentColor),
            shadowElevation = 16.dp,
            modifier = Modifier
                .fillMaxWidth(0.92f)
                .padding(16.dp)
        ) {
            Column(
                modifier = Modifier.padding(22.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Surface(
                    shape = CircleShape,
                    color = accentColor.copy(alpha = 0.14f),
                    modifier = Modifier
                        .size(72.dp)
                        .graphicsLayer {
                            scaleX = pulseScale
                            scaleY = pulseScale
                        }
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Outlined.AccessAlarm,
                            contentDescription = "Alarma activa",
                            tint = accentColor,
                            modifier = Modifier.size(38.dp)
                        )
                    }
                }

                Spacer(Modifier.height(12.dp))

                Surface(
                    shape = RoundedCornerShape(50),
                    color = if (alarmEvent.esCritico) Color(0xFFFFEBEE) else TealBadgeBg
                ) {
                    Text(
                        text = if (alarmEvent.esCritico) {
                            "🔔 ALARMA NATIVA • DOSIS CRÍTICA OBLIGATORIA"
                        } else {
                            "🔔 ALARMA NATIVA • HORA DE TU MEDICAMENTO"
                        },
                        fontSize = 11.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = accentColor,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp)
                    )
                }

                Spacer(Modifier.height(10.dp))

                Text(
                    text = alarmEvent.nombreMedicamento,
                    fontSize = 23.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary,
                    textAlign = TextAlign.Center
                )

                Spacer(Modifier.height(4.dp))

                Text(
                    text = "${alarmEvent.dosisDetalle} • ${alarmEvent.horaFormateada}",
                    fontSize = 14.5.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = TextSecondary,
                    textAlign = TextAlign.Center
                )

                if (esAdultoMayor) {
                    Spacer(Modifier.height(10.dp))
                    Surface(
                        shape = RoundedCornerShape(14.dp),
                        color = if (alarmEvent.esCritico) Color(0xFFFFEBEE) else Color(0xFFFFF8E1),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = if (alarmEvent.esCritico) {
                                "Supervisión Adulto Mayor: Este medicamento es CRÍTICO. Si no se toma a tiempo, se enviará automáticamente una alerta a tu cuidador."
                            } else {
                                "Supervisión Adulto Mayor: Si pospones u omites esta toma, se notificará a tu cuidador."
                            },
                            fontSize = 12.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = if (alarmEvent.esCritico) Color(0xFFB71C1C) else Color(0xFFE65100),
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(10.dp)
                        )
                    }
                }

                Spacer(Modifier.height(18.dp))

                Button(
                    onClick = onTomarAhora,
                    shape = RoundedCornerShape(18.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 54.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Check,
                        contentDescription = null,
                        tint = Color.White
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = "Tomar Medicamento Ahora",
                        fontSize = 15.5.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color.White
                    )
                }

                Spacer(Modifier.height(8.dp))

                if (!alarmEvent.esCritico && alarmEvent.permitePosponer) {
                    OutlinedButton(
                        onClick = onPosponer30Min,
                        shape = RoundedCornerShape(16.dp),
                        border = BorderStroke(1.2.dp, InputBorderColor),
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 48.dp)
                    ) {
                        Text(
                            text = if (esAdultoMayor) "Posponer 30 min (Notifica al Cuidador)" else "Posponer 30 min",
                            fontSize = 13.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = TealDark
                        )
                    }
                }

                TextButton(
                    onClick = onDismiss,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = "Silenciar alarma por ahora",
                        fontSize = 13.sp,
                        color = TextSecondary
                    )
                }
            }
        }
    }
}
