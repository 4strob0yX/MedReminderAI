package com.medreminder.ai.ui.home

import android.content.Intent
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.ui.unit.IntOffset
import android.net.Uri
import android.widget.Toast
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Path
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.animation.core.EaseInOutSine
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.ui.graphics.graphicsLayer
import com.medreminder.ai.notifications.NotificationHelper
import com.medreminder.ai.notifications.ReminderAlarmScheduler
import com.medreminder.ai.notifications.TtsHelper
import com.medreminder.ai.ui.components.DraggableMediCompanion
import com.medreminder.ai.ui.components.MediAssistantDialog
import com.medreminder.ai.ui.components.MediFloatingCompanion
import com.medreminder.ai.ui.components.MediMascotView
import com.medreminder.ai.ui.components.MediMood
import com.medreminder.ai.ui.theme.AccessibilityPreferences
import com.medreminder.ai.ui.theme.FontScaleMode
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
import com.medreminder.ai.ui.theme.ThemeMode
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.VolumeUp
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AccessAlarm
import androidx.compose.material.icons.outlined.BarChart
import androidx.compose.material.icons.outlined.CalendarToday
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Contrast
import androidx.compose.material.icons.outlined.EmojiEvents
import androidx.compose.material.icons.outlined.FormatSize
import androidx.compose.material.icons.outlined.HealthAndSafety
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.LocalFireDepartment
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.MedicalInformation
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.NotificationImportant
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material.icons.outlined.Replay
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Sms
import androidx.compose.material.icons.outlined.Vaccines
import androidx.compose.material.icons.outlined.Warning
import androidx.compose.material.icons.outlined.WaterDrop
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.ui.components.MedBrandLogo
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.AppBackground
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.OmitBrownText
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealBadgeText
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import com.medreminder.ai.ui.theme.TealSoftBg
import com.medreminder.ai.ui.theme.TextPrimary
import com.medreminder.ai.ui.theme.TextSecondary
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.util.Locale

data class PillColorPalette(
    val key: String,
    val label: String,
    val containerBg: Color,
    val iconTint: Color,
    val dotColor: Color
)

val PILL_COLOR_OPTIONS = listOf(
    PillColorPalette("blanco", "Blanco", Color(0xFFF1F5F9), Color(0xFF334155), Color(0xFFCBD5E1)),
    PillColorPalette("azul", "Azul", Color(0xFFE0F2FE), Color(0xFF0369A1), Color(0xFF0284C7)),
    PillColorPalette("amarillo", "Amarillo", Color(0xFFFEF9C3), Color(0xFFB45309), Color(0xFFFACC15)),
    PillColorPalette("rojo", "Rojo / Coral", Color(0xFFFFE4E6), Color(0xFFBE123C), Color(0xFFF43F5E)),
    PillColorPalette("verde", "Verde", Color(0xFFDCFCE7), Color(0xFF15803D), Color(0xFF22C55E)),
    PillColorPalette("bicolor", "Bicolor", Color(0xFFF3E8FF), Color(0xFF6D28D9), Color(0xFF9333EA))
)

fun resolvePillPalette(colorKey: String?): PillColorPalette {
    val clean = colorKey?.trim()?.lowercase() ?: "blanco"
    return PILL_COLOR_OPTIONS.firstOrNull { clean.contains(it.key) } ?: PILL_COLOR_OPTIONS.first()
}

fun resolveFormaIcon(forma: FormaFarmaceutica): ImageVector = when (forma) {
    FormaFarmaceutica.COMPRIMIDOS -> Icons.Outlined.Medication
    FormaFarmaceutica.GOTAS -> Icons.Outlined.WaterDrop
    FormaFarmaceutica.INYECTABLE -> Icons.Outlined.Vaccines
}

/**
 * Contenedor principal post-autenticación que coordina:
 * - Pantalla Hoy / Plan Diario con Accesibilidad, Rachas TikTok, Honor y Modo Castigo
 * - Modal de Confirmación de Toma con Verificación Visual y Deslizar/Mantener 2s
 * - Pantalla Mi Botiquín
 * - Pantalla Alergias y Apoyo
 * - Pantalla Progreso (Gráficas y Mapa de Calor)
 * - Pantalla Registrar Medicamento
 */
