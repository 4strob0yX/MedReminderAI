package com.medreminder.ai.ui.home

import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.Label
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material.icons.outlined.AccessAlarm
import androidx.compose.material.icons.outlined.AccessTime
import androidx.compose.material.icons.outlined.CalendarMonth
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Inventory2
import androidx.compose.material.icons.outlined.MedicalInformation
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.NotificationImportant
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material.icons.outlined.Restaurant
import androidx.compose.material.icons.outlined.Scale
import androidx.compose.material.icons.outlined.Vaccines
import androidx.compose.material.icons.outlined.Warning
import androidx.compose.material.icons.outlined.WaterDrop
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.data.remote.MedicamentoCatalogoItemDto
import com.medreminder.ai.ui.components.MedBrandLogo
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.AppBackground
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealBadgeText
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import com.medreminder.ai.ui.theme.TealSoftBg
import com.medreminder.ai.ui.theme.TextMuted
import com.medreminder.ai.ui.theme.TextPrimary
import com.medreminder.ai.ui.theme.TextSecondary

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun NuevoMedicamentoScreen(
    form: NuevoMedicamentoFormState,
    snackbarHostState: SnackbarHostState,
    onBack: () -> Unit,
    onFormaChange: (FormaFarmaceutica) -> Unit,
    onColorPastillaChange: (String) -> Unit = {},
    onNombreChange: (String) -> Unit,
    onSelectCatalogoSugerencia: (MedicamentoCatalogoItemDto) -> Unit,
    onDosisChange: (String) -> Unit,
    onFrecuenciaTextoChange: (String) -> Unit,
    onSelectFrecuenciaChip: (Int, String) -> Unit,
    onHoraPrimeraTomaChange: (String) -> Unit = {},
    onDuracionChange: (String, Int?) -> Unit = { _, _ -> },
    onInstruccionesTomaChange: (String) -> Unit = {},
    onStockTextoChange: (String) -> Unit,
    onIncrementStock: (Int) -> Unit,
    onTogglePermitePosponer: (Boolean) -> Unit,
    onToggleEsCritico: (Boolean) -> Unit,
    onContraindicacionesChange: (String) -> Unit,
    onDismissRiesgoModal: () -> Unit = {},
    onGuardar: () -> Unit,
    onConfirmarGuardarConRiesgo: () -> Unit = onGuardar
) {
    Scaffold(
        containerColor = AppBackground,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            Column(
                modifier = Modifier
                    .background(AppBackground)
                    .statusBarsPadding()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 14.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(
                        onClick = onBack,
                        enabled = !form.isSubmitting,
                        modifier = Modifier.size(48.dp)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Volver",
                            tint = TextPrimary
                        )
                    }
                    Spacer(Modifier.width(4.dp))
                    MedBrandLogo(size = 38.dp, cornerRadius = 12.dp)
                    Spacer(Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "REGISTRO CLÍNICO",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.ExtraBold,
                            letterSpacing = 0.7.sp,
                            color = TealDark
                        )
                        Text(
                            text = "Nuevo Medicamento",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary
                        )
                    }
                }
                HorizontalDivider(color = InputBorderColor, thickness = 1.dp)
            }
        },
        bottomBar = {
            Surface(
                color = CardBackground,
                shadowElevation = 10.dp
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .navigationBarsPadding()
                        .padding(horizontal = 20.dp, vertical = 12.dp)
                ) {
                    Button(
                        onClick = onGuardar,
                        enabled = !form.isSubmitting,
                        shape = RoundedCornerShape(20.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 60.dp)
                    ) {
                        if (form.isSubmitting) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(24.dp),
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
                                text = "Guardar Medicamento",
                                fontSize = 17.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color.White
                            )
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 1. Subtítulo amigable sin botones de cierre duplicados
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
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
                            modifier = Modifier.size(42.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.MedicalInformation,
                                    contentDescription = null,
                                    tint = TealDark,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                        }
                        Spacer(Modifier.width(12.dp))
                        Text(
                            text = "Escribe el nombre para autocompletar dosis, verificar alergias e identificar visualmente tu medicamento.",
                            fontSize = 13.5.sp,
                            color = TextSecondary,
                            lineHeight = 19.sp
                        )
                    }
                }
            }

            // 2. Alerta de Alergia o Interacción detectada
            if (form.alertaAlergia != null || form.alertaInteraccion != null) {
                item {
                    Surface(
                        shape = RoundedCornerShape(22.dp),
                        color = Color(0xFFFFEBEE),
                        border = BorderStroke(1.5.dp, Color(0xFFD32F2F)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.Top
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Warning,
                                contentDescription = null,
                                tint = Color(0xFFD32F2F),
                                modifier = Modifier.size(26.dp)
                            )
                            Spacer(Modifier.width(12.dp))
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text(
                                    text = "ALERTA CLÍNICA DE SEGURIDAD",
                                    fontWeight = FontWeight.ExtraBold,
                                    fontSize = 13.sp,
                                    color = Color(0xFFB71C1C)
                                )
                                form.alertaAlergia?.let { alerta ->
                                    Text(
                                        text = "• Alergia: $alerta",
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        color = Color(0xFFC62828),
                                        lineHeight = 18.sp
                                    )
                                }
                                form.alertaInteraccion?.let { interaccion ->
                                    Text(
                                        text = "• Interacción: $interaccion",
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        color = Color(0xFFC62828),
                                        lineHeight = 18.sp
                                    )
                                }
                            }
                        }
                    }
                }
            }

            // 3. Forma farmacéutica (botones grandes >= 60dp con alto contraste y etiqueta explícita)
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.MedicalInformation,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Column {
                                Text(
                                    text = "Forma farmacéutica",
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = TextPrimary
                                )
                                Text(
                                    text = form.forma.label,
                                    fontSize = 12.5.sp,
                                    color = TextSecondary
                                )
                            }
                        }
                        Spacer(Modifier.height(14.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            FormaToggleButton(
                                selected = form.forma == FormaFarmaceutica.COMPRIMIDOS,
                                label = "Pastilla",
                                icon = Icons.Outlined.Medication,
                                onClick = { onFormaChange(FormaFarmaceutica.COMPRIMIDOS) },
                                modifier = Modifier.weight(1f)
                            )
                            FormaToggleButton(
                                selected = form.forma == FormaFarmaceutica.GOTAS,
                                label = "Gotas",
                                icon = Icons.Outlined.WaterDrop,
                                onClick = { onFormaChange(FormaFarmaceutica.GOTAS) },
                                modifier = Modifier.weight(1f)
                            )
                            FormaToggleButton(
                                selected = form.forma == FormaFarmaceutica.INYECTABLE,
                                label = "Inyección",
                                icon = Icons.Outlined.Vaccines,
                                onClick = { onFormaChange(FormaFarmaceutica.INYECTABLE) },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }

            // 4. Selector de Color Visual de Pastilla / Envase (para el Check Visual Rápido)
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.Palette,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Column {
                                Text(
                                    text = "Color distintivo para verificación visual",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = TextPrimary
                                )
                                Text(
                                    text = "Te ayudará a confirmar que tienes el medicamento correcto al tomarlo",
                                    fontSize = 12.sp,
                                    color = TextSecondary
                                )
                            }
                        }
                        Spacer(Modifier.height(12.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            PILL_COLOR_OPTIONS.forEach { option ->
                                val selected = form.colorPastilla.equals(option.key, ignoreCase = true)
                                Surface(
                                    shape = RoundedCornerShape(14.dp),
                                    color = if (selected) option.containerBg else SoftWarmSurface,
                                    border = BorderStroke(
                                        width = if (selected) 2.dp else 1.dp,
                                        color = if (selected) option.iconTint else InputBorderColor
                                    ),
                                    modifier = Modifier
                                        .heightIn(min = 44.dp)
                                        .clip(RoundedCornerShape(14.dp))
                                        .clickable { onColorPastillaChange(option.key) }
                                ) {
                                    Row(
                                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .size(14.dp)
                                                .clip(CircleShape)
                                                .background(option.dotColor)
                                        )
                                        Spacer(Modifier.width(6.dp))
                                        Text(
                                            text = option.label,
                                            fontSize = 12.5.sp,
                                            fontWeight = if (selected) FontWeight.ExtraBold else FontWeight.SemiBold,
                                            color = TextPrimary
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // 5. Nombre del medicamento + AUTOCOMPLETADO
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(
                                modifier = Modifier.weight(1f, fill = false),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Outlined.Label,
                                    contentDescription = null,
                                    tint = TealPrimary,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = "Medicamento",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            }
                            Spacer(Modifier.width(8.dp))
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = TealSoftBg
                            ) {
                                Text(
                                    text = "Sugerencias IA",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TealPrimary,
                                    maxLines = 1,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }
                        }
                        Spacer(Modifier.height(12.dp))
                        SoftCardInputField(
                            value = form.nombre,
                            onValueChange = onNombreChange,
                            placeholder = "ej. Paracetamol, Amoxicilina, Losartán...",
                            error = form.nombreError,
                            enabled = !form.isSubmitting
                        )

                        // Desplegable de sugerencias de autocompletado
                        if (form.catalogoSugerencias.isNotEmpty()) {
                            Spacer(Modifier.height(10.dp))
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = Color(0xFFF7FAFA),
                                border = BorderStroke(1.dp, TealSoftBg),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Column(
                                    modifier = Modifier.padding(10.dp),
                                    verticalArrangement = Arrangement.spacedBy(6.dp)
                                ) {
                                    Text(
                                        text = "SUGERENCIAS CLÍNICAS (TOCA PARA APLICAR):",
                                        fontSize = 10.5.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = TealDark,
                                        letterSpacing = 0.5.sp
                                    )
                                    form.catalogoSugerencias.take(4).forEach { item ->
                                        Surface(
                                            shape = RoundedCornerShape(12.dp),
                                            color = Color.White,
                                            border = BorderStroke(1.dp, Color(0xFFE8ECEB)),
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clickable { onSelectCatalogoSugerencia(item) }
                                        ) {
                                            Row(
                                                modifier = Modifier.padding(12.dp),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Icon(
                                                    imageVector = Icons.Outlined.Medication,
                                                    contentDescription = null,
                                                    tint = TealPrimary,
                                                    modifier = Modifier.size(20.dp)
                                                )
                                                Spacer(Modifier.width(10.dp))
                                                Column(modifier = Modifier.weight(1f)) {
                                                    Text(
                                                        text = item.nombre,
                                                        fontWeight = FontWeight.Bold,
                                                        fontSize = 13.5.sp,
                                                        color = TextPrimary
                                                    )
                                                    Text(
                                                        text = "Activo: ${item.principioActivo} • ${item.dosisSugerida}",
                                                        fontSize = 11.5.sp,
                                                        color = TextSecondary
                                                    )
                                                }
                                                if (item.esCriticoDefecto) {
                                                    Surface(
                                                        shape = RoundedCornerShape(6.dp),
                                                        color = Color(0xFFFFEBEE)
                                                    ) {
                                                        Text(
                                                            text = "CRÍTICO",
                                                            color = Color(0xFFD32F2F),
                                                            fontSize = 9.sp,
                                                            fontWeight = FontWeight.ExtraBold,
                                                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                                        )
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // 6. Contraindicaciones conocidas del fármaco
            if (form.contraindicaciones.isNotBlank()) {
                item {
                    Surface(
                        shape = RoundedCornerShape(18.dp),
                        color = Color(0xFFFFF8E1),
                        border = BorderStroke(1.dp, Color(0xFFFFE082)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.Top) {
                            Icon(
                                imageVector = Icons.Outlined.Info,
                                contentDescription = null,
                                tint = Color(0xFFF57F17),
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(Modifier.width(10.dp))
                            Column {
                                Text(
                                    text = "Contraindicaciones clínicas conocidas",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 13.sp,
                                    color = Color(0xFFE65100)
                                )
                                Spacer(Modifier.height(3.dp))
                                Text(
                                    text = form.contraindicaciones,
                                    fontSize = 12.sp,
                                    color = Color(0xFF5D4037),
                                    lineHeight = 17.sp
                                )
                            }
                        }
                    }
                }
            }

            // 7. Medicamento Crítico / Imposible de Posponer (Toggle Clínico)
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = if (form.esCritico) Color(0xFFFFF5F5) else CardBackground,
                    border = BorderStroke(1.5.dp, if (form.esCritico) Color(0xFFE57373) else InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(18.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(14.dp),
                            color = if (form.esCritico) Color(0xFFFFCDD2) else TealSoftBg,
                            modifier = Modifier.size(48.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = if (form.esCritico) Icons.Outlined.NotificationImportant else Icons.Outlined.AccessAlarm,
                                    contentDescription = null,
                                    tint = if (form.esCritico) Color(0xFFD32F2F) else TealDark,
                                    modifier = Modifier.size(24.dp)
                                )
                            }
                        }
                        Spacer(Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Medicamento crítico",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (form.esCritico) Color(0xFFB71C1C) else TextPrimary
                            )
                            Text(
                                text = if (form.esCritico) "Dosis estricta: PROHIBIDO posponer u omitir la toma" else "Permite posponer la toma si es necesario",
                                fontSize = 12.sp,
                                color = if (form.esCritico) Color(0xFFD32F2F) else TextSecondary
                            )
                        }
                        Switch(
                            checked = form.esCritico,
                            onCheckedChange = { onToggleEsCritico(it) },
                            colors = SwitchDefaults.colors(
                                checkedThumbColor = Color.White,
                                checkedTrackColor = Color(0xFFD32F2F)
                            )
                        )
                    }
                }
            }

            // 8. Dosis + chips
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.Scale,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = "Dosis",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        }
                        Spacer(Modifier.height(12.dp))
                        SoftCardInputField(
                            value = form.dosis,
                            onValueChange = onDosisChange,
                            placeholder = "ej. 400 mg o 1 comprimido",
                            error = form.dosisError,
                            enabled = !form.isSubmitting
                        )
                        Spacer(Modifier.height(12.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            SuggestionChipPill(
                                text = "500 mg",
                                selected = form.dosis == "500 mg",
                                onClick = { onDosisChange("500 mg") }
                            )
                            SuggestionChipPill(
                                text = "1 comprimido",
                                selected = form.dosis == "1 comprimido",
                                onClick = { onDosisChange("1 comprimido") }
                            )
                            SuggestionChipPill(
                                text = "10 ml",
                                selected = form.dosis == "10 ml",
                                onClick = { onDosisChange("10 ml") }
                            )
                            SuggestionChipPill(
                                text = "1 ampolla",
                                selected = form.dosis == "1 ampolla",
                                onClick = { onDosisChange("1 ampolla") }
                            )
                        }
                    }
                }
            }

            // 9. Indicación de Toma (Con alimentos, En ayunas, Con abundante agua, Antes de dormir)
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.Restaurant,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = "Indicación de Toma",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        }
                        Spacer(Modifier.height(12.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            listOf(
                                "Con alimentos",
                                "En ayunas",
                                "Con abundante agua",
                                "Antes de dormir"
                            ).forEach { indicacion ->
                                SuggestionChipPill(
                                    text = indicacion,
                                    selected = form.instruccionesToma == indicacion,
                                    onClick = { onInstruccionesTomaChange(indicacion) }
                                )
                            }
                        }
                    }
                }
            }

            // 10. Frecuencia + Selector de Hora de 1ª Toma + Duración del Tratamiento
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.AccessTime,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = "Frecuencia y Horario",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        }
                        Spacer(Modifier.height(12.dp))
                        SoftCardInputField(
                            value = form.frecuenciaTexto,
                            onValueChange = onFrecuenciaTextoChange,
                            placeholder = "ej. Cada 8 horas",
                            error = null,
                            enabled = !form.isSubmitting
                        )
                        Spacer(Modifier.height(10.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            SuggestionChipPill(
                                text = "Cada 6h",
                                selected = form.frecuenciaHoras == 6,
                                onClick = { onSelectFrecuenciaChip(6, "Cada 6 horas") }
                            )
                            SuggestionChipPill(
                                text = "Cada 8h",
                                selected = form.frecuenciaHoras == 8,
                                onClick = { onSelectFrecuenciaChip(8, "Cada 8 horas") }
                            )
                            SuggestionChipPill(
                                text = "Cada 12h",
                                selected = form.frecuenciaHoras == 12,
                                onClick = { onSelectFrecuenciaChip(12, "Cada 12 horas") }
                            )
                            SuggestionChipPill(
                                text = "1 vez al día",
                                selected = form.frecuenciaHoras == 24,
                                onClick = { onSelectFrecuenciaChip(24, "1 vez al día") }
                            )
                        }

                        Spacer(Modifier.height(16.dp))
                        HorizontalDivider(color = InputBorderColor, thickness = 1.dp)
                        Spacer(Modifier.height(14.dp))

                        Text(
                            text = "Hora de 1ª toma:",
                            fontSize = 13.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(8.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            listOf("08:00 AM", "02:00 PM", "09:00 PM", "Ahora").forEach { hora ->
                                SuggestionChipPill(
                                    text = hora,
                                    selected = form.horaPrimeraToma == hora,
                                    onClick = { onHoraPrimeraTomaChange(hora) }
                                )
                            }
                        }

                        Spacer(Modifier.height(14.dp))

                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Outlined.CalendarMonth,
                                contentDescription = null,
                                tint = TealPrimary,
                                modifier = Modifier.size(17.dp)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                text = "Duración del tratamiento:",
                                fontSize = 13.5.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                        }
                        Spacer(Modifier.height(8.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            listOf(
                                "Crónico / Continuo" to null,
                                "7 días" to 7,
                                "14 días" to 14,
                                "30 días" to 30
                            ).forEach { (etiqueta, dias) ->
                                SuggestionChipPill(
                                    text = etiqueta,
                                    selected = form.duracionTratamiento == etiqueta,
                                    onClick = { onDuracionChange(etiqueta, dias) }
                                )
                            }
                        }
                    }
                }
            }

            // 11. Cantidad inicial en envase (sin saltos de línea forzados)
            item {
                Surface(
                    shape = RoundedCornerShape(24.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        FlowRow(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalArrangement = Arrangement.spacedBy(4.dp)
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.Inventory2,
                                    contentDescription = null,
                                    tint = TealPrimary,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = "Cantidad inicial en envase",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            }
                            Text(
                                text = "Control de stock",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = TextSecondary
                            )
                        }
                        Spacer(Modifier.height(12.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            Box(modifier = Modifier.weight(1f)) {
                                SoftCardInputField(
                                    value = form.cantidadStockTexto,
                                    onValueChange = onStockTextoChange,
                                    placeholder = "ej. 30 ${form.forma.unitPlural}",
                                    error = null,
                                    enabled = !form.isSubmitting,
                                    keyboardType = KeyboardType.Number
                                )
                            }
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = SoftWarmSurface
                            ) {
                                Row(
                                    modifier = Modifier.padding(4.dp),
                                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                                ) {
                                    StockStepperButton(
                                        icon = Icons.Default.Remove,
                                        contentDescription = "Disminuir stock",
                                        onClick = { onIncrementStock(-1) }
                                    )
                                    StockStepperButton(
                                        icon = Icons.Default.Add,
                                        contentDescription = "Aumentar stock",
                                        onClick = { onIncrementStock(1) }
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }

        // Diálogo de confirmación explícita si hay alerta de alergia o interacción farmacológica
        if (form.showConfirmacionRiesgoModal) {
            ConfirmacionRiesgoClinicoDialog(
                nombreMedicamento = form.nombre,
                alertaAlergia = form.alertaAlergia,
                alertaInteraccion = form.alertaInteraccion,
                onDismiss = onDismissRiesgoModal,
                onConfirm = onConfirmarGuardarConRiesgo
            )
        }
    }
}

@Composable
private fun FormaToggleButton(
    selected: Boolean,
    label: String,
    icon: ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        shape = RoundedCornerShape(18.dp),
        color = if (selected) TealPrimary else SoftWarmSurface,
        border = BorderStroke(
            width = if (selected) 2.dp else 1.dp,
            color = if (selected) TealPrimary else InputBorderColor
        ),
        modifier = modifier
            .heightIn(min = 68.dp)
            .clip(RoundedCornerShape(18.dp))
            .clickable { onClick() }
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = label,
                tint = if (selected) Color.White else TealDark,
                modifier = Modifier.size(24.dp)
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = label,
                fontSize = 12.sp,
                fontWeight = FontWeight.ExtraBold,
                color = if (selected) Color.White else TextPrimary,
                maxLines = 2,
                textAlign = TextAlign.Center,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun ConfirmacionRiesgoClinicoDialog(
    nombreMedicamento: String,
    alertaAlergia: String?,
    alertaInteraccion: String?,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(
            shape = RoundedCornerShape(26.dp),
            color = CardBackground,
            shadowElevation = 12.dp,
            modifier = Modifier
                .fillMaxWidth(0.92f)
                .padding(16.dp)
        ) {
            Column(
                modifier = Modifier
                    .padding(22.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(
                        shape = CircleShape,
                        color = Color(0xFFFFEBEE),
                        modifier = Modifier.size(44.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Outlined.Warning,
                                contentDescription = null,
                                tint = Color(0xFFD32F2F),
                                modifier = Modifier.size(24.dp)
                            )
                        }
                    }
                    Spacer(Modifier.width(12.dp))
                    Text(
                        text = "Riesgo Clínico Detectado",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color(0xFFB71C1C)
                    )
                }

                Spacer(Modifier.height(12.dp))
                Text(
                    text = "Se detectó una advertencia importante para '$nombreMedicamento':",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = TextPrimary
                )
                Spacer(Modifier.height(8.dp))

                alertaAlergia?.let {
                    Text(
                        text = "Alerta: $it",
                        fontSize = 13.sp,
                        color = Color(0xFFC62828),
                        lineHeight = 18.sp
                    )
                    Spacer(Modifier.height(6.dp))
                }
                alertaInteraccion?.let {
                    Text(
                        text = "Alerta: $it",
                        fontSize = 13.sp,
                        color = Color(0xFFC62828),
                        lineHeight = 18.sp
                    )
                    Spacer(Modifier.height(6.dp))
                }

                Text(
                    text = "¿Confirmas que tu médico tratante autorizó este medicamento?",
                    fontSize = 13.sp,
                    color = TextSecondary
                )

                Spacer(Modifier.height(18.dp))
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
                        onClick = onConfirm,
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFC62828)),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 52.dp)
                    ) {
                        Text("Sí, Autorizado", fontWeight = FontWeight.Bold, color = Color.White)
                    }
                }
            }
        }
    }
}

