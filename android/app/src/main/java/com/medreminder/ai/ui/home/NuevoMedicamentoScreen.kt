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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material.icons.outlined.AccessTime
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Inventory2
import androidx.compose.material.icons.automirrored.outlined.Label
import androidx.compose.material.icons.outlined.MedicalInformation
import androidx.compose.material.icons.outlined.MedicalServices
import androidx.compose.material.icons.outlined.Medication
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Scale
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Vaccines
import androidx.compose.material.icons.outlined.WaterDrop
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
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

/**
 * Pantalla 5: Registrar Medicamento (Formulario clínico con Forma farmacéutica,
 * Nombre, Dosis con chips de sugerencia, Frecuencia con chips, Stock +/- y Guardar).
 */
@Composable
fun NuevoMedicamentoScreen(
    form: NuevoMedicamentoFormState,
    snackbarHostState: SnackbarHostState,
    onBack: () -> Unit,
    onFormaChange: (FormaFarmaceutica) -> Unit,
    onNombreChange: (String) -> Unit,
    onDosisChange: (String) -> Unit,
    onFrecuenciaTextoChange: (String) -> Unit,
    onSelectFrecuenciaChip: (Int, String) -> Unit,
    onStockTextoChange: (String) -> Unit,
    onIncrementStock: (Int) -> Unit,
    onGuardar: () -> Unit
) {
    Scaffold(
        containerColor = AppBackground,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            Column(modifier = Modifier.background(AppBackground)) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = onBack, enabled = !form.isSubmitting) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Volver",
                            tint = TextPrimary
                        )
                    }
                    MedBrandLogo(size = 36.dp, cornerRadius = 10.dp)
                    Spacer(Modifier.width(10.dp))
                    Text(
                        text = "Registrar Medicamento",
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
                HorizontalDivider(color = InputBorderColor, thickness = 1.dp)
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 18.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 1. Tarjeta de encabezado "REGISTRO CLÍNICO - Nuevo Medicamento"
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
                    color = SoftWarmSurface,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Surface(
                                shape = RoundedCornerShape(50),
                                color = TealBadgeBg
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.MedicalInformation,
                                        contentDescription = null,
                                        tint = TealBadgeText,
                                        modifier = Modifier.size(14.dp)
                                    )
                                    Spacer(Modifier.width(6.dp))
                                    Text(
                                        text = "REGISTRO CLÍNICO",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        letterSpacing = 0.6.sp,
                                        color = TealBadgeText
                                    )
                                }
                            }
                            Surface(
                                shape = CircleShape,
                                color = Color(0xFFE9E7E4),
                                modifier = Modifier
                                    .size(38.dp)
                                    .clip(CircleShape)
                                    .clickable(enabled = !form.isSubmitting) { onBack() }
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = Icons.Default.Close,
                                        contentDescription = "Cerrar",
                                        tint = TextPrimary,
                                        modifier = Modifier.size(18.dp)
                                    )
                                }
                            }
                        }
                        Spacer(Modifier.height(12.dp))
                        Text(
                            text = "Nuevo Medicamento",
                            fontSize = 26.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(6.dp))
                        Text(
                            text = "Ingresa los datos del envase o receta médica para sincronizar alertas.",
                            fontSize = 14.sp,
                            color = TextSecondary,
                            lineHeight = 20.sp
                        )
                    }
                }
            }

            // 2. Tarjeta Forma farmacéutica
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(18.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(14.dp),
                            color = TealSoftBg,
                            modifier = Modifier.size(48.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.MedicalInformation,
                                    contentDescription = null,
                                    tint = TealDark,
                                    modifier = Modifier.size(24.dp)
                                )
                            }
                        }
                        Spacer(Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Forma\nfarmacéutica",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = TextPrimary,
                                lineHeight = 19.sp
                            )
                            Spacer(Modifier.height(2.dp))
                            Text(
                                text = form.forma.label,
                                fontSize = 12.sp,
                                color = TextSecondary
                            )
                        }
                        Spacer(Modifier.width(8.dp))
                        Surface(
                            shape = RoundedCornerShape(16.dp),
                            color = SoftWarmSurface
                        ) {
                            Row(
                                modifier = Modifier.padding(4.dp),
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                FormaToggleButton(
                                    selected = form.forma == FormaFarmaceutica.COMPRIMIDOS,
                                    icon = Icons.Outlined.Medication,
                                    onClick = { onFormaChange(FormaFarmaceutica.COMPRIMIDOS) }
                                )
                                FormaToggleButton(
                                    selected = form.forma == FormaFarmaceutica.GOTAS,
                                    icon = Icons.Outlined.WaterDrop,
                                    onClick = { onFormaChange(FormaFarmaceutica.GOTAS) }
                                )
                                FormaToggleButton(
                                    selected = form.forma == FormaFarmaceutica.INYECTABLE,
                                    icon = Icons.Outlined.Vaccines,
                                    onClick = { onFormaChange(FormaFarmaceutica.INYECTABLE) }
                                )
                            }
                        }
                    }
                }
            }

            // 3. Tarjeta Nombre del medicamento (* Requerido)
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
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
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Outlined.Label,
                                    contentDescription = null,
                                    tint = TealPrimary,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = "Nombre del medicamento",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                            }
                            Text(
                                text = "* Requerido",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold,
                                color = AlertRedText
                            )
                        }
                        Spacer(Modifier.height(12.dp))
                        SoftCardInputField(
                            value = form.nombre,
                            onValueChange = onNombreChange,
                            placeholder = "ej. Ibuprofeno, Paracetamol",
                            error = form.nombreError,
                            enabled = !form.isSubmitting
                        )
                    }
                }
            }

            // 4. Tarjeta Dosis + chips de sugerencia ("500 mg", "1 comp.", "10 ml")
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
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
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Text(
                                text = "Sugerencias:",
                                fontSize = 12.5.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = TextSecondary
                            )
                            SuggestionChipPill(
                                text = "500 mg",
                                selected = form.dosis == "500 mg",
                                onClick = { onDosisChange("500 mg") }
                            )
                            SuggestionChipPill(
                                text = "1 comp.",
                                selected = form.dosis == "1 comprimido",
                                onClick = { onDosisChange("1 comprimido") }
                            )
                            SuggestionChipPill(
                                text = "10 ml",
                                selected = form.dosis == "10 ml",
                                onClick = { onDosisChange("10 ml") }
                            )
                        }
                    }
                }
            }

            // 5. Tarjeta Frecuencia + chips ("Cada 8h", "Cada 12h", "1 vez al día")
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
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
                                text = "Frecuencia",
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
                        Spacer(Modifier.height(12.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
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
                    }
                }
            }

            // 6. Tarjeta Cantidad Inicial en envase + Stepper (- / +)
            item {
                Surface(
                    shape = RoundedCornerShape(22.dp),
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
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Outlined.Inventory2,
                                    contentDescription = null,
                                    tint = TealPrimary,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = "Cantidad Inicial en\nenvase",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary,
                                    lineHeight = 19.sp
                                )
                            }
                            Text(
                                text = "Control de\nstock",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = TextSecondary,
                                lineHeight = 15.sp
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
                                    placeholder = "ej. 30 pastillas",
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

            // 7. Banner Recordatorios inteligentes
            item {
                Surface(
                    shape = RoundedCornerShape(18.dp),
                    color = SoftWarmSurface,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Shield,
                            contentDescription = null,
                            tint = TealPrimary,
                            modifier = Modifier.size(22.dp)
                        )
                        Spacer(Modifier.width(12.dp))
                        Column {
                            Text(
                                text = "Recordatorios inteligentes",
                                fontSize = 14.5.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary
                            )
                            Spacer(Modifier.height(3.dp))
                            Text(
                                text = "Calcularemos el reabastecimiento automáticamente con base en tu posología programada.",
                                fontSize = 13.sp,
                                color = TextSecondary,
                                lineHeight = 18.sp
                            )
                        }
                    }
                }
            }

            // 8. Botón Guardar Medicamento (>= 56dp)
            item {
                Button(
                    onClick = onGuardar,
                    enabled = !form.isSubmitting,
                    shape = RoundedCornerShape(18.dp),
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
                Spacer(Modifier.height(16.dp))
            }
        }
    }
}

