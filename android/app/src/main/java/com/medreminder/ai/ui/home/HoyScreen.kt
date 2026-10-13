package com.medreminder.ai.ui.home

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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AccessAlarm
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.material.icons.outlined.CalendarToday
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.MedicalInformation
import androidx.compose.material.icons.outlined.MedicalServices
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.ui.components.MedBrandLogo
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.AppBackground
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.CyanIconBg
import com.medreminder.ai.ui.theme.CyanIconTint
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

/**
 * Contenedor principal post-autenticación que coordina:
 * - Pantalla 4: Hoy / Plan Diario
 * - Pantalla 3: Confirmación de Toma (Modal sobre Hoy)
 * - Pantalla 6: Mi Botiquín
 * - Pantalla 5: Registrar Medicamento
 */
@Composable
fun HomeRoute(
    viewModel: HomeViewModel,
    onLogout: () -> Unit
) {
    val state by viewModel.state.collectAsState()
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(state.snackbarMessage) {
        state.snackbarMessage?.let { msg ->
            snackbarHostState.showSnackbar(msg)
            viewModel.onSnackbarShown()
        }
    }

    if (state.showNuevoMedicamento) {
        NuevoMedicamentoScreen(
            form = state.form,
            snackbarHostState = snackbarHostState,
            onBack = viewModel::onCloseNuevoMedicamento,
            onFormaChange = viewModel::onFormaChange,
            onNombreChange = viewModel::onNombreMedChange,
            onDosisChange = viewModel::onDosisMedChange,
            onFrecuenciaTextoChange = viewModel::onFrecuenciaTextoChange,
            onSelectFrecuenciaChip = viewModel::onSelectFrecuenciaChip,
            onStockTextoChange = viewModel::onStockTextoChange,
            onIncrementStock = viewModel::onIncrementStock,
            onGuardar = viewModel::onGuardarMedicamento
        )
        return
    }

    Scaffold(
        containerColor = AppBackground,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            ClinicalBrandTopBar(
                subtitle = when (state.selectedTab) {
                    HomeTab.HOY -> "Hoy"
                    HomeTab.MI_BOTIQUIN -> "Mi Botiquín"
                    HomeTab.ANALISIS_DFS -> "Análisis y Búsqueda DFS"
                },
                onProfileClick = onLogout
            )
        },
        bottomBar = {
            ClinicalBottomBar(
                selectedTab = state.selectedTab,
                onSelectTab = viewModel::onSelectTab
            )
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when (state.selectedTab) {
                HomeTab.HOY -> HoyScreenContent(
                    state = state,
                    onRegistrarTomaClick = viewModel::onOpenConfirmacionToma,
                    onNuevoMedClick = viewModel::onOpenNuevoMedicamento
                )

                HomeTab.MI_BOTIQUIN -> BotiquinScreenContent(
                    state = state,
                    onAddMedicamentoClick = viewModel::onOpenNuevoMedicamento
                )

                HomeTab.ANALISIS_DFS -> AnalisisDfsScreenContent(
                    state = state
                )
            }

            // Pantalla 3: Modal de Confirmación de Toma
            state.selectedTomaForModal?.let { toma ->
                ConfirmacionTomaModal(
                    toma = toma,
                    isActionInFlight = state.isActionInFlight,
                    onDismiss = viewModel::onDismissConfirmacionToma,
                    onTomarAhora = viewModel::onTomarAhora,
                    onPosponer30Min = viewModel::onPosponer30Min,
                    onOmitirToma = viewModel::onOmitirToma
                )
            }
        }
    }
}

@Composable
fun ClinicalBrandTopBar(
    subtitle: String,
    onProfileClick: () -> Unit
) {
    Column(modifier = Modifier.background(AppBackground)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            MedBrandLogo(size = 40.dp, cornerRadius = 11.dp)
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "MEDREMINDER AI",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 0.8.sp,
                    color = TealDark
                )
                Text(
                    text = subtitle,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary
                )
            }
            Surface(
                shape = CircleShape,
                color = TealDark,
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .clickable { onProfileClick() }
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Outlined.Person,
                        contentDescription = "Perfil / Cerrar sesión",
                        tint = Color.White,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }
        HorizontalDivider(color = InputBorderColor, thickness = 1.dp)
    }
}