@Composable
fun HomeRoute(
    viewModel: HomeViewModel,
    onLogout: () -> Unit
) {
    val state by viewModel.state.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }
    var showLogoutDialog by remember { mutableStateOf(false) }
    var showMediDialog by remember { mutableStateOf(false) }

    val context = LocalContext.current
    val accessSettings = LocalAccessibilitySettings.current

    val isTtsSpeaking by TtsHelper.isSpeaking.collectAsState()
    val currentTtsKey by TtsHelper.currentKey.collectAsState()
    val currentTtsText by TtsHelper.currentText.collectAsState()
    val activeAlarmEvent by NotificationHelper.activeAlarmEvent.collectAsState()

    val speakText: (String) -> Unit = { texto ->
        if (isTtsSpeaking) {
            TtsHelper.stop()
        } else {
            TtsHelper.speak(context, texto, key = "general")
        }
    }

    // Programar alarmas nativas exactas y publicar recordatorio activo en la barra de notificaciones
    LaunchedEffect(state.tomasHoy) {
        NotificationHelper.ensureChannelsCreated(context)
        val pendientes = state.tomasHoy.filter { it.estado == "pendiente" }
        pendientes.forEach { toma ->
            ReminderAlarmScheduler.scheduleFromHoraFormateada(
                context = context,
                idRecordatorio = toma.idRecordatorio,
                horaFormateada = toma.horaFormateada,
                nombreMedicamento = toma.nombreMedicamento,
                dosisDetalle = toma.dosisDetalle.substringBefore("•").trim(),
                esCritico = toma.esCritico,
                permitePosponer = toma.permitePosponer
            )
        }
        val proxima = pendientes.firstOrNull()
        if (proxima != null) {
            NotificationHelper.showUpcomingSummaryNotification(
                context = context,
                pendientesCount = pendientes.size,
                proximaMedNombre = proxima.nombreMedicamento,
                proximaMedHora = proxima.horaFormateada,
                proximaMedDosis = proxima.dosisDetalle.substringBefore("•").trim(),
                esCritico = proxima.esCritico
            )
        }
    }

    // Disparar notificación nativa al cuidador cuando salta el modal de castigo/supervisión geriátrica
    LaunchedEffect(state.seniorPenaltyModal) {
        state.seniorPenaltyModal?.let { penalty ->
            NotificationHelper.showCaregiverAlertNotification(
                context = context,
                titulo = if (penalty.isCriticalAutoSent) {
                    "🚨 ALERTA CRÍTICA AUTOMÁTICA AL CUIDADOR"
                } else {
                    "⚠️ Aviso al Cuidador (${penalty.cuidadorNombre})"
                },
                mensaje = penalty.mensajeAlerta,
                esCritico = penalty.isCriticalAutoSent
            )
        }
    }

    BackHandler(enabled = state.showVistaCuidador) {
        viewModel.onCloseVistaCuidador()
    }

    BackHandler(enabled = !state.showVistaCuidador && state.showEscaneoReceta) {
        viewModel.onCloseEscaneoReceta()
    }

    BackHandler(enabled = !state.showVistaCuidador && !state.showEscaneoReceta && state.showNuevoMedicamento) {
        viewModel.onCloseNuevoMedicamento()
    }

    BackHandler(enabled = !state.showVistaCuidador && !state.showEscaneoReceta && !state.showNuevoMedicamento && state.selectedTab != HomeTab.HOY) {
        viewModel.onSelectTab(HomeTab.HOY)
    }

    LaunchedEffect(state.snackbarMessage) {
        state.snackbarMessage?.let { msg ->
            snackbarHostState.showSnackbar(msg)
            viewModel.onSnackbarShown()
        }
    }

    if (state.showVistaCuidador) {
        CuidadorScreen(
            state = state,
            onBack = viewModel::onCloseVistaCuidador,
            onRefresh = { viewModel.cargarPanelCuidador(silencioso = false) },
            onAtenderAlerta = viewModel::onAtenderAlertaCuidador,
            onSimularAlertaCritica = viewModel::onSimularAlertaCriticaCuidador,
            onCambiarRangoEdadDemo = viewModel::onCambiarRangoEdadDemo
        )
        return
    }

    if (state.showEscaneoReceta) {
        ConfirmarRecetaScreen(
            state = state,
            onBack = viewModel::onCloseEscaneoReceta,
            onAnalizarReceta = viewModel::onAnalizarRecetaIa,
            onActualizarItem = viewModel::onActualizarItemReceta,
            onConfirmarGuardar = viewModel::onConfirmarYGuardarReceta
        )
        return
    }

    if (state.showNuevoMedicamento) {
        NuevoMedicamentoScreen(
            form = state.form,
            snackbarHostState = snackbarHostState,
            onBack = viewModel::onCloseNuevoMedicamento,
            onFormaChange = viewModel::onFormaChange,
            onColorPastillaChange = viewModel::onColorPastillaChange,
            onNombreChange = viewModel::onNombreMedChange,
            onSelectCatalogoSugerencia = viewModel::onSelectCatalogoSugerencia,
            onDosisChange = viewModel::onDosisMedChange,
            onFrecuenciaTextoChange = viewModel::onFrecuenciaTextoChange,
            onSelectFrecuenciaChip = viewModel::onSelectFrecuenciaChip,
            onHoraPrimeraTomaChange = viewModel::onHoraPrimeraTomaChange,
            onDuracionChange = viewModel::onDuracionChange,
            onInstruccionesTomaChange = viewModel::onInstruccionesTomaChange,
            onStockTextoChange = viewModel::onStockTextoChange,
            onIncrementStock = viewModel::onIncrementStock,
            onTogglePermitePosponer = viewModel::onTogglePermitePosponer,
            onToggleEsCritico = viewModel::onToggleEsCritico,
            onContraindicacionesChange = viewModel::onContraindicacionesChange,
            onSolicitarSugerenciasIa = viewModel::onSolicitarSugerenciasIa,
            onEscanearRecetaCompletaIa = viewModel::onOpenEscaneoReceta,
            onDismissRiesgoModal = viewModel::onDismissConfirmacionRiesgoModal,
            onGuardar = { viewModel.onGuardarMedicamento(forzarConRiesgo = false) },
            onConfirmarGuardarConRiesgo = { viewModel.onGuardarMedicamento(forzarConRiesgo = true) }
        )
        return
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Scaffold(
            containerColor = accessSettings.adaptiveBackground,
            snackbarHost = { SnackbarHost(snackbarHostState) },
            topBar = {
                ModernHeroHeader(
                    selectedTab = state.selectedTab,
                    subtitle = when (state.selectedTab) {
                        HomeTab.HOY -> "Plan de Hoy"
                        HomeTab.MI_BOTIQUIN -> "Mi Botiquín"
                        HomeTab.SALUD_APOYO -> "Alergias y Apoyo"
                        HomeTab.ANALISIS_DFS -> "Mi Progreso"
                    },
                    userName = state.nombreUsuario.ifBlank { "Paciente" },
                    dateHeader = state.fechaEncabezado.ifBlank { "Hoy" },
                    completadas = state.tomasCompletadasCount,
                    totalTomas = state.tomasHoy.size,
                    onProfileClick = { showLogoutDialog = true },
                    onToggleTextoGrande = {
                        val current = accessSettings.fontScaleMode
                        val next = when (current) {
                            FontScaleMode.NORMAL -> FontScaleMode.GRANDE
                            FontScaleMode.GRANDE -> FontScaleMode.EXTRA_GRANDE
                            FontScaleMode.EXTRA_GRANDE -> FontScaleMode.NORMAL
                        }
                        accessSettings.onFontScaleModeChange(next)
                        viewModel.onToggleTextoGrande()
                    },
                    onToggleAltoContraste = {
                        val current = accessSettings.themeMode
                        val next = when (current) {
                            ThemeMode.CALIDO_AMIGABLE -> ThemeMode.ALTO_CONTRASTE_DIA
                            ThemeMode.ALTO_CONTRASTE_DIA -> ThemeMode.ALTO_CONTRASTE_NOCHE
                            ThemeMode.ALTO_CONTRASTE_NOCHE -> ThemeMode.CALIDO_AMIGABLE
                        }
                        accessSettings.onThemeModeChange(next)
                        viewModel.onToggleAltoContraste()
                    },
                    isSpeakingPlan = isTtsSpeaking && currentTtsKey == "plan",
                    onSpeakPlan = {
                        if (isTtsSpeaking && currentTtsKey == "plan") {
                            TtsHelper.stop()
                        } else {
                            val totalTomas = state.tomasHoy.size
                            val completadas = state.tomasCompletadasCount
                            val resumen = if (state.tomasHoy.isEmpty()) {
                                "Hola ${state.nombreUsuario}. Hoy no tienes tomas pendientes programadas."
                            } else {
                                val pendientes = state.tomasHoy.filter { it.estado == "pendiente" }
                                "Hola ${state.nombreUsuario}. Hoy tienes $totalTomas tomas programadas y has completado $completadas. " +
                                    if (pendientes.isNotEmpty()) {
                                        "Próxima toma: ${pendientes.first().nombreMedicamento} a las ${pendientes.first().horaFormateada}."
                                    } else {
                                        "Completaste todas tus tomas del día."
                                    }
                            }
                            TtsHelper.speak(context, resumen, key = "plan")
                        }
                    }
                )
            },
            bottomBar = {
                // El footer se repliega suavemente cuando Medi abre su chat para evitar cualquier solapamiento
                AnimatedVisibility(
                    visible = !showMediDialog,
                    enter = fadeIn(tween(180)) + expandVertically(expandFrom = Alignment.Bottom),
                    exit = fadeOut(tween(140)) + shrinkVertically(shrinkTowards = Alignment.Bottom)
                ) {
                    ClinicalBottomBar(
                        selectedTab = state.selectedTab,
                        onSelectTab = viewModel::onSelectTab
                    )
                }
            }
        ) { innerPadding ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
            ) {
                if (!accessSettings.isHighContrast) {
                    AuroraBackdrop(modifier = Modifier.fillMaxSize())
                }
                when (state.selectedTab) {
                    HomeTab.HOY -> HoyScreenContent(
                        state = state,
                        onRegistrarTomaClick = viewModel::onOpenConfirmacionToma,
                        onRevertirTomaClick = viewModel::onRevertirToma,
                        onNuevoMedClick = viewModel::onOpenNuevoMedicamento,
                        onOpenVistaCuidador = viewModel::onOpenVistaCuidador,
                        onCambiarRangoEdadDemo = viewModel::onCambiarRangoEdadDemo,
                        onToggleTextoGrande = {
                            val current = accessSettings.fontScaleMode
                            val next = when (current) {
                                FontScaleMode.NORMAL -> FontScaleMode.GRANDE
                                FontScaleMode.GRANDE -> FontScaleMode.EXTRA_GRANDE
                                FontScaleMode.EXTRA_GRANDE -> FontScaleMode.NORMAL
                            }
                            accessSettings.onFontScaleModeChange(next)
                            viewModel.onToggleTextoGrande()
                        },
                        onToggleAltoContraste = {
                            val current = accessSettings.themeMode
                            val next = when (current) {
                                ThemeMode.CALIDO_AMIGABLE -> ThemeMode.ALTO_CONTRASTE_DIA
                                ThemeMode.ALTO_CONTRASTE_DIA -> ThemeMode.ALTO_CONTRASTE_NOCHE
                                ThemeMode.ALTO_CONTRASTE_NOCHE -> ThemeMode.CALIDO_AMIGABLE
                            }
                            accessSettings.onThemeModeChange(next)
                            viewModel.onToggleAltoContraste()
                        },
                        onSpeakText = speakText,
                        isTtsSpeaking = isTtsSpeaking,
                        currentTtsKey = currentTtsKey
                    )

                    HomeTab.MI_BOTIQUIN -> BotiquinScreenContent(
                        state = state,
                        onAddMedicamentoClick = viewModel::onOpenNuevoMedicamento,
                        onEscanearRecetaClick = viewModel::onOpenEscaneoReceta,
                        onRecargarStock = viewModel::onRecargarStock,
                        onEliminarMedicamento = viewModel::onEliminarMedicamento
                    )

                    HomeTab.SALUD_APOYO -> SaludApoyoScreenContent(
                        state = state,
                        onAgregarAlergia = viewModel::onAgregarAlergia,
                        onEliminarAlergia = viewModel::onEliminarAlergia,
                        onGuardarContacto = viewModel::onGuardarContacto,
                        onEliminarContacto = viewModel::onEliminarContacto,
                        onOpenVistaCuidador = viewModel::onOpenVistaCuidador
                    )

                    HomeTab.ANALISIS_DFS -> AnalisisDfsScreenContent(
                        state = state
                    )
                }
            }
        }

        // Barra Flotante de Audio Reader (Accesibilidad Activa en Vivo)
        AnimatedVisibility(
            visible = isTtsSpeaking && !showMediDialog,
            enter = fadeIn() + expandVertically(expandFrom = Alignment.Bottom),
            exit = fadeOut() + shrinkVertically(shrinkTowards = Alignment.Bottom),
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(horizontal = 20.dp, vertical = 76.dp)
        ) {
            Surface(
                shape = RoundedCornerShape(50),
                color = accessSettings.adaptiveCardSurface,
                shadowElevation = 8.dp,
                border = BorderStroke(1.2.dp, TealPrimary.copy(alpha = 0.5f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    MiniVoiceWaveform(
                        isSpeaking = true,
                        color = TealPrimary,
                        modifier = Modifier.size(18.dp)
                    )

                    Text(
                        text = currentTtsText ?: "Reproduciendo voz...",
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.Medium,
                        color = accessSettings.adaptiveTextPrimary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f)
                    )

                    Surface(
                        shape = CircleShape,
                        color = Color(0xFFEF4444).copy(alpha = 0.12f),
                        modifier = Modifier
                            .size(28.dp)
                            .clip(CircleShape)
                            .bounceClick()
                            .clickable { TtsHelper.stop() }
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Default.Close,
                                contentDescription = "Detener lectura",
                                tint = Color(0xFFEF4444),
                                modifier = Modifier.size(15.dp)
                            )
                        }
                    }
                }
            }
        }

        // Omnipresent Friendly Companion Mascot "Medi" Draggable Living Entity con chat emergente
        // Al estar en el Box raíz exterior a Scaffold, Medi y su chat flotan por encima de TODO sin ser tapados por el footer
        DraggableMediCompanion(
            onClick = { showMediDialog = true },
            modifier = Modifier.fillMaxSize(),
            safeBottomPadding = 86.dp,
            isChatOpen = showMediDialog,
            onDismissChat = { showMediDialog = false },
            reaction = state.mediReaction,
            nombreUsuario = state.nombreUsuario.ifBlank { "Paciente" },
            contextoPantalla = when (state.selectedTab) {
                HomeTab.HOY -> "Hoy"
                HomeTab.MI_BOTIQUIN -> "Botiquín"
                HomeTab.SALUD_APOYO -> "Apoyo"
                HomeTab.ANALISIS_DFS -> "Progreso"
            },
            onAskAi = viewModel::consultarMediAi
        )

        // Modal de Confirmación de Toma con Verificación Visual y Anti-Toque Falso
        state.selectedTomaForModal?.let { toma ->
            ConfirmacionTomaModal(
                toma = toma,
                esAdultoMayor = state.esAdultoMayor,
                contactosApoyo = state.contactosApoyo,
                castigoPosponerBloqueado = state.castigoPosponerBloqueado,
                isActionInFlight = state.isActionInFlight,
                onDismiss = viewModel::onDismissConfirmacionToma,
                onTomarAhora = viewModel::onTomarAhora,
                onPosponer30Min = viewModel::onPosponer30Min,
                onOmitirToma = viewModel::onOmitirToma,
                onSpeakText = { texto ->
                    if (isTtsSpeaking && currentTtsKey == "modal_confirmacion") {
                        TtsHelper.stop()
                    } else {
                        TtsHelper.speak(context, texto, key = "modal_confirmacion")
                    }
                }
            )
        }

        // Modal de Castigo / Alerta al Cuidador para Adulto Mayor (Normal vs Crítico Automático)
        state.seniorPenaltyModal?.let { penalty ->
            SeniorCaregiverPenaltyModal(
                penalty = penalty,
                onDismiss = viewModel::onDismissSeniorPenaltyModal,
                onCorregirYTomarAhora = {
                    viewModel.onTomarPorId(penalty.idRecordatorio, penalty.medicamentoNombre)
                },
                onAbrirVistaCuidador = viewModel::onOpenVistaCuidador
            )
        }

        // Modal de Alarma Nativa de Medicamento (salta automáticamente cuando llega la hora de una toma)
        activeAlarmEvent?.let { alarm ->
            NativeMedicationAlarmModal(
                alarmEvent = alarm,
                esAdultoMayor = state.esAdultoMayor,
                onTomarAhora = {
                    NotificationHelper.dismissActiveAlarmEvent()
                    NotificationHelper.cancelNotification(context, alarm.idRecordatorio)
                    viewModel.onTomarPorId(alarm.idRecordatorio, alarm.nombreMedicamento)
                },
                onPosponer30Min = {
                    NotificationHelper.dismissActiveAlarmEvent()
                    ReminderAlarmScheduler.scheduleSnooze30Min(
                        context = context,
                        idRecordatorio = alarm.idRecordatorio,
                        nombreMedicamento = alarm.nombreMedicamento,
                        dosisDetalle = alarm.dosisDetalle,
                        horaFormateada = alarm.horaFormateada
                    )
                    val matchingToma = state.tomasHoy.firstOrNull { it.idRecordatorio == alarm.idRecordatorio }
                    if (matchingToma != null) {
                        viewModel.onOpenConfirmacionToma(matchingToma)
                        viewModel.onPosponer30Min()
                    }
                },
                onDismiss = {
                    NotificationHelper.dismissActiveAlarmEvent()
                }
            )
        }

        // Diálogo de confirmación antes de cerrar sesión
        if (showLogoutDialog) {
            LogoutConfirmDialog(
                nombreUsuario = state.nombreUsuario,
                onDismiss = { showLogoutDialog = false },
                onConfirmLogout = {
                    showLogoutDialog = false
                    onLogout()
                }
            )
        }
    }
}

/** Fondo "aurora": resplandores atmosféricos suaves y de ultra-alto rendimiento (sin carga continua en GPU). */
@Composable
fun AuroraBackdrop(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height
        val r = w * 0.85f
        fun glow(color: Color, cx: Float, cy: Float, alpha: Float) = drawCircle(
            brush = Brush.radialGradient(
                listOf(color.copy(alpha = alpha), Color.Transparent),
                center = Offset(cx, cy),
                radius = r
            ),
            radius = r,
            center = Offset(cx, cy)
        )
        glow(Color(0xFF2DD4BF), w * 0.22f, h * 0.08f, 0.16f)
        glow(Color(0xFF10B981), w * 0.82f, h * 0.58f, 0.11f)
        glow(Color(0xFF7C4DFF), w * 0.28f, h * 0.92f, 0.08f)
    }
}