@Composable
private fun SoftCardInputField(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String,
    error: String?,
    enabled: Boolean,
    keyboardType: KeyboardType = KeyboardType.Text
) {
    Column {
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            placeholder = {
                Text(
                    text = placeholder,
                    color = TextMuted,
                    fontSize = 14.sp
                )
            },
            singleLine = true,
            enabled = enabled,
            keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
            shape = RoundedCornerShape(16.dp),
            isError = error != null,
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = SoftWarmSurface,
                unfocusedContainerColor = SoftWarmSurface,
                disabledContainerColor = SoftWarmSurface,
                focusedBorderColor = TealPrimary,
                unfocusedBorderColor = Color.Transparent,
                errorBorderColor = AlertRedText
            ),
            modifier = Modifier.fillMaxWidth()
        )
        if (error != null) {
            Spacer(Modifier.height(4.dp))
            Text(
                text = error,
                color = AlertRedText,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.padding(start = 6.dp)
            )
        }
    }
}

@Composable
private fun SuggestionChipPill(
    text: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(14.dp),
        color = if (selected) TealDark else SoftWarmSurface,
        border = if (selected) null else BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier
            .heightIn(min = 40.dp)
            .clip(RoundedCornerShape(14.dp))
            .clickable { onClick() }
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = text,
                fontSize = 12.5.sp,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.SemiBold,
                color = if (selected) Color.White else TextPrimary
            )
        }
    }
}

@Composable
private fun StockStepperButton(
    icon: ImageVector,
    contentDescription: String,
    onClick: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(14.dp),
        color = Color.White,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier
            .size(48.dp)
            .clip(RoundedCornerShape(14.dp))
            .clickable { onClick() }
    ) {
        Box(contentAlignment = Alignment.Center) {
            Icon(
                imageVector = icon,
                contentDescription = contentDescription,
                tint = TextPrimary,
                modifier = Modifier.size(20.dp)
            )
        }
    }
}