@Composable
private fun FormaToggleButton(
    selected: Boolean,
    icon: ImageVector,
    onClick: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = if (selected) TealPrimary else Color.Transparent,
        modifier = Modifier
            .size(44.dp)
            .clip(RoundedCornerShape(12.dp))
            .clickable { onClick() }
    ) {
        Box(contentAlignment = Alignment.Center) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = if (selected) Color.White else TextPrimary,
                modifier = Modifier.size(20.dp)
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
        shape = RoundedCornerShape(50),
        color = if (selected) TealPrimary else TealBadgeBg,
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .clickable { onClick() }
    ) {
        Text(
            text = text,
            fontSize = 12.5.sp,
            fontWeight = FontWeight.Bold,
            color = if (selected) Color.White else TealBadgeText,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp)
        )
    }
}

@Composable
private fun StockStepperButton(
    icon: ImageVector,
    contentDescription: String,
    onClick: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = CardBackground,
        modifier = Modifier
            .size(48.dp)
            .clip(RoundedCornerShape(12.dp))
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
                    fontSize = 15.sp
                )
            },
            singleLine = true,
            enabled = enabled,
            isError = error != null,
            keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
            shape = RoundedCornerShape(16.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = SoftWarmSurface,
                unfocusedContainerColor = SoftWarmSurface,
                disabledContainerColor = SoftWarmSurface,
                focusedBorderColor = TealPrimary,
                unfocusedBorderColor = Color.Transparent,
                disabledBorderColor = Color.Transparent
            ),
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 56.dp)
        )
        if (error != null) {
            Text(
                text = error,
                color = MaterialTheme.colorScheme.error,
                fontSize = 12.sp,
                modifier = Modifier.padding(start = 8.dp, top = 4.dp)
            )
        }
    }
}