@Composable
fun ClinicalBottomBar(
    selectedTab: HomeTab,
    onSelectTab: (HomeTab) -> Unit
) {
    Surface(
        color = CardBackground,
        shadowElevation = 8.dp
    ) {
        Column {
            HorizontalDivider(color = InputBorderColor, thickness = 1.dp)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
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
                    selected = selectedTab == HomeTab.ANALISIS_DFS,
                    label = "Análisis",
                    icon = Icons.Outlined.AccountTree,
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
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        shape = RoundedCornerShape(14.dp),
        color = if (selected) TealPrimary else Color.Transparent,
        modifier = modifier
            .heightIn(min = 52.dp)
            .clip(RoundedCornerShape(14.dp))
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = label,
                tint = if (selected) Color.White else TextPrimary,
                modifier = Modifier.size(18.dp)
            )
            Spacer(Modifier.width(6.dp))
            Text(
                text = label,
                fontSize = 13.5.sp,
                fontWeight = FontWeight.Bold,
                color = if (selected) Color.White else TextPrimary,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun HoyScreenContent(
    state: HomeUiState,
    onRegistrarTomaClick: (TomaHoyItemUi) -> Unit,
    onNuevoMedClick: () -> Unit
) {
    val totalTomas = state.tomasHoy.size
    val completadas = state.tomasCompletadasCount

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 20.dp, vertical = 18.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        // Tarjeta Plan Diario
        item {
            Surface(
                shape = RoundedCornerShape(22.dp),
                color = CardBackground,
                border = BorderStroke(1.dp, InputBorderColor),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(20.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "PLAN DIARIO",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.ExtraBold,
                            letterSpacing = 0.8.sp,
                            color = TealPrimary
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = state.fechaEncabezado,
                            fontSize = 24.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "$totalTomas tomas programadas",
                            fontSize = 14.sp,
                            color = TextSecondary
                        )
                    }
                    Spacer(Modifier.width(12.dp))
                    // Anillo circular 0/3
                    Surface(
                        shape = CircleShape,
                        color = SoftWarmSurface,
                        border = BorderStroke(4.dp, Color(0xFFE5E3E0)),
                        modifier = Modifier.size(64.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Text(
                                text = "$completadas/$totalTomas",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                color = TealPrimary
                            )
                        }
                    }
                }
            }
        }

        if (state.isLoading && state.tomasHoy.isEmpty()) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 48.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = TealPrimary)
                }
            }
        } else if (state.tomasHoy.isEmpty()) {
            item {
                EmptyHoyCard(onNuevoMedClick = onNuevoMedClick)
            }
        } else {
            itemsIndexed(state.tomasHoy, key = { _, it -> it.idRecordatorio }) { index, item ->
                TomaHoyCard(
                    item = item,
                    iconIndex = index,
                    onRegistrarClick = { onRegistrarTomaClick(item) }
                )
            }
        }

        // Banner inferior de valor médico legal
        item {
            Surface(
                shape = RoundedCornerShape(18.dp),
                color = SoftWarmSurface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Surface(
                        shape = CircleShape,
                        color = TealBadgeBg,
                        modifier = Modifier.size(40.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Outlined.Shield,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    }
                    Spacer(Modifier.width(14.dp))
                    Text(
                        text = "Registro con valor médico legal. Cada dosis queda registrada con marca de tiempo precisa.",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = TextPrimary,
                        lineHeight = 18.sp
                    )
                }
            }
        }
    }
}

@Composable
private fun TomaHoyCard(
    item: TomaHoyItemUi,
    iconIndex: Int,
    onRegistrarClick: () -> Unit
) {
    val isPendiente = item.estado == "pendiente"
    val (badgeText, badgeBg, badgeColor) = when (item.estado) {
        "tomado" -> Triple("Tomado", TealBadgeBg, TealPrimary)
        "omitido" -> Triple("Omitido", AlertRedBg, AlertRedText)
        else -> Triple("Pendiente", TealBadgeBg, TealBadgeText)
    }

    val medIcon = when (iconIndex % 3) {
        0 -> Icons.Outlined.Medication
        1 -> Icons.Outlined.MedicalInformation
        else -> Icons.Outlined.EditNote
    }

    Surface(
        shape = RoundedCornerShape(24.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column {
                    Text(
                        text = item.etiquetaPeriodo,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 0.6.sp,
                        color = TextSecondary
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = item.horaFormateada,
                        fontSize = 32.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                }
                Surface(
                    shape = RoundedCornerShape(50),
                    color = badgeBg
                ) {
                    Text(
                        text = badgeText,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = badgeColor,
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 6.dp)
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    shape = RoundedCornerShape(14.dp),
                    color = SoftWarmSurface,
                    modifier = Modifier.size(48.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = medIcon,
                            contentDescription = null,
                            tint = TealPrimary,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }
                Spacer(Modifier.width(14.dp))
                Column {
                    Text(
                        text = item.nombreMedicamento,
                        fontSize = 19.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = item.dosisDetalle,
                        fontSize = 14.sp,
                        color = TextSecondary
                    )
                }
            }

            Spacer(Modifier.height(18.dp))

            // Botón Registrar Toma (>= 56dp)
            Button(
                onClick = onRegistrarClick,
                enabled = isPendiente,
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = TealPrimary,
                    disabledContainerColor = SoftWarmSurface
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 56.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Check,
                    contentDescription = null,
                    tint = if (isPendiente) Color.White else TextSecondary,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = when (item.estado) {
                        "tomado" -> "Toma Registrada"
                        "omitido" -> "Toma Omitida"
                        else -> "Registrar Toma"
                    },
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isPendiente) Color.White else TextSecondary
                )
            }
        }
    }
}