@Composable
fun Modifier.bounceClick(scaleDown: Float = 0.94f): Modifier {
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (isPressed) scaleDown else 1f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessMedium
        ),
        label = "bounce_scale"
    )
    return this.graphicsLayer {
        scaleX = scale
        scaleY = scale
    }
}

/**
 * Indicador visual vivo de onda de voz / ecualizador para feedback sonoro inmediato
 */
@Composable
fun MiniVoiceWaveform(
    isSpeaking: Boolean,
    color: Color,
    modifier: Modifier = Modifier
) {
    val transition = rememberInfiniteTransition(label = "waveform_anim")
    val h1 by transition.animateFloat(
        initialValue = 4f,
        targetValue = 14f,
        animationSpec = infiniteRepeatable(
            animation = tween(380, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "w_h1"
    )
    val h2 by transition.animateFloat(
        initialValue = 13f,
        targetValue = 5f,
        animationSpec = infiniteRepeatable(
            animation = tween(310, delayMillis = 80, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "w_h2"
    )
    val h3 by transition.animateFloat(
        initialValue = 6f,
        targetValue = 16f,
        animationSpec = infiniteRepeatable(
            animation = tween(440, delayMillis = 160, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "w_h3"
    )

    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(2.5.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        listOf(h1, h2, h3).forEach { h ->
            Box(
                modifier = Modifier
                    .width(3.dp)
                    .height(if (isSpeaking) h.dp else 4.dp)
                    .clip(RoundedCornerShape(50))
                    .background(color)
            )
        }
    }
}

/**
 * Header Heroico Moderno 2026:
 * Integra logotipo interactivo, saludo dinámico, cápsula flotante de accesibilidad
 * y avatar con halo activo de adherencia diaria.
 */
@Composable
fun ModernHeroHeader(
    selectedTab: HomeTab,
    subtitle: String,
    userName: String,
    dateHeader: String,
    completadas: Int,
    totalTomas: Int,
    onProfileClick: () -> Unit,
    onToggleTextoGrande: () -> Unit,
    onToggleAltoContraste: () -> Unit,
    isSpeakingPlan: Boolean = false,
    onSpeakPlan: () -> Unit
) {
    val a11y = LocalAccessibilitySettings.current
    val infiniteTransition = rememberInfiniteTransition(label = "header_aura_anim")
    val auraAlpha by infiniteTransition.animateFloat(
        initialValue = 0.05f,
        targetValue = 0.15f,
        animationSpec = infiniteRepeatable(
            animation = tween(3200, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "aura_pulse"
    )

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                Brush.verticalGradient(
                    listOf(
                        TealPrimary.copy(alpha = auraAlpha),
                        a11y.adaptiveBackground
                    )
                )
            )
            .statusBarsPadding()
            .padding(horizontal = 18.dp, vertical = 3.dp)
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            // Fila superior: Logo y Cápsula de Fecha a la izquierda, Accesibilidad y Perfil a la derecha
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Box(modifier = Modifier.bounceClick()) {
                        MedBrandLogo(size = 38.dp, cornerRadius = 13.dp)
                    }
                    Spacer(Modifier.width(10.dp))
                    Surface(
                        shape = RoundedCornerShape(50),
                        color = a11y.adaptiveSoftSurface,
                        border = BorderStroke(0.8.dp, a11y.adaptiveBorder)
                    ) {
                        Text(
                            text = if (selectedTab == HomeTab.HOY) dateHeader.ifBlank { "Hoy" } else subtitle,
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 0.5.sp,
                            color = a11y.adaptivePrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 3.dp)
                        )
                    }
                }

                // Lado Derecho: Cápsula Unificada de Accesibilidad + Avatar con Halo de Adherencia
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    // Cápsula Flotante de Accesibilidad (Pill Unificado 2026)
                    Surface(
                        shape = RoundedCornerShape(50),
                        color = a11y.adaptiveCardSurface,
                        border = BorderStroke(1.dp, a11y.adaptiveBorder),
                        shadowElevation = 2.dp
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                        ) {
                            // Tamaño de fuente (TT)
                            Box(
                                modifier = Modifier
                                    .size(34.dp)
                                    .clip(CircleShape)
                                    .bounceClick()
                                    .clickable { onToggleTextoGrande() },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.FormatSize,
                                    contentDescription = "Tamaño de fuente",
                                    tint = if (a11y.fontScaleMode != FontScaleMode.NORMAL) TealPrimary else a11y.adaptiveTextSecondary,
                                    modifier = Modifier.size(17.dp)
                                )
                            }

                            Box(
                                modifier = Modifier
                                    .width(1.dp)
                                    .height(16.dp)
                                    .background(a11y.adaptiveBorder)
                            )

                            // Alto contraste
                            Box(
                                modifier = Modifier
                                    .size(34.dp)
                                    .clip(CircleShape)
                                    .bounceClick()
                                    .clickable { onToggleAltoContraste() },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.Contrast,
                                    contentDescription = "Alto contraste",
                                    tint = if (a11y.isHighContrast) TealPrimary else a11y.adaptiveTextSecondary,
                                    modifier = Modifier.size(17.dp)
                                )
                            }

                            Box(
                                modifier = Modifier
                                    .width(1.dp)
                                    .height(16.dp)
                                    .background(a11y.adaptiveBorder)
                            )

                            // Escuchar Plan (TTS)
                            Box(
                                modifier = Modifier
                                    .size(34.dp)
                                    .clip(CircleShape)
                                    .background(if (isSpeakingPlan) TealPrimary.copy(alpha = 0.18f) else Color.Transparent)
                                    .bounceClick()
                                    .clickable { onSpeakPlan() },
                                contentAlignment = Alignment.Center
                            ) {
                                if (isSpeakingPlan) {
                                    MiniVoiceWaveform(
                                        isSpeaking = true,
                                        color = TealPrimary,
                                        modifier = Modifier.size(16.dp)
                                    )
                                } else {
                                    Icon(
                                        imageVector = Icons.AutoMirrored.Outlined.VolumeUp,
                                        contentDescription = "Escuchar plan",
                                        tint = if (isSpeakingPlan) TealPrimary else a11y.adaptiveTextSecondary,
                                        modifier = Modifier.size(17.dp)
                                    )
                                }
                            }
                        }
                    }

                    // Avatar de Perfil con Anillo de Adherencia Viva
                    Box(
                        modifier = Modifier
                            .size(42.dp)
                            .bounceClick()
                            .clickable { onProfileClick() },
                        contentAlignment = Alignment.Center
                    ) {
                        val adherenceFraction = if (totalTomas > 0) completadas.toFloat() / totalTomas else 0f
                        val animatedSweep by animateFloatAsState(
                            targetValue = 360f * adherenceFraction,
                            animationSpec = tween(900, easing = FastOutSlowInEasing),
                            label = "avatar_ring_sweep"
                        )

                        Canvas(modifier = Modifier.fillMaxSize()) {
                            val strokeWidth = 2.5.dp.toPx()
                            // Pista de fondo
                            drawCircle(
                                color = a11y.adaptiveBorder.copy(alpha = 0.5f),
                                radius = (size.width - strokeWidth) / 2f,
                                style = Stroke(strokeWidth)
                            )
                            // Arco de adherencia diaria
                            if (animatedSweep > 0f) {
                                drawArc(
                                    color = Color(0xFF10B981),
                                    startAngle = -90f,
                                    sweepAngle = animatedSweep,
                                    useCenter = false,
                                    style = Stroke(strokeWidth, cap = StrokeCap.Round)
                                )
                            }
                        }

                        Surface(
                            shape = CircleShape,
                            color = if (a11y.isDarkTheme) Color(0xFF162226) else TealSoftBg,
                            modifier = Modifier
                                .size(32.dp)
                                .clip(CircleShape)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.Person,
                                    contentDescription = "Perfil y Ajustes",
                                    tint = a11y.adaptivePrimary,
                                    modifier = Modifier.size(17.dp)
                                )
                            }
                        }
                    }
                }
            }

            Spacer(Modifier.height(4.dp))

            // Fila inferior: Saludo editorial cálido sin recortar
            Text(
                text = "Hola, $userName",
                fontSize = 22.sp,
                fontWeight = FontWeight.ExtraBold,
                color = a11y.adaptiveTextPrimary,
                letterSpacing = (-0.3).sp
            )
        }
    }
}