@Composable
private fun EmptyHoyCard(onNuevoMedClick: () -> Unit) {
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
                shape = RoundedCornerShape(16.dp),
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
 * Pantalla 3: Modal / Hoja de Confirmación de Toma.
 * Incluye barra superior "Confirmación De Toma", tarjeta modal con píldora cian,
 * "Tomar Ahora", "Posponer 30 min" y "Omitir Toma".
 */
@Composable
fun ConfirmacionTomaModal(
    toma: TomaHoyItemUi,
    isActionInFlight: Boolean,
    onDismiss: () -> Unit,
    onTomarAhora: () -> Unit,
    onPosponer30Min: () -> Unit,
    onOmitirToma: () -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.45f))
        ) {
            // Cabecera blanca superior idéntica a la captura "Confirmación De Toma"
            Surface(
                color = AppBackground,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
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
                    MedBrandLogo(size = 36.dp, cornerRadius = 10.dp)
                    Spacer(Modifier.width(10.dp))
                    Text(
                        text = "Confirmación De Toma",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary,
                        modifier = Modifier.weight(1f)
                    )
                    Surface(
                        shape = CircleShape,
                        color = TealDark,
                        modifier = Modifier.size(36.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Outlined.Person,
                                contentDescription = null,
                                tint = Color.White,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                }
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 16.dp, vertical = 28.dp),
                contentAlignment = Alignment.Center
            ) {
                Surface(
                    shape = RoundedCornerShape(30.dp),
                    color = CardBackground,
                    shadowElevation = 12.dp,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier.padding(horizontal = 22.dp, vertical = 20.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        // Indicador superior tipo drag handle
                        Box(
                            modifier = Modifier
                                .width(48.dp)
                                .height(5.dp)
                                .clip(RoundedCornerShape(50))
                                .background(Color(0xFFDCDAD7))
                        )

                        Spacer(Modifier.height(16.dp))

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

                        Spacer(Modifier.height(20.dp))

                        // Círculo cian con ícono de cápsula
                        Surface(
                            shape = CircleShape,
                            color = CyanIconBg,
                            modifier = Modifier.size(68.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.Medication,
                                    contentDescription = null,
                                    tint = CyanIconTint,
                                    modifier = Modifier.size(32.dp)
                                )
                            }
                        }

                        Spacer(Modifier.height(16.dp))

                        Text(
                            text = toma.nombreMedicamento,
                            fontSize = 26.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary,
                            textAlign = TextAlign.Center
                        )

                        Spacer(Modifier.height(6.dp))

                        Text(
                            text = "Dosis programada: ${toma.dosisDetalle.substringBefore("•").trim()} con agua",
                            fontSize = 15.sp,
                            color = TextSecondary,
                            textAlign = TextAlign.Center
                        )

                        Spacer(Modifier.height(18.dp))

                        // Caja de instrucción clínica
                        Surface(
                            shape = RoundedCornerShape(14.dp),
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
                                    text = "Tomar junto con alimentos o leche para proteger el estómago.",
                                    fontSize = 13.5.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = TextPrimary,
                                    lineHeight = 18.sp
                                )
                            }
                        }

                        Spacer(Modifier.height(22.dp))

                        // 1. Botón Tomar Ahora (>= 56dp)
                        Button(
                            onClick = onTomarAhora,
                            enabled = !isActionInFlight,
                            shape = RoundedCornerShape(18.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(min = 58.dp)
                        ) {
                            if (isActionInFlight) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(22.dp),
                                    color = Color.White,
                                    strokeWidth = 2.dp
                                )
                            } else {
                                Icon(
                                    imageVector = Icons.Outlined.CheckCircle,
                                    contentDescription = null,
                                    tint = Color.White,
                                    modifier = Modifier.size(22.dp)
                                )
                                Spacer(Modifier.width(10.dp))
                                Text(
                                    text = "Tomar Ahora",
                                    fontSize = 17.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color.White
                                )
                            }
                        }

                        Spacer(Modifier.height(12.dp))

                        // 2. Botón Posponer 30 min (>= 56dp)
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
                                .heightIn(min = 58.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.AccessAlarm,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(Modifier.width(10.dp))
                            Text(
                                text = "Posponer 30 min",
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold,
                                color = TealPrimary
                            )
                        }

                        Spacer(Modifier.height(8.dp))

                        // 3. Botón Omitir Toma (>= 56dp)
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
                                text = "Omitir Toma",
                                fontSize = 15.5.sp,
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