@Composable
fun ClinicalBottomBar(
    selectedTab: HomeTab,
    onSelectTab: (HomeTab) -> Unit
) {
    val a11y = LocalAccessibilitySettings.current
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Surface(
            shape = RoundedCornerShape(32.dp),
            color = if (a11y.isDarkTheme) Color(0xF20F172A) else Color(0xF5FFFFFF),
            border = BorderStroke(1.dp, if (a11y.isDarkTheme) Color(0x332DD4BF) else Color(0x330F766E)),
            shadowElevation = 16.dp,
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 6.dp, vertical = 5.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                BottomNavPill(
                    selected = selectedTab == HomeTab.HOY,
                    label = "Hoy",
                    icon = Icons.Outlined.CalendarToday,
                    onClick = { onSelectTab(HomeTab.HOY) },
                    modifier = Modifier.weight(1f)
                )
                BottomNavPill(
                    selected = selectedTab == HomeTab.MI_BOTIQUIN,
                    label = "Botiquín",
                    icon = Icons.Outlined.MedicalInformation,
                    onClick = { onSelectTab(HomeTab.MI_BOTIQUIN) },
                    modifier = Modifier.weight(1f)
                )
                BottomNavPill(
                    selected = selectedTab == HomeTab.SALUD_APOYO,
                    label = "Apoyo",
                    icon = Icons.Outlined.HealthAndSafety,
                    onClick = { onSelectTab(HomeTab.SALUD_APOYO) },
                    modifier = Modifier.weight(1f)
                )
                BottomNavPill(
                    selected = selectedTab == HomeTab.ANALISIS_DFS,
                    label = "Progreso",
                    icon = Icons.Outlined.BarChart,
                    onClick = { onSelectTab(HomeTab.ANALISIS_DFS) },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun BottomNavPill(
    selected: Boolean,
    label: String,
    icon: ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val a11y = LocalAccessibilitySettings.current
    Surface(
        shape = RoundedCornerShape(24.dp),
        color = if (selected) TealPrimary else Color.Transparent,
        modifier = modifier
            .height(56.dp)
            .bounceClick()
            .clip(RoundedCornerShape(24.dp))
            .clickable { onClick() }
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 2.dp, vertical = 4.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = label,
                tint = if (selected) Color.White else a11y.adaptiveTextSecondary,
                modifier = Modifier.size(19.dp)
            )
            Spacer(Modifier.height(2.dp))
            Text(
                text = label,
                fontSize = 11.sp,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                color = if (selected) Color.White else a11y.adaptiveTextSecondary,
                maxLines = 1,
                softWrap = false,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun HoyScreenContent(
    state: HomeUiState,
    onRegistrarTomaClick: (TomaHoyItemUi) -> Unit,
    onRevertirTomaClick: (Int) -> Unit,
    onNuevoMedClick: () -> Unit,
    onOpenVistaCuidador: () -> Unit = {},
    onCambiarRangoEdadDemo: (Boolean) -> Unit = {},
    onToggleTextoGrande: () -> Unit = {},
    onToggleAltoContraste: () -> Unit = {},
    onSpeakText: (String) -> Unit = {},
    isTtsSpeaking: Boolean = false,
    currentTtsKey: String? = null
) {
    val totalTomas = state.tomasHoy.size
    val completadas = state.tomasCompletadasCount
    val context = LocalContext.current
    val a11y = LocalAccessibilitySettings.current

    val infiniteTransition = rememberInfiniteTransition(label = "plan_ambient_anim")
    val shimmerOffset by infiniteTransition.animateFloat(
        initialValue = -300f,
        targetValue = 800f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 2200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "shimmer_x"
    )
    val flamePulse by infiniteTransition.animateFloat(
        initialValue = 0.94f,
        targetValue = 1.08f,
        animationSpec = infiniteRepeatable(
            animation = tween(850, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "flame_pulse"
    )

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(start = 18.dp, end = 18.dp, top = 8.dp, bottom = 96.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // 1. Tarjeta de Progreso Diario + Modo Adaptativo por Edad (Racha/Honor vs Supervisión Adulto Mayor)
        item {
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = a11y.adaptiveCardSurface,
                border = BorderStroke(a11y.borderWidth, a11y.adaptiveBorder),
                shadowElevation = 2.dp,
                modifier = Modifier
                    .fillMaxWidth()
                    .bounceClick()
            ) {
                Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(6.dp)
                                        .clip(CircleShape)
                                        .background(TealPrimary)
                                )
                                Spacer(Modifier.width(6.dp))
                                Text(
                                    text = if (totalTomas == 0) "Sin dosis pendientes hoy" else "$completadas de $totalTomas tomas completadas",
                                    fontSize = 14.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = a11y.adaptiveTextPrimary
                                )
                            }
                            Spacer(Modifier.height(8.dp))
                            val progressFraction = if (totalTomas > 0) completadas.toFloat() / totalTomas else 0f
                            val animProgress by animateFloatAsState(
                                targetValue = progressFraction,
                                animationSpec = tween(600, easing = FastOutSlowInEasing),
                                label = "daily_prog"
                            )
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth(0.94f)
                                    .height(5.dp)
                                    .clip(RoundedCornerShape(50))
                                    .background(a11y.adaptiveSoftSurface)
                            ) {
                                val shimmerBrush = Brush.linearGradient(
                                    colors = listOf(
                                        TealPrimary,
                                        Color(0xFF2DD4BF),
                                        Color(0xFF38BDF8),
                                        TealPrimary
                                    ),
                                    start = Offset(shimmerOffset, 0f),
                                    end = Offset(shimmerOffset + 320f, 0f)
                                )
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth(fraction = animProgress)
                                        .fillMaxHeight()
                                        .clip(RoundedCornerShape(50))
                                        .background(shimmerBrush)
                                )
                            }
                        }

                        // Dependiendo del rango de edad:
                        // - Joven/Adulto (< 60 años): Muestra Racha de Fuego y Rango de Honor
                        // - Adulto Mayor (>= 60 años): Muestra Insignia de Supervisión Geriátrica
                        if (!state.esAdultoMayor) {
                            Surface(
                                shape = RoundedCornerShape(14.dp),
                                color = TealBadgeBg,
                                modifier = Modifier
                                    .padding(start = 10.dp)
                                    .graphicsLayer {
                                        scaleX = flamePulse
                                        scaleY = flamePulse
                                    }
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.LocalFireDepartment,
                                        contentDescription = null,
                                        tint = TealPrimary,
                                        modifier = Modifier.size(15.dp)
                                    )
                                    Spacer(Modifier.width(4.dp))
                                    Text(
                                        text = "${state.rachaDias} d • ${state.rangoHonor}",
                                        fontSize = 11.5.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = TealDark
                                    )
                                }
                            }
                        } else {
                            Surface(
                                shape = RoundedCornerShape(14.dp),
                                color = Color(0xFFFFF3E0),
                                border = BorderStroke(1.dp, Color(0xFFFFB74D)),
                                modifier = Modifier.padding(start = 10.dp)
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 5.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.HealthAndSafety,
                                        contentDescription = null,
                                        tint = Color(0xFFE65100),
                                        modifier = Modifier.size(14.dp)
                                    )
                                    Spacer(Modifier.width(4.dp))
                                    Text(
                                        text = "${state.edadUsuario}a • Supervisión",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = Color(0xFFE65100)
                                    )
                                }
                            }
                        }
                    }

                    // Si es Joven/Adulto (<60 años), mostramos su barra de Rango de Honor y Escudos
                    if (!state.esAdultoMayor) {
                        Spacer(Modifier.height(10.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Outlined.EmojiEvents,
                                    contentDescription = null,
                                    tint = if (state.castigoActivo) AlertRedText else TealPrimary,
                                    modifier = Modifier.size(15.dp)
                                )
                                Spacer(Modifier.width(5.dp))
                                Text(
                                    text = if (state.castigoActivo) {
                                        "Honor ${state.rangoHonor} Penalizado (${state.puntosXp} XP)"
                                    } else {
                                        "Honor ${state.rangoHonor} (${state.puntosXp} XP) • ${state.escudosRacha} Escudos"
                                    },
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (state.castigoActivo) AlertRedText else a11y.adaptiveTextSecondary
                                )
                            }
                            Text(
                                text = "Modo Joven/Adulto (${state.edadUsuario}a)",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = TealPrimary
                            )
                        }
                    }

                    Spacer(Modifier.height(10.dp))

                    // Barra de Acciones Rápidas: Vista Cuidador + Alarma Nativa + Selector Rango de Edad
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        // Botón Vista Cuidador
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = if (a11y.isDarkTheme) Color(0xFF1B2B32) else TealSoftBg,
                            border = BorderStroke(1.dp, TealPrimary.copy(alpha = 0.35f)),
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { onOpenVistaCuidador() }
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.HealthAndSafety,
                                    contentDescription = null,
                                    tint = TealDark,
                                    modifier = Modifier.size(15.dp)
                                )
                                Spacer(Modifier.width(4.dp))
                                Text(
                                    text = "Vista Cuidador",
                                    fontSize = 11.5.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = TealDark,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                        }

                        // Botón Probar Alarma Nativa
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = if (a11y.isDarkTheme) Color(0xFF1E293B) else Color(0xFFE0F2FE),
                            border = BorderStroke(1.dp, Color(0xFF0284C7).copy(alpha = 0.35f)),
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(12.dp))
                                .clickable {
                                    val primera = state.tomasHoy.firstOrNull { it.estado == "pendiente" }
                                        ?: state.tomasHoy.firstOrNull()
                                    ReminderAlarmScheduler.triggerImmediateNativeAlarm(
                                        context = context,
                                        idRecordatorio = primera?.idRecordatorio ?: 777,
                                        nombreMedicamento = primera?.nombreMedicamento ?: "Losartán Potásico",
                                        dosisDetalle = primera?.dosisDetalle?.substringBefore("•")?.trim() ?: "50 mg",
                                        horaFormateada = primera?.horaFormateada ?: "Ahora",
                                        esCritico = primera?.esCritico ?: false,
                                        permitePosponer = primera?.permitePosponer ?: true
                                    )
                                }
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.AccessAlarm,
                                    contentDescription = null,
                                    tint = Color(0xFF0369A1),
                                    modifier = Modifier.size(15.dp)
                                )
                                Spacer(Modifier.width(4.dp))
                                Text(
                                    text = "Alarma Nativa",
                                    fontSize = 11.5.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = Color(0xFF0369A1),
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                        }

                        // Alternar Rango de Edad (Adulto Mayor 69a vs Joven 28a)
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = if (state.esAdultoMayor) Color(0xFFFFF8E1) else TealBadgeBg,
                            border = BorderStroke(
                                1.dp,
                                if (state.esAdultoMayor) Color(0xFFFFB300) else TealPrimary
                            ),
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { onCambiarRangoEdadDemo(!state.esAdultoMayor) }
                        ) {
                            Text(
                                text = if (state.esAdultoMayor) "Edad: 69a ⇄" else "Edad: 28a ⇄",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = if (state.esAdultoMayor) Color(0xFFE65100) else TealDark,
                                modifier = Modifier.padding(horizontal = 9.dp, vertical = 7.dp)
                            )
                        }
                    }
                }
            }
        }

        // 3. Banner de Modo Castigo / Delación al Cuidador (cuando hay omisiones o bajo Honor)
        if (state.castigoActivo || state.vecesOmitidasHoy > 0) {
            item {
                ModoCastigoCuidadorBanner(
                    vecesOmitidasHoy = state.vecesOmitidasHoy,
                    tomasCriticasOmitidas = state.tomasCriticasOmitidasHoy,
                    contactosApoyo = state.contactosApoyo
                )
            }
        }

        // 4. Lista de Medicamentos del Día (Inmediatamente visible sin excesivo scroll)
        if (state.isLoading && state.tomasHoy.isEmpty()) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 36.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = a11y.adaptivePrimary)
                }
            }
        } else if (state.tomasHoy.isEmpty()) {
            item {
                EmptyHoyCard(onNuevoMedClick = onNuevoMedClick)
            }
        } else {
            itemsIndexed(state.tomasHoy, key = { _, it -> it.idRecordatorio }) { index, item ->
                val isSpeakingThisToma = isTtsSpeaking && currentTtsKey == "toma_${item.idRecordatorio}"
                ConnectedTimelineTomaRow(
                    item = item,
                    isFirst = index == 0,
                    isLast = index == state.tomasHoy.size - 1,
                    modoAltoContraste = a11y.isHighContrast,
                    isSpeakingThisToma = isSpeakingThisToma,
                    onRegistrarClick = { onRegistrarTomaClick(item) },
                    onRevertirClick = { onRevertirTomaClick(item.idRecordatorio) },
                    onSpeakClick = {
                        if (isSpeakingThisToma) {
                            TtsHelper.stop()
                        } else {
                            TtsHelper.speakMedicationReminder(
                                context = context,
                                tomaId = item.idRecordatorio.toString(),
                                nombreMedicamento = item.nombreMedicamento,
                                dosisDetalle = item.dosisDetalle,
                                horaFormateada = item.horaFormateada,
                                esCritico = item.esCritico,
                                contraindicaciones = null
                            )
                        }
                    }
                )
            }
        }

        // Espaciador inferior ergonómico
        item {
            Spacer(Modifier.height(16.dp))
        }
    }
}

@Composable
private fun AccessibilityActionChip(
    icon: ImageVector,
    label: String,
    active: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val a11y = LocalAccessibilitySettings.current
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = if (active) a11y.adaptivePrimary else a11y.adaptiveCardSurface,
        border = BorderStroke(a11y.borderWidth, if (active) a11y.adaptivePrimary else a11y.adaptiveBorder),
        modifier = modifier
            .heightIn(min = 44.dp)
            .clip(RoundedCornerShape(16.dp))
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = label,
                tint = if (active) Color.White else a11y.adaptivePrimary,
                modifier = Modifier.size(18.dp)
            )
            Spacer(Modifier.width(6.dp))
            Text(
                text = label,
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                color = if (active) Color.White else a11y.adaptiveTextPrimary,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun UnifiedHeroPlanCard(
    fechaEncabezado: String,
    totalTomas: Int,
    completadas: Int,
    rachaDias: Int,
    escudosRacha: Int,
    rangoHonor: String,
    puntosXp: Int,
    progresoHonorPct: Int,
    castigoActivo: Boolean
) {
    val a11y = LocalAccessibilitySettings.current
    val (flameColor, flameBg, flameLabel) = when {
        castigoActivo || rachaDias <= 0 -> Triple(
            Color(0xFF607D8B),
            if (a11y.isDarkTheme) Color(0xFF1E262B) else Color(0xFFECEFF1),
            "Racha en riesgo"
        )
        rachaDias >= 30 -> Triple(
            Color(0xFF7C4DFF),
            if (a11y.isDarkTheme) Color(0xFF261D3A) else Color(0xFFEDE7F6),
            "Fuego Mítico • $rachaDias d"
        )
        rachaDias >= 7 -> Triple(
            Color(0xFF0288D1),
            if (a11y.isDarkTheme) Color(0xFF102835) else Color(0xFFE1F5FE),
            "Fuego Azul • $rachaDias d"
        )
        else -> Triple(
            Color(0xFFFF6D00),
            if (a11y.isDarkTheme) Color(0xFF332014) else Color(0xFFFFF3E0),
            "Racha • $rachaDias d"
        )
    }

    Surface(
        shape = RoundedCornerShape(24.dp),
        color = a11y.adaptiveCardSurface,
        border = BorderStroke(a11y.borderWidth, if (castigoActivo) Color(0xFFEF9A9A) else a11y.adaptiveBorder),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Badges superiores de racha, escudos y honor en FlowRow
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                // Insignia de Fuego Estilo TikTok
                Surface(
                    shape = RoundedCornerShape(50),
                    color = flameBg
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.LocalFireDepartment,
                            contentDescription = "Racha de fuego",
                            tint = flameColor,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(Modifier.width(4.dp))
                        Text(
                            text = flameLabel,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = flameColor
                        )
                    }
                }

                // Escudos Protectores de Racha
                Surface(
                    shape = RoundedCornerShape(50),
                    color = if (a11y.isDarkTheme) Color(0xFF1B2B32) else TealSoftBg
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Shield,
                            contentDescription = "Escudos de racha",
                            tint = a11y.adaptivePrimary,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(Modifier.width(4.dp))
                        Text(
                            text = "$escudosRacha Escudos",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = a11y.adaptivePrimary
                        )
                    }
                }

                // Rango de Honor y XP
                Surface(
                    shape = RoundedCornerShape(50),
                    color = if (castigoActivo) Color(0xFFFFEBEE) else (if (a11y.isDarkTheme) Color(0xFF1E2824) else Color(0xFFE8F5E9))
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.EmojiEvents,
                            contentDescription = null,
                            tint = if (castigoActivo) AlertRedText else (if (a11y.isDarkTheme) Color(0xFF81C784) else Color(0xFF2E7D32)),
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(Modifier.width(4.dp))
                        Text(
                            text = "$rangoHonor • $puntosXp XP",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (castigoActivo) AlertRedText else (if (a11y.isDarkTheme) Color(0xFF81C784) else Color(0xFF2E7D32))
                        )
                    }
                }
            }

            Spacer(Modifier.height(10.dp))

            // Barra sutil de progreso de Honor
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(5.dp)
                    .clip(RoundedCornerShape(50))
                    .background(a11y.adaptiveSoftSurface)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(fraction = (progresoHonorPct / 100f).coerceIn(0.06f, 1f))
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(if (castigoActivo) AlertRedText else a11y.adaptivePrimary)
                )
            }

            Spacer(Modifier.height(12.dp))

            // Sección Plan Diario con Anillo de Progreso
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "PLAN DIARIO",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 0.8.sp,
                        color = a11y.adaptivePrimary
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = fechaEncabezado,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = a11y.adaptiveTextPrimary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = if (totalTomas == 0) "Sin tomas programadas hoy"
                        else "$completadas de $totalTomas tomas completadas hoy",
                        fontSize = 13.sp,
                        color = a11y.adaptiveTextSecondary
                    )
                }
                Spacer(Modifier.width(10.dp))
                DailyProgressRing(
                    completadas = completadas,
                    total = totalTomas
                )
            }
        }
    }
}

@Composable
private fun DopaminaRachaHonorCard(
    rachaDias: Int,
    escudosRacha: Int,
    rangoHonor: String,
    puntosXp: Int,
    progresoHonorPct: Int,
    castigoActivo: Boolean
) {
    val (flameColor, flameBg, flameLabel) = when {
        castigoActivo || rachaDias <= 0 -> Triple(
            Color(0xFF607D8B),
            Color(0xFFECEFF1),
            "Racha en riesgo"
        )
        rachaDias >= 30 -> Triple(
            Color(0xFF7C4DFF),
            Color(0xFFEDE7F6),
            "Fuego Mítico • $rachaDias días"
        )
        rachaDias >= 7 -> Triple(
            Color(0xFF0288D1),
            Color(0xFFE1F5FE),
            "Fuego Azul • $rachaDias días"
        )
        else -> Triple(
            Color(0xFFFF6D00),
            Color(0xFFFFF3E0),
            "Racha activa • $rachaDias días"
        )
    }

    Surface(
        shape = RoundedCornerShape(26.dp),
        color = CardBackground,
        border = BorderStroke(1.5.dp, if (castigoActivo) Color(0xFFEF9A9A) else InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Insignia de Fuego Estilo TikTok
                Surface(
                    shape = RoundedCornerShape(50),
                    color = flameBg
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.LocalFireDepartment,
                            contentDescription = "Racha de fuego",
                            tint = flameColor,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = flameLabel,
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = flameColor
                        )
                    }
                }

                // Escudos Protectores de Racha
                Surface(
                    shape = RoundedCornerShape(50),
                    color = TealSoftBg
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Shield,
                            contentDescription = "Escudos de racha",
                            tint = TealDark,
                            modifier = Modifier.size(15.dp)
                        )
                        Spacer(Modifier.width(5.dp))
                        Text(
                            text = "$escudosRacha Escudos",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = TealDark
                        )
                    }
                }
            }

            Spacer(Modifier.height(14.dp))

            // Barra de Rango de Honor y XP
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Outlined.EmojiEvents,
                        contentDescription = null,
                        tint = if (castigoActivo) AlertRedText else TealPrimary,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        text = if (castigoActivo) "Honor $rangoHonor (Penalizado)" else "Rango de Honor: $rangoHonor",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = if (castigoActivo) AlertRedText else TextPrimary
                    )
                }
                Text(
                    text = "$puntosXp XP",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = TealPrimary
                )
            }

            Spacer(Modifier.height(8.dp))

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(RoundedCornerShape(50))
                    .background(SoftWarmSurface)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(fraction = (progresoHonorPct / 100f).coerceIn(0.08f, 1f))
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(if (castigoActivo) AlertRedText else TealPrimary)
                )
            }
        }
    }
}

@Composable
private fun ModoCastigoCuidadorBanner(
    vecesOmitidasHoy: Int,
    tomasCriticasOmitidas: Int,
    contactosApoyo: List<ContactoApoyoDto>
) {
    val context = LocalContext.current
    val contacto = contactosApoyo.firstOrNull { it.esPrincipal } ?: contactosApoyo.firstOrNull()

    Surface(
        shape = RoundedCornerShape(24.dp),
        color = Color(0xFFFFEBEE),
        border = BorderStroke(1.5.dp, Color(0xFFE57373)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    shape = CircleShape,
                    color = Color(0xFFFFCDD2),
                    modifier = Modifier.size(40.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Outlined.Warning,
                            contentDescription = null,
                            tint = Color(0xFFC62828),
                            modifier = Modifier.size(22.dp)
                        )
                    }
                }
                Spacer(Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "PENALIZACIÓN DE HONOR ACTIVA",
                        fontSize = 11.5.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color(0xFFB71C1C),
                        letterSpacing = 0.6.sp
                    )
                    Text(
                        text = if (tomasCriticasOmitidas > 0) {
                            "Omitiste $tomasCriticasOmitidas dosis crítica(s) hoy"
                        } else {
                            "Registraste $vecesOmitidasHoy dosis omitida(s) hoy (-45 XP)"
                        },
                        fontSize = 15.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color(0xFFC62828)
                    )
                }
            }

            Spacer(Modifier.height(8.dp))
            Text(
                text = "El botón 'Posponer 30 min' ha sido bloqueado temporalmente. Cumple tus próximas tomas a tiempo para restaurar tu Honor.",
                fontSize = 13.sp,
                color = Color(0xFF7F0000),
                lineHeight = 18.sp
            )

            Spacer(Modifier.height(12.dp))

            Button(
                onClick = {
                    val telefonoDestino = contacto?.telefono ?: ""
                    val nombreCuidador = contacto?.nombreCompleto ?: "Cuidador"
                    val mensajeAlerta = "Alerta MedReminder AI: Hola $nombreCuidador, se detectó la omisión de $vecesOmitidasHoy dosis programada(s) hoy. Por favor verifica mi seguimiento médico."
                    val smsIntent = Intent(Intent.ACTION_SENDTO).apply {
                        data = Uri.parse("smsto:$telefonoDestino")
                        putExtra("sms_body", mensajeAlerta)
                    }
                    runCatching { context.startActivity(smsIntent) }
                },
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFC62828)),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 52.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.Sms,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = if (contacto != null) {
                        "Notificar Incumplimiento a ${contacto.nombreCompleto}"
                    } else {
                        "Enviar Alerta de Incumplimiento al Cuidador"
                    },
                    fontSize = 13.5.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }
        }
    }
}

@Composable
private fun DailyProgressRing(
    completadas: Int,
    total: Int
) {
    val progress = if (total > 0) (completadas.toFloat() / total.toFloat()).coerceIn(0f, 1f) else 0f
    val animatedProgress by animateFloatAsState(targetValue = progress, label = "dailyRing")

    Box(
        modifier = Modifier.size(66.dp),
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val stroke = Stroke(width = 6.dp.toPx(), cap = StrokeCap.Round)
            drawArc(
                color = Color(0xFFE5E3E0),
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                style = stroke
            )
            if (animatedProgress > 0f) {
                drawArc(
                    color = TealPrimary,
                    startAngle = -90f,
                    sweepAngle = 360f * animatedProgress,
                    useCenter = false,
                    style = stroke
                )
            }
        }
        Text(
            text = "$completadas/$total",
            fontSize = 15.sp,
            fontWeight = FontWeight.ExtraBold,
            color = TealPrimary
        )
    }
}

@Composable
fun RealisticPillGraphic(
    forma: FormaFarmaceutica,
    palette: PillColorPalette,
    size: Dp = 48.dp
) {
    Canvas(modifier = Modifier.size(size)) {
        val w = size.toPx()
        val h = size.toPx()
        when (forma) {
            FormaFarmaceutica.COMPRIMIDOS -> {
                val pillW = w * 0.88f
                val pillH = h * 0.52f
                val left = (w - pillW) / 2f
                val top = (h - pillH) / 2f
                val radius = CornerRadius(pillH / 2f, pillH / 2f)

                // Sombra suave proyectada
                drawRoundRect(
                    color = Color.Black.copy(alpha = 0.07f),
                    topLeft = Offset(left, top + 2.dp.toPx()),
                    size = Size(pillW, pillH),
                    cornerRadius = radius
                )
                // Cuerpo con gradiente suave
                drawRoundRect(
                    brush = Brush.verticalGradient(
                        listOf(palette.containerBg, palette.dotColor.copy(alpha = 0.85f))
                    ),
                    topLeft = Offset(left, top),
                    size = Size(pillW, pillH),
                    cornerRadius = radius
                )
                // Borde fino
                drawRoundRect(
                    color = palette.iconTint.copy(alpha = 0.35f),
                    topLeft = Offset(left, top),
                    size = Size(pillW, pillH),
                    cornerRadius = radius,
                    style = Stroke(width = 1.2.dp.toPx())
                )
                // Ranura central divisoria (score line)
                drawLine(
                    color = palette.iconTint.copy(alpha = 0.45f),
                    start = Offset(w / 2f, top + 3.dp.toPx()),
                    end = Offset(w / 2f, top + pillH - 3.dp.toPx()),
                    strokeWidth = 1.4.dp.toPx(),
                    cap = StrokeCap.Round
                )
                // Brillo especular superior
                drawLine(
                    color = Color.White.copy(alpha = 0.70f),
                    start = Offset(left + pillH * 0.4f, top + 2.dp.toPx()),
                    end = Offset(left + pillW - pillH * 0.4f, top + 2.dp.toPx()),
                    strokeWidth = 1.2.dp.toPx(),
                    cap = StrokeCap.Round
                )
            }
            FormaFarmaceutica.GOTAS -> {
                val dropPath = Path().apply {
                    moveTo(w / 2f, h * 0.15f)
                    cubicTo(w * 0.25f, h * 0.55f, w * 0.20f, h * 0.85f, w / 2f, h * 0.85f)
                    cubicTo(w * 0.80f, h * 0.85f, w * 0.75f, h * 0.55f, w / 2f, h * 0.15f)
                    close()
                }
                drawPath(
                    path = dropPath,
                    brush = Brush.verticalGradient(listOf(Color(0xFFBAE6FD), Color(0xFF0284C7)))
                )
                drawPath(
                    path = dropPath,
                    color = Color(0xFF0369A1).copy(alpha = 0.45f),
                    style = Stroke(width = 1.2.dp.toPx())
                )
            }
            FormaFarmaceutica.INYECTABLE -> {
                val ampW = w * 0.48f
                val ampH = h * 0.76f
                val left = (w - ampW) / 2f
                val top = (h - ampH) / 2f
                val radius = CornerRadius(6.dp.toPx(), 6.dp.toPx())
                drawRoundRect(
                    brush = Brush.verticalGradient(listOf(Color(0xFFFEF08A), Color(0xFFD97706))),
                    topLeft = Offset(left, top),
                    size = Size(ampW, ampH),
                    cornerRadius = radius
                )
                drawRoundRect(
                    color = Color(0xFFB45309).copy(alpha = 0.5f),
                    topLeft = Offset(left, top),
                    size = Size(ampW, ampH),
                    cornerRadius = radius,
                    style = Stroke(width = 1.2.dp.toPx())
                )
                drawLine(
                    color = Color.White.copy(alpha = 0.85f),
                    start = Offset(left + 2.dp.toPx(), top + ampH * 0.35f),
                    end = Offset(left + ampW - 2.dp.toPx(), top + ampH * 0.35f),
                    strokeWidth = 2.dp.toPx()
                )
            }
        }
    }
}

@Composable
private fun ConnectedTimelineTomaRow(
    item: TomaHoyItemUi,
    isFirst: Boolean,
    isLast: Boolean,
    modoAltoContraste: Boolean,
    isSpeakingThisToma: Boolean = false,
    onRegistrarClick: () -> Unit,
    onRevertirClick: () -> Unit,
    onSpeakClick: () -> Unit
) {
    val a11y = LocalAccessibilitySettings.current
    val isTomado = item.estado == "tomado"
    val isPendiente = item.estado == "pendiente"
    val isOmitido = item.estado == "omitido"

    val infinitePulse = rememberInfiniteTransition(label = "pulse_node")
    val radarScale by infinitePulse.animateFloat(
        initialValue = 1f,
        targetValue = 2.4f,
        animationSpec = infiniteRepeatable(
            animation = tween(1600, easing = EaseInOutSine),
            repeatMode = RepeatMode.Restart
        ),
        label = "radar_scale"
    )
    val radarAlpha by infinitePulse.animateFloat(
        initialValue = 0.55f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1600, easing = EaseInOutSine),
            repeatMode = RepeatMode.Restart
        ),
        label = "radar_alpha"
    )

    val nodeColor = when {
        isTomado -> Color(0xFF10B981)
        isOmitido -> AlertRedText
        item.esCritico -> Color(0xFF0284C7)
        else -> a11y.adaptivePrimary
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(IntrinsicSize.Min),
        verticalAlignment = Alignment.Top
    ) {
        // Columna de Línea de Tiempo Conectada (Timeline Rail)
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .width(26.dp)
                .fillMaxHeight()
                .padding(top = 22.dp)
        ) {
            // Nodo iluminado de estado con halo de radar animado en dosis pendientes
            Box(
                modifier = Modifier.size(24.dp),
                contentAlignment = Alignment.Center
            ) {
                if (isPendiente) {
                    Box(
                        modifier = Modifier
                            .size(18.dp)
                            .graphicsLayer {
                                scaleX = radarScale
                                scaleY = radarScale
                                alpha = radarAlpha
                            }
                            .clip(CircleShape)
                            .background(nodeColor)
                    )
                }

                Box(
                    modifier = Modifier
                        .size(20.dp)
                        .clip(CircleShape)
                        .background(
                            if (isTomado) Color(0xFF10B981)
                            else if (isPendiente) nodeColor.copy(alpha = 0.16f)
                            else AlertRedBg
                        )
                        .border(
                            width = 2.dp,
                            color = nodeColor,
                            shape = CircleShape
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    if (isTomado) {
                        Icon(
                            imageVector = Icons.Default.Check,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(11.dp)
                        )
                    } else if (isPendiente) {
                        Box(
                            modifier = Modifier
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(nodeColor)
                        )
                    }
                }
            }

            // Línea conectora dinámica hacia la siguiente toma
            if (!isLast) {
                Box(
                    modifier = Modifier
                        .width(2.dp)
                        .weight(1f)
                        .background(
                            Brush.verticalGradient(
                                listOf(
                                    nodeColor.copy(alpha = 0.5f),
                                    a11y.adaptiveBorder.copy(alpha = 0.4f)
                                )
                            )
                        )
                )
            }
        }

        Spacer(Modifier.width(10.dp))

        // Tarjeta con diseño estilo Linear / Apple Health
        Box(modifier = Modifier.weight(1f)) {
            TomaHoyCard(
                item = item,
                modoAltoContraste = modoAltoContraste,
                isSpeakingThisToma = isSpeakingThisToma,
                onRegistrarClick = onRegistrarClick,
                onRevertirClick = onRevertirClick,
                onSpeakClick = onSpeakClick
            )
        }
    }
}

@Composable
private fun TomaHoyCard(
    item: TomaHoyItemUi,
    modoAltoContraste: Boolean,
    onRegistrarClick: () -> Unit,
    onRevertirClick: () -> Unit,
    onSpeakClick: () -> Unit,
    isSpeakingThisToma: Boolean = false
) {
    val a11y = LocalAccessibilitySettings.current
    val isPendiente = item.estado == "pendiente"
    val (badgeText, badgeBg, badgeColor) = when (item.estado) {
        "tomado" -> Triple("Tomado", if (a11y.isDarkTheme) Color(0xFF064E3B) else Color(0xFFD1FAE5), Color(0xFF10B981))
        "omitido" -> Triple("Omitido", AlertRedBg, AlertRedText)
        else -> Triple("Pendiente", TealBadgeBg, TealBadgeText)
    }

    val pillPalette = resolvePillPalette(item.colorPastilla)

    Surface(
        shape = RoundedCornerShape(26.dp),
        color = a11y.adaptiveCardSurface,
        border = BorderStroke(
            1.dp,
            if (modoAltoContraste) TealDark else a11y.adaptiveBorder
        ),
        shadowElevation = 4.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            // Fila superior: Micro-etiqueta Linear + Hora grande + Iconos
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = item.etiquetaPeriodo.uppercase(),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.sp,
                        color = a11y.adaptiveTextSecondary
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = item.horaFormateada,
                        fontSize = 28.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = a11y.adaptiveTextPrimary
                    )
                }

                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    IconButton(
                        onClick = onSpeakClick,
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(if (isSpeakingThisToma) a11y.adaptivePrimary.copy(alpha = 0.18f) else a11y.adaptiveSoftSurface)
                    ) {
                        if (isSpeakingThisToma) {
                            MiniVoiceWaveform(
                                isSpeaking = true,
                                color = a11y.adaptivePrimary,
                                modifier = Modifier.size(16.dp)
                            )
                        } else {
                            Icon(
                                imageVector = Icons.AutoMirrored.Outlined.VolumeUp,
                                contentDescription = "Escuchar indicación de toma",
                                tint = a11y.adaptivePrimary,
                                modifier = Modifier.size(17.dp)
                            )
                        }
                    }
                    Surface(
                        shape = RoundedCornerShape(50),
                        color = badgeBg
                    ) {
                        Text(
                            text = badgeText,
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = badgeColor,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp)
                        )
                    }
                }
            }

            if (item.vecesPospuesto > 0) {
                Spacer(Modifier.height(6.dp))
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = Color(0xFFFFF8E1),
                    border = BorderStroke(1.dp, Color(0xFFFFE082))
                ) {
                    Text(
                        text = "Pospuesto (${item.vecesPospuesto}/2)",
                        fontSize = 11.5.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFFE65100),
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            // Fila central: Gráfico de pastilla realista + Nombre de medicamento y dosis
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    shape = RoundedCornerShape(16.dp),
                    color = a11y.adaptiveSoftSurface,
                    modifier = Modifier.size(52.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        RealisticPillGraphic(
                            forma = item.formaFarmaceutica,
                            palette = pillPalette,
                            size = 38.dp
                        )
                    }
                }
                Spacer(Modifier.width(14.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = item.nombreMedicamento,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = a11y.adaptiveTextPrimary
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = item.dosisDetalle,
                        fontSize = 13.5.sp,
                        color = a11y.adaptiveTextSecondary
                    )
                }
            }

            // Alerta de Dosis Crítica
            if (item.esCritico || !item.permitePosponer) {
                Spacer(Modifier.height(10.dp))
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = Color(0xFFFFEBEE)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.NotificationImportant,
                            contentDescription = null,
                            tint = Color(0xFFD32F2F),
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "DOSIS CRÍTICA · NO POSPONIBLE",
                            fontSize = 10.5.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = Color(0xFFC62828),
                            letterSpacing = 0.5.sp
                        )
                    }
                }
            }

            Spacer(Modifier.height(16.dp))

            // Botón de acción principal estilo Linear
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Button(
                    onClick = onRegistrarClick,
                    enabled = isPendiente,
                    shape = RoundedCornerShape(16.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = TealPrimary,
                        disabledContainerColor = a11y.adaptiveSoftSurface
                    ),
                    modifier = Modifier
                        .weight(1f)
                        .heightIn(min = 52.dp)
                        .bounceClick()
                ) {
                    Icon(
                        imageVector = Icons.Default.Check,
                        contentDescription = null,
                        tint = if (isPendiente) Color.White else a11y.adaptiveTextSecondary,
                        modifier = Modifier.size(19.dp)
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = when (item.estado) {
                            "tomado" -> "Tomada"
                            "omitido" -> "Omitida"
                            else -> "Registrar Toma"
                        },
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        color = if (isPendiente) Color.White else a11y.adaptiveTextSecondary
                    )
                }

                if (!isPendiente) {
                    OutlinedButton(
                        onClick = onRevertirClick,
                        shape = RoundedCornerShape(16.dp),
                        border = BorderStroke(1.dp, a11y.adaptiveBorder),
                        contentPadding = PaddingValues(horizontal = 14.dp),
                        modifier = Modifier
                            .heightIn(min = 52.dp)
                            .bounceClick()
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Replay,
                            contentDescription = "Deshacer",
                            tint = a11y.adaptivePrimary,
                            modifier = Modifier.size(17.dp)
                        )
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "Deshacer",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            color = a11y.adaptivePrimary
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun EmptyHoyCard(onNuevoMedClick: () -> Unit) {
    Surface(
        shape = RoundedCornerShape(24.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Sin tomas pendientes para hoy",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
            Spacer(Modifier.height(6.dp))
            Text(
                text = "Registra un medicamento en tu botiquín para generar tus recordatorios automáticos.",
                fontSize = 14.sp,
                color = TextSecondary,
                textAlign = TextAlign.Center
            )
            Spacer(Modifier.height(18.dp))
            Button(
                onClick = onNuevoMedClick,
                shape = RoundedCornerShape(18.dp),
                colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 56.dp)
            ) {
                Text(
                    text = "Registrar Medicamento",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

/**
 * Control futurista "desliza para confirmar": es la ÚNICA vía para registrar la toma,
 * de modo que el paciente no pueda confirmar con un toque automático.
 */
@Composable
fun SwipeToConfirmTrack(
    enabled: Boolean,
    inFlight: Boolean,
    disabledHint: String,
    onConfirmed: () -> Unit,
    modifier: Modifier = Modifier
) {
    val thumbSize = 56.dp
    val pad = 4.dp
    val density = LocalDensity.current
    val scope = rememberCoroutineScope()
    val offset = remember { Animatable(0f) }
    val transition = rememberInfiniteTransition(label = "swipe_hint")
    val shimmer by transition.animateFloat(
        initialValue = 0f,
        targetValue = 8f,
        animationSpec = infiniteRepeatable(tween(900, easing = EaseInOutSine), RepeatMode.Reverse),
        label = "swipe_hint_shift"
    )

    LaunchedEffect(inFlight) {
        if (!inFlight && offset.value > 0f) offset.animateTo(0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium))
    }

    BoxWithConstraints(
        modifier = modifier
            .fillMaxWidth()
            .height(thumbSize + pad * 2)
            .clip(RoundedCornerShape(50))
            .background(if (enabled || inFlight) Color(0xFF0B1F24) else Color(0xFFCFD8DC))
            .border(
                1.dp,
                if (enabled || inFlight) Brush.horizontalGradient(listOf(Color(0xFF2DD4BF), Color(0xFF10B981)))
                else Brush.horizontalGradient(listOf(Color(0xFFB0BEC5), Color(0xFFB0BEC5))),
                RoundedCornerShape(50)
            )
    ) {
        val maxPx = with(density) { (maxWidth - thumbSize - pad * 2).toPx() }.coerceAtLeast(1f)
        val progress = (offset.value / maxPx).coerceIn(0f, 1f)

        // Estela de progreso
        Box(
            modifier = Modifier
                .fillMaxHeight()
                .width(thumbSize + pad * 2 + with(density) { offset.value.toDp() })
                .background(Brush.horizontalGradient(listOf(Color(0x332DD4BF), Color(0x9910B981))))
        )

        Text(
            text = when {
                inFlight -> "Registrando toma..."
                !enabled -> disabledHint
                progress > 0.6f -> "Suelta para confirmar"
                else -> "Desliza para confirmar  \u203A\u203A\u203A"
            },
            fontSize = 14.sp,
            fontWeight = FontWeight.Bold,
            color = if (enabled || inFlight) Color.White.copy(alpha = (1f - progress * 0.8f)) else Color(0xFF546E7A),
            textAlign = TextAlign.Center,
            modifier = Modifier
                .align(Alignment.Center)
                .padding(start = thumbSize / 2 + shimmer.dp, end = 12.dp)
        )

        var acc by remember { mutableFloatStateOf(0f) }
        Box(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset { IntOffset((with(density) { pad.toPx() } + offset.value).toInt(), 0) }
                .size(thumbSize)
                .clip(CircleShape)
                .background(
                    if (enabled || inFlight) Brush.linearGradient(listOf(Color(0xFF2DD4BF), Color(0xFF14B8A6)))
                    else Brush.linearGradient(listOf(Color(0xFF90A4AE), Color(0xFF78909C)))
                )
                .pointerInput(enabled, maxPx) {
                    if (!enabled) return@pointerInput
                    detectHorizontalDragGestures(
                        onDragStart = { acc = offset.value },
                        onHorizontalDrag = { change, dragAmount ->
                            change.consume()
                            acc = (acc + dragAmount).coerceIn(0f, maxPx)
                            val target = acc
                            scope.launch { offset.snapTo(target) }
                        },
                        onDragEnd = {
                            scope.launch {
                                if (acc / maxPx >= 0.9f) {
                                    offset.animateTo(maxPx, tween(120))
                                    onConfirmed()
                                } else {
                                    offset.animateTo(0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium))
                                }
                            }
                        },
                        onDragCancel = {
                            scope.launch { offset.animateTo(0f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium)) }
                        }
                    )
                },
            contentAlignment = Alignment.Center
        ) {
            if (inFlight) {
                CircularProgressIndicator(modifier = Modifier.size(24.dp), color = Color.White, strokeWidth = 2.5.dp)
            } else {
                Icon(
                    imageVector = if (progress > 0.9f) Icons.Outlined.CheckCircle else Icons.Outlined.Medication,
                    contentDescription = "Deslizar para confirmar toma",
                    tint = Color.White,
                    modifier = Modifier.size(26.dp)
                )
            }
        }
    }
}

/**
 * Pantalla 3: Modal de Confirmación de Toma con:
 * - Scroll vertical completo
 * - Check Visual Rápido de la pastilla (confirmar color/forma)
 * - Control de deslizar o mantener presionado 2 segundos (anti-piloto automático)
 * - Ventana de horario estricta y bloqueo de posponer por bajo Honor
 */
@Composable
fun ConfirmacionTomaModal(
    toma: TomaHoyItemUi,
    esAdultoMayor: Boolean = true,
    contactosApoyo: List<ContactoApoyoDto> = emptyList(),
    castigoPosponerBloqueado: Boolean = false,
    isActionInFlight: Boolean,
    onDismiss: () -> Unit,
    onTomarAhora: () -> Unit,
    onPosponer30Min: () -> Unit,
    onOmitirToma: () -> Unit,
    onSpeakText: (String) -> Unit = {}
) {
    val expectedPalette = resolvePillPalette(toma.colorPastilla)
    val checkOptions = remember(toma.colorPastilla) {
        val distractors = PILL_COLOR_OPTIONS.filter { it.key != expectedPalette.key }.take(2)
        (listOf(expectedPalette) + distractors).sortedBy { it.label }
    }

    var selectedColorKey by remember(toma.idRecordatorio) { mutableStateOf(expectedPalette.key) }
    val visualCheckPassed = selectedColorKey == expectedPalette.key

    var sliderProgress by remember(toma.idRecordatorio) { mutableFloatStateOf(0f) }
    var holdProgress by remember(toma.idRecordatorio) { mutableFloatStateOf(0f) }
    var earlyWindowUnlocked by remember(toma.idRecordatorio) { mutableStateOf(!toma.esEnFuturoLejano) }
    val scope = rememberCoroutineScope()

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.5f))
        ) {
            // Cabecera blanca superior con statusBarsPadding
            Surface(
                color = AppBackground,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 12.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = onDismiss, enabled = !isActionInFlight) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Cerrar",
                            tint = TextPrimary
                        )
                    }
                    MedBrandLogo(size = 36.dp, cornerRadius = 11.dp)
                    Spacer(Modifier.width(10.dp))
                    Text(
                        text = "Confirmación de Toma",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary,
                        modifier = Modifier.weight(1f)
                    )
                    val isTtsSpeaking by TtsHelper.isSpeaking.collectAsState()
                    val currentTtsKey by TtsHelper.currentKey.collectAsState()
                    val isSpeakingModal = isTtsSpeaking && currentTtsKey == "modal_confirmacion"

                    IconButton(
                        onClick = {
                            if (isSpeakingModal) {
                                TtsHelper.stop()
                            } else {
                                onSpeakText(
                                    "Confirmación de toma para ${toma.nombreMedicamento}. ${toma.instruccionesToma}. Confirma el color ${expectedPalette.label} y desliza el control hasta el final para registrar."
                                )
                            }
                        },
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(if (isSpeakingModal) TealDark.copy(alpha = 0.15f) else Color.Transparent)
                    ) {
                        if (isSpeakingModal) {
                            MiniVoiceWaveform(
                                isSpeaking = true,
                                color = TealDark,
                                modifier = Modifier.size(16.dp)
                            )
                        } else {
                            Icon(
                                imageVector = Icons.AutoMirrored.Outlined.VolumeUp,
                                contentDescription = "Escuchar instrucciones",
                                tint = TealDark,
                                modifier = Modifier.size(19.dp)
                            )
                        }
                    }
                }
            }

            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .navigationBarsPadding()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                contentAlignment = Alignment.Center
            ) {
                Surface(
                    shape = RoundedCornerShape(30.dp),
                    color = CardBackground,
                    shadowElevation = 12.dp,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier
                            .verticalScroll(rememberScrollState())
                            .padding(horizontal = 22.dp, vertical = 20.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Box(
                            modifier = Modifier
                                .width(48.dp)
                                .height(5.dp)
                                .clip(RoundedCornerShape(50))
                                .background(Color(0xFFDCDAD7))
                        )

                        Spacer(Modifier.height(14.dp))

                        // Pill "Toma de las 08:00 AM"
                        Surface(
                            shape = RoundedCornerShape(50),
                            color = TealBadgeBg
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 16.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.AccessAlarm,
                                    contentDescription = null,
                                    tint = TealBadgeText,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(Modifier.width(6.dp))
                                Text(
                                    text = "Toma de las ${toma.horaFormateada}",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TealBadgeText
                                )
                            }
                        }

                        Spacer(Modifier.height(16.dp))

                        // Cabecera Biomédica Futurista: Pastilla + Medi acompañando al paciente
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(16.dp)
                        ) {
                            Surface(
                                shape = CircleShape,
                                color = expectedPalette.containerBg,
                                border = BorderStroke(2.dp, expectedPalette.iconTint.copy(alpha = 0.45f)),
                                shadowElevation = 6.dp,
                                modifier = Modifier.size(68.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = resolveFormaIcon(toma.formaFarmaceutica),
                                        contentDescription = null,
                                        tint = expectedPalette.iconTint,
                                        modifier = Modifier.size(34.dp)
                                    )
                                }
                            }

                            MediMascotView(
                                size = 66.dp,
                                mood = if (isActionInFlight) com.medreminder.ai.ui.components.MediMood.CELEBRATING
                                    else if (visualCheckPassed) com.medreminder.ai.ui.components.MediMood.HAPPY
                                    else com.medreminder.ai.ui.components.MediMood.ATTENTIVE,
                                animateHover = true
                            )
                        }

                        Spacer(Modifier.height(12.dp))

                        Text(
                            text = toma.nombreMedicamento,
                            fontSize = 24.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary,
                            textAlign = TextAlign.Center
                        )

                        Spacer(Modifier.height(4.dp))

                        Text(
                            text = "Dosis programada: ${toma.dosisDetalle.substringBefore("•").trim()}",
                            fontSize = 15.sp,
                            color = TextSecondary,
                            textAlign = TextAlign.Center
                        )

                        Spacer(Modifier.height(14.dp))

                        // Caja de instrucción clínica real del medicamento
                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = SoftWarmSurface,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Row(
                                modifier = Modifier.padding(14.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.Info,
                                    contentDescription = null,
                                    tint = TealPrimary,
                                    modifier = Modifier.size(20.dp)
                                )
                                Spacer(Modifier.width(10.dp))
                                Text(
                                    text = "Indicación: ${toma.instruccionesToma}",
                                    fontSize = 13.5.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = TextPrimary,
                                    lineHeight = 18.sp
                                )
                            }
                        }

                        // Ventana de horario estricta si falta > 2 horas
                        if (toma.esEnFuturoLejano && !earlyWindowUnlocked) {
                            Spacer(Modifier.height(12.dp))
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = Color(0xFFFFF8E1),
                                border = BorderStroke(1.dp, Color(0xFFFFB300)),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text(
                                        text = "Ventana de horario anticipada",
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = Color(0xFFE65100)
                                    )
                                    Spacer(Modifier.height(4.dp))
                                    Text(
                                        text = "Esta dosis está programada para más adelante (${toma.horaFormateada}). ¿Deseas desbloquear el registro anticipado?",
                                        fontSize = 12.sp,
                                        color = Color(0xFF5D4037)
                                    )
                                    Spacer(Modifier.height(8.dp))
                                    TextButton(onClick = { earlyWindowUnlocked = true }) {
                                        Text("Desbloquear registro anticipado", fontWeight = FontWeight.Bold, color = TealDark)
                                    }
                                }
                            }
                        }

                        Spacer(Modifier.height(14.dp))

                        // Check Visual Rápido de la pastilla
                        Surface(
                            shape = RoundedCornerShape(18.dp),
                            color = Color(0xFFF8FAFC),
                            border = BorderStroke(1.dp, InputBorderColor),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Column(modifier = Modifier.padding(14.dp)) {
                                Text(
                                    text = "1. Verificación visual rápida: confirma el color/forma",
                                    fontSize = 12.5.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = TextPrimary
                                )
                                Spacer(Modifier.height(8.dp))
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                                ) {
                                    checkOptions.forEach { option ->
                                        val isSelected = selectedColorKey == option.key
                                        Surface(
                                            shape = RoundedCornerShape(14.dp),
                                            color = if (isSelected) option.containerBg else Color.White,
                                            border = BorderStroke(
                                                width = if (isSelected) 2.dp else 1.dp,
                                                color = if (isSelected) option.iconTint else InputBorderColor
                                            ),
                                            modifier = Modifier
                                                .weight(1f)
                                                .heightIn(min = 48.dp)
                                                .clip(RoundedCornerShape(14.dp))
                                                .clickable { selectedColorKey = option.key }
                                        ) {
                                            Row(
                                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 10.dp),
                                                verticalAlignment = Alignment.CenterVertically,
                                                horizontalArrangement = Arrangement.Center
                                            ) {
                                                Box(
                                                    modifier = Modifier
                                                        .size(12.dp)
                                                        .clip(CircleShape)
                                                        .background(option.dotColor)
                                                )
                                                Spacer(Modifier.width(6.dp))
                                                Text(
                                                    text = option.label,
                                                    fontSize = 12.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    color = TextPrimary,
                                                    maxLines = 1,
                                                    overflow = TextOverflow.Ellipsis
                                                )
                                            }
                                        }
                                    }
                                }
                                if (!visualCheckPassed) {
                                    Spacer(Modifier.height(6.dp))
                                    Text(
                                        text = "Selecciona el color registrado de tu medicamento (${expectedPalette.label}) para continuar.",
                                        fontSize = 11.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = AlertRedText
                                    )
                                }
                            }
                        }

                        Spacer(Modifier.height(14.dp))

                        // Botón de Confirmación Directa Futurista (1 toque directo sin fricción)
                        Button(
                            onClick = onTomarAhora,
                            enabled = visualCheckPassed && earlyWindowUnlocked && !isActionInFlight,
                            shape = RoundedCornerShape(18.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = TealPrimary,
                                disabledContainerColor = Color(0xFFE2E8F0)
                            ),
                            elevation = ButtonDefaults.buttonElevation(defaultElevation = 6.dp, pressedElevation = 2.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(min = 54.dp)
                                .bounceClick()
                        ) {
                            if (isActionInFlight) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(20.dp),
                                    color = Color.White,
                                    strokeWidth = 2.dp
                                )
                                Spacer(Modifier.width(10.dp))
                                Text(
                                    text = "Registrando toma...",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color.White
                                )
                            } else {
                                Icon(
                                    imageVector = Icons.Default.Check,
                                    contentDescription = null,
                                    tint = if (visualCheckPassed && earlyWindowUnlocked) Color.White else Color.Gray,
                                    modifier = Modifier.size(20.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = "Confirmar toma ahora",
                                    fontSize = 15.5.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = if (visualCheckPassed && earlyWindowUnlocked) Color.White else Color.Gray
                                )
                            }
                        }

                        Spacer(Modifier.height(10.dp))

                        // Control gestual alternativo para quien prefiera deslizar
                        Text(
                            text = "— o desliza si prefieres confirmación gestual —",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Medium,
                            color = TextSecondary,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(Modifier.height(6.dp))
                        SwipeToConfirmTrack(
                            enabled = visualCheckPassed && earlyWindowUnlocked && !isActionInFlight,
                            inFlight = isActionInFlight,
                            disabledHint = if (!visualCheckPassed) "Verifica el color para continuar" else "Desbloquea el registro anticipado",
                            onConfirmed = onTomarAhora
                        )

                        Spacer(Modifier.height(12.dp))

                        // 2. Botón Posponer 30 min (bloqueado si es Crítico, límite de posposiciones, o Castigo por bajo Honor)
                        val snoozeBlockedByCritico = toma.esCritico || !toma.permitePosponer
                        val snoozeBlockedByLimit = toma.vecesPospuesto >= 2
                        val snoozeBlockedByHonor = castigoPosponerBloqueado

                        if (snoozeBlockedByCritico || snoozeBlockedByLimit || snoozeBlockedByHonor) {
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = if (snoozeBlockedByCritico) Color(0xFFFFEBEE) else Color(0xFFFAFAFA),
                                border = BorderStroke(1.dp, if (snoozeBlockedByCritico) Color(0xFFFFCDD2) else Color(0xFFE0E0E0)),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .heightIn(min = 54.dp)
                            ) {
                                Row(
                                    modifier = Modifier.padding(14.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.Center
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.Lock,
                                        contentDescription = null,
                                        tint = if (snoozeBlockedByCritico) Color(0xFFC62828) else Color(0xFF757575),
                                        modifier = Modifier.size(18.dp)
                                    )
                                    Spacer(Modifier.width(8.dp))
                                    Text(
                                        text = when {
                                            snoozeBlockedByCritico -> "Posponer Prohibido (Dosis Crítica)"
                                            snoozeBlockedByHonor -> "Bloqueado por bajo Honor — cumple a tiempo"
                                            else -> "Límite de posposiciones alcanzado (2/2)"
                                        },
                                        fontSize = 13.5.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = if (snoozeBlockedByCritico) Color(0xFFC62828) else Color(0xFF616161)
                                    )
                                }
                            }

                            val contactoPrincipal = contactosApoyo.firstOrNull { it.esPrincipal } ?: contactosApoyo.firstOrNull()
                            if (contactoPrincipal != null) {
                                Spacer(Modifier.height(10.dp))
                                val context = LocalContext.current
                                Button(
                                    onClick = {
                                        val intent = Intent(Intent.ACTION_DIAL).apply {
                                            data = Uri.parse("tel:${contactoPrincipal.telefono}")
                                        }
                                        context.startActivity(intent)
                                    },
                                    enabled = !isActionInFlight,
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF37474F)),
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .heightIn(min = 52.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.Phone,
                                        contentDescription = null,
                                        tint = Color.White,
                                        modifier = Modifier.size(18.dp)
                                    )
                                    Spacer(Modifier.width(8.dp))
                                    Text(
                                        text = "Llamar a ${contactoPrincipal.nombreCompleto}",
                                        fontSize = 14.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color.White
                                    )
                                }
                            }
                        } else {
                            OutlinedButton(
                                onClick = onPosponer30Min,
                                enabled = !isActionInFlight,
                                shape = RoundedCornerShape(18.dp),
                                border = BorderStroke(1.dp, InputBorderColor),
                                colors = ButtonDefaults.outlinedButtonColors(
                                    containerColor = CardBackground,
                                    contentColor = TealPrimary
                                ),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .heightIn(min = 56.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.AccessAlarm,
                                    contentDescription = null,
                                    tint = TealPrimary,
                                    modifier = Modifier.size(20.dp)
                                )
                                Spacer(Modifier.width(10.dp))
                                Text(
                                    text = if (esAdultoMayor) {
                                        "Posponer 30 min (Notifica al Cuidador)"
                                    } else {
                                        "Posponer 30 min (${toma.vecesPospuesto}/2)"
                                    },
                                    fontSize = 14.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TealPrimary
                                )
                            }
                        }

                        Spacer(Modifier.height(6.dp))

                        // 3. Omisión: Si es crítico y se omite/no se toma, envía automáticamente la alerta crítica al cuidador
                        if (toma.esCritico) {
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = Color(0xFFFFEBEE),
                                border = BorderStroke(1.dp, Color(0xFFFFCDD2)),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(top = 8.dp)
                            ) {
                                Column(modifier = Modifier.padding(14.dp)) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(
                                            imageVector = Icons.Outlined.Lock,
                                            contentDescription = null,
                                            tint = Color(0xFFC62828),
                                            modifier = Modifier.size(20.dp)
                                        )
                                        Spacer(Modifier.width(10.dp))
                                        Column {
                                            Text(
                                                text = "Dosis Crítica Vital Obligatoria",
                                                fontSize = 13.5.sp,
                                                fontWeight = FontWeight.ExtraBold,
                                                color = Color(0xFFC62828)
                                            )
                                            Spacer(Modifier.height(2.dp))
                                            Text(
                                                text = "Por ser un medicamento crítico, si lo omites se enviará AUTOMÁTICAMENTE una alerta urgente a tu cuidador.",
                                                fontSize = 12.sp,
                                                color = Color(0xFFB71C1C),
                                                lineHeight = 16.sp
                                            )
                                        }
                                    }
                                    Spacer(Modifier.height(10.dp))
                                    OutlinedButton(
                                        onClick = onOmitirToma,
                                        enabled = !isActionInFlight,
                                        shape = RoundedCornerShape(12.dp),
                                        border = BorderStroke(1.2.dp, Color(0xFFC62828)),
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Icon(
                                            imageVector = Icons.Outlined.NotificationImportant,
                                            contentDescription = null,
                                            tint = Color(0xFFC62828),
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Spacer(Modifier.width(6.dp))
                                        Text(
                                            text = "No puedo tomarla (Enviar Alerta Automática al Cuidador)",
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = Color(0xFFC62828)
                                        )
                                    }
                                }
                            }
                        } else {
                            TextButton(
                                onClick = onOmitirToma,
                                enabled = !isActionInFlight,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .heightIn(min = 56.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Close,
                                    contentDescription = null,
                                    tint = OmitBrownText,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = if (esAdultoMayor) {
                                        "Omitir Toma (Enviará Alerta a tu Cuidador)"
                                    } else {
                                        "Omitir Toma (-45 XP • Penaliza Honor)"
                                    },
                                    fontSize = 14.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = OmitBrownText
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun LogoutConfirmDialog(
    nombreUsuario: String,
    onDismiss: () -> Unit,
    onConfirmLogout: () -> Unit
) {
    Dialog(onDismissRequest = onDismiss) {
        Surface(
            shape = RoundedCornerShape(26.dp),
            color = CardBackground,
            shadowElevation = 10.dp,
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(22.dp)) {
                Text(
                    text = "¿Cerrar sesión?",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = TextPrimary
                )
                Spacer(Modifier.height(8.dp))
                Text(
                    text = "Sesión activa de ${nombreUsuario.ifBlank { "Paciente" }}. Tus medicamentos y recordatorios seguirán guardados de forma segura.",
                    fontSize = 14.sp,
                    color = TextSecondary,
                    lineHeight = 20.sp
                )
                Spacer(Modifier.height(20.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedButton(
                        onClick = onDismiss,
                        shape = RoundedCornerShape(16.dp),
                        border = BorderStroke(1.dp, InputBorderColor),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 52.dp)
                    ) {
                        Text("Cancelar", fontWeight = FontWeight.Bold, color = TextPrimary)
                    }
                    Button(
                        onClick = onConfirmLogout,
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = AlertRedText),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 52.dp)
                    ) {
                        Text("Cerrar sesión", fontWeight = FontWeight.Bold, color = Color.White)
                    }
                }
            }
        }
    }
}

