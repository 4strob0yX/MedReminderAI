package com.medreminder.ai.ui.home

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.util.Base64
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.CameraAlt
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.PhotoLibrary
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.WarningAmber
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
import com.medreminder.ai.ui.theme.ThemeMode
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import java.io.ByteArrayOutputStream
import kotlin.coroutines.resume
import kotlin.math.max

private const val RECETA_EJEMPLO_1 =
    "Dra. Elena Vargas - Medicina Interna (Ced. 482910)\n" +
    "1) Amoxicilina 500 mg cápsulas: tomar 1 cada 8 horas por 7 días después de los alimentos.\n" +
    "2) Paracetamol 500 mg tabletas: tomar 1 cada 8 horas por 5 días en caso de fiebre o dolor."

private const val RECETA_EJEMPLO_2 =
    "Dr. Roberto Gómez - Cardiometabolismo (Ced. 719304)\n" +
    "1) Metformina 850 mg tabletas: tomar 1 cada 12 horas por 30 días con los alimentos.\n" +
    "2) Atorvastatina 20 mg comprimidos: tomar 1 cada 24 horas por 30 días por la noche."

@Composable
fun ConfirmarRecetaScreen(
    state: HomeUiState,
    onBack: () -> Unit,
    onAnalizarReceta: (textoReceta: String?, imageBase64: String?) -> Unit,
    onActualizarItem: (index: Int, item: EditablePrescriptionItem) -> Unit,
    onConfirmarGuardar: () -> Unit
) {
    val accTheme = LocalAccessibilitySettings.current
    val isNight = accTheme.themeMode == ThemeMode.ALTO_CONTRASTE_NOCHE
    val bgPrimary = if (isNight) Color(0xFF0A1417) else Color(0xFFF3F8F9)
    val surfaceColor = if (isNight) Color(0xFF122227) else Color.White
    val textPrimary = if (isNight) Color(0xFFF1F7F8) else Color(0xFF102A32)
    val textSecondary = if (isNight) Color(0xFFA9C3C9) else Color(0xFF4A6670)
    val tealPrimary = Color(0xFF006D77)
    val borderLight = if (isNight) Color(0xFF233B43) else Color(0xFFDCE8EB)

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var textoOcrEditable by remember { mutableStateOf("") }
    var fotoCapturadaLabel by remember { mutableStateOf<String?>(null) }
    var isRunningOcr by remember { mutableStateOf(false) }

    fun procesarBitmapReceta(rawBitmap: Bitmap, origenLabel: String) {
        scope.launch {
            isRunningOcr = true
            fotoCapturadaLabel = "$origenLabel • Ejecutando OCR en dispositivo..."
            val (ocrText, b64, dims) = withContext(Dispatchers.Default) {
                val scaled = scaleBitmapForOcr(rawBitmap)
                val recognized = runMlKitOcr(scaled).trim()
                val encoded = encodeBitmapJpegBase64(scaled)
                Triple(recognized, encoded, "${scaled.width}x${scaled.height} px")
            }
            isRunningOcr = false
            // Limpiamos cualquier texto anterior/demo para no contaminar el escaneo real
            textoOcrEditable = ocrText
            fotoCapturadaLabel = if (ocrText.isNotBlank()) {
                "$origenLabel ($dims) • OCR detectó ${ocrText.length} caracteres"
            } else {
                "$origenLabel ($dims) • Sin texto legible por OCR, enviando imagen a IA"
            }
            onAnalizarReceta(ocrText.ifBlank { null }, b64)
        }
    }

    val cameraLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicturePreview()
    ) { bitmap: Bitmap? ->
        if (bitmap != null) {
            procesarBitmapReceta(bitmap, "Foto capturada")
        }
    }

    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            scope.launch {
                val bitmap = withContext(Dispatchers.IO) {
                    decodeBitmapFromUri(context, uri)
                }
                if (bitmap != null) {
                    procesarBitmapReceta(bitmap, "Imagen de galería")
                } else {
                    fotoCapturadaLabel = "No se pudo leer la imagen seleccionada"
                }
            }
        }
    }

    val seleccionadosCount = state.itemsRecetaEditables.count { it.seleccionado }

    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .imePadding(),
        containerColor = bgPrimary,
        topBar = {
            Surface(
                color = surfaceColor,
                shadowElevation = 2.dp
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = onBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Volver",
                            tint = textPrimary
                        )
                    }
                    Spacer(Modifier.width(8.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "MOTOR OLLAMA · MEDI-CLINICO",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = tealPrimary,
                            letterSpacing = 0.7.sp
                        )
                        Text(
                            text = "Escanear y Confirmar Receta",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = textPrimary
                        )
                    }
                }
            }
        },
        bottomBar = {
            Surface(
                color = surfaceColor,
                shadowElevation = 10.dp
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .navigationBarsPadding()
                        .padding(horizontal = 20.dp, vertical = 12.dp)
                ) {
                    Button(
                        onClick = onConfirmarGuardar,
                        enabled = seleccionadosCount > 0 && !state.guardandoRecetaMasiva && !state.analizandoRecetaIa,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(54.dp),
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = tealPrimary,
                            contentColor = Color.White
                        )
                    ) {
                        if (state.guardandoRecetaMasiva) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(20.dp),
                                strokeWidth = 2.5.dp,
                                color = Color.White
                            )
                            Spacer(Modifier.width(10.dp))
                            Text(
                                text = "Guardando receta en Mi Botiquín...",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold
                            )
                        } else {
                            Icon(
                                imageVector = Icons.Outlined.CheckCircle,
                                contentDescription = null,
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = "Confirmar y Guardar ($seleccionadosCount Medicamento${if (seleccionadosCount == 1) "" else "s"})",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 14.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            // Card 1: Captura por Cámara, Galería o Receta Médica OCR
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = surfaceColor,
                border = BorderStroke(1.dp, borderLight),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(38.dp)
                                .clip(CircleShape)
                                .background(tealPrimary.copy(alpha = 0.12f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Description,
                                contentDescription = null,
                                tint = tealPrimary,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                        Spacer(Modifier.width(10.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "1. Captura o Texto de Receta Médica",
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                color = textPrimary
                            )
                            Text(
                                text = "Procesado 100% local con tu motor Ollama (medi-clinico)",
                                fontSize = 12.sp,
                                color = textSecondary
                            )
                        }
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        OutlinedButton(
                            onClick = { cameraLauncher.launch(null) },
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp),
                            border = BorderStroke(1.dp, tealPrimary.copy(alpha = 0.5f))
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.CameraAlt,
                                contentDescription = null,
                                tint = tealPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text("Cámara", color = tealPrimary, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                        }
                        OutlinedButton(
                            onClick = { galleryLauncher.launch("image/*") },
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp),
                            border = BorderStroke(1.dp, tealPrimary.copy(alpha = 0.5f))
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.PhotoLibrary,
                                contentDescription = null,
                                tint = tealPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text("Galería", color = tealPrimary, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                        }
                    }

                    if (fotoCapturadaLabel != null) {
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = Color(0xFFE0F2F1)
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                if (isRunningOcr) {
                                    CircularProgressIndicator(
                                        modifier = Modifier.size(14.dp),
                                        strokeWidth = 2.dp,
                                        color = tealPrimary
                                    )
                                    Spacer(Modifier.width(8.dp))
                                }
                                Text(
                                    text = if (isRunningOcr) fotoCapturadaLabel!! else "✓ $fotoCapturadaLabel",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = tealPrimary
                                )
                            }
                        }
                    }

                    // Plantillas opcionales para probar el motor Ollama al instante
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = if (textoOcrEditable == RECETA_EJEMPLO_1) tealPrimary.copy(alpha = 0.14f) else bgPrimary,
                            border = BorderStroke(1.dp, tealPrimary.copy(alpha = 0.35f)),
                            modifier = Modifier
                                .weight(1f)
                                .clickable {
                                    fotoCapturadaLabel = null
                                    textoOcrEditable = RECETA_EJEMPLO_1
                                    onAnalizarReceta(RECETA_EJEMPLO_1, null)
                                }
                        ) {
                            Text(
                                text = "Plantilla 1: Alergia",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = tealPrimary,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp)
                            )
                        }
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = if (textoOcrEditable == RECETA_EJEMPLO_2) tealPrimary.copy(alpha = 0.14f) else bgPrimary,
                            border = BorderStroke(1.dp, tealPrimary.copy(alpha = 0.35f)),
                            modifier = Modifier
                                .weight(1f)
                                .clickable {
                                    fotoCapturadaLabel = null
                                    textoOcrEditable = RECETA_EJEMPLO_2
                                    onAnalizarReceta(RECETA_EJEMPLO_2, null)
                                }
                        ) {
                            Text(
                                text = "Plantilla 2: Cardio",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = tealPrimary,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp)
                            )
                        }
                    }

                    OutlinedTextField(
                        value = textoOcrEditable,
                        onValueChange = { textoOcrEditable = it },
                        label = { Text("Texto de la receta médica (OCR / Editable)") },
                        placeholder = { Text("Toma una foto, elige de galería o escribe/pega la receta aquí...") },
                        minLines = 3,
                        maxLines = 5,
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(14.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = tealPrimary,
                            unfocusedBorderColor = borderLight,
                            focusedTextColor = textPrimary,
                            unfocusedTextColor = textPrimary
                        )
                    )

                    Button(
                        onClick = { onAnalizarReceta(textoOcrEditable, null) },
                        enabled = !state.analizandoRecetaIa && !isRunningOcr && textoOcrEditable.isNotBlank(),
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = tealPrimary,
                            contentColor = Color.White
                        )
                    ) {
                        if (state.analizandoRecetaIa) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(18.dp),
                                strokeWidth = 2.dp,
                                color = Color.White
                            )
                            Spacer(Modifier.width(8.dp))
                            Text("Extrayendo medicamentos con Ollama (medi-clinico)...", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                        } else {
                            Icon(
                                imageVector = Icons.Outlined.AutoAwesome,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text("Analizar Receta con Ollama (medi-clinico)", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                        }
                    }
                }
            }

            // Resumen clínico de extracción
            if (!state.resumenRecetaIa.isNullOrBlank()) {
                Surface(
                    shape = RoundedCornerShape(16.dp),
                    color = if (isNight) Color(0xFF142E35) else Color(0xFFE4F4F6),
                    border = BorderStroke(1.dp, tealPrimary.copy(alpha = 0.4f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier.padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(
                                text = "MÉDICO: ${state.medicoRecetaDetectado.uppercase()}",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = tealPrimary
                            )
                            Text(
                                text = state.modeloRecetaUsado.uppercase(),
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold,
                                color = tealPrimary
                            )
                        }
                        Text(
                            text = state.resumenRecetaIa,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Medium,
                            color = textPrimary
                        )
                    }
                }
            }

            // Título de Sección 2: Lista de Confirmación Editable
            Text(
                text = "2. Confirma y Edita los Medicamentos Detectados (${state.itemsRecetaEditables.size})",
                fontSize = 15.sp,
                fontWeight = FontWeight.ExtraBold,
                color = textPrimary,
                modifier = Modifier.padding(top = 4.dp)
            )

            state.itemsRecetaEditables.forEachIndexed { index, item ->
                val hasAllergyAlert = !item.alertaAlergia.isNullOrBlank()
                val hasInteractionAlert = !item.alertaInteraccion.isNullOrBlank()
                val isHighConfidence = item.confidence.equals("high", ignoreCase = true)

                val cardBorderColor = when {
                    hasAllergyAlert -> Color(0xFFD32F2F)
                    hasInteractionAlert || !isHighConfidence -> Color(0xFFE65100)
                    item.seleccionado -> tealPrimary
                    else -> borderLight
                }

                Surface(
                    shape = RoundedCornerShape(18.dp),
                    color = surfaceColor,
                    border = BorderStroke(if (hasAllergyAlert) 2.dp else 1.5.dp, cardBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier.padding(15.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        // Fila superior: Checkbox + Nombre + Badge de Confianza IA
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Checkbox(
                                checked = item.seleccionado,
                                onCheckedChange = { checked ->
                                    onActualizarItem(index, item.copy(seleccionado = checked))
                                },
                                colors = CheckboxDefaults.colors(checkedColor = tealPrimary)
                            )
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = item.nombre,
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = textPrimary
                                )
                                if (item.principioActivo.isNotBlank()) {
                                    Text(
                                        text = "Principio activo: ${item.principioActivo}",
                                        fontSize = 12.sp,
                                        color = textSecondary
                                    )
                                }
                            }
                            Surface(
                                shape = RoundedCornerShape(50),
                                color = if (isHighConfidence) Color(0xFFE6F4EA) else Color(0xFFFFF3E0)
                            ) {
                                Text(
                                    text = if (isHighConfidence) "Confianza Alta" else "Revisar OCR",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isHighConfidence) Color(0xFF1E7E34) else Color(0xFFE65100),
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                )
                            }
                        }

                        // Banner de Alerta Roja de Alergia Cruzada (Regla 1)
                        if (hasAllergyAlert) {
                            Surface(
                                shape = RoundedCornerShape(12.dp),
                                color = Color(0xFFFFEBEE),
                                border = BorderStroke(1.dp, Color(0xFFEF5350)),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Row(
                                    modifier = Modifier.padding(10.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.WarningAmber,
                                        contentDescription = null,
                                        tint = Color(0xFFC62828),
                                        modifier = Modifier.size(20.dp)
                                    )
                                    Spacer(Modifier.width(8.dp))
                                    Text(
                                        text = item.alertaAlergia ?: "",
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color(0xFFB71C1C)
                                    )
                                }
                            }
                        }

                        // Banner de Alerta de Interacción (Regla 4)
                        if (hasInteractionAlert) {
                            Surface(
                                shape = RoundedCornerShape(12.dp),
                                color = Color(0xFFFFF8E1),
                                border = BorderStroke(1.dp, Color(0xFFFFB300)),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Row(
                                    modifier = Modifier.padding(10.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        imageVector = Icons.Outlined.Shield,
                                        contentDescription = null,
                                        tint = Color(0xFFE65100),
                                        modifier = Modifier.size(18.dp)
                                    )
                                    Spacer(Modifier.width(8.dp))
                                    Text(
                                        text = item.alertaInteraccion ?: "",
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        color = Color(0xFFBF360C)
                                    )
                                }
                            }
                        }

                        HorizontalDivider(color = borderLight)

                        // Campos editables: Nombre y Dosis
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            OutlinedTextField(
                                value = item.nombre,
                                onValueChange = { onActualizarItem(index, item.copy(nombre = it)) },
                                label = { Text("Medicamento") },
                                singleLine = true,
                                modifier = Modifier.weight(1.3f),
                                shape = RoundedCornerShape(12.dp)
                            )
                            OutlinedTextField(
                                value = item.dosageOrDosis(),
                                onValueChange = { onActualizarItem(index, item.copy(dosis = it)) },
                                label = { Text("Dosis") },
                                singleLine = true,
                                modifier = Modifier.weight(0.9f),
                                shape = RoundedCornerShape(12.dp)
                            )
                        }

                        // Frecuencia en horas + Duración en días
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Column(modifier = Modifier.weight(1.4f)) {
                                Text(
                                    text = "Frecuencia (cada ${item.frecuenciaHoras} h)",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = textSecondary
                                )
                                Spacer(Modifier.height(4.dp))
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    listOf(6, 8, 12, 24).forEach { freq ->
                                        val selectedFreq = item.frecuenciaHoras == freq
                                        Surface(
                                            shape = RoundedCornerShape(8.dp),
                                            color = if (selectedFreq) tealPrimary else bgPrimary,
                                            border = BorderStroke(1.dp, if (selectedFreq) tealPrimary else borderLight),
                                            modifier = Modifier.clickable {
                                                onActualizarItem(index, item.copy(frecuenciaHoras = freq))
                                            }
                                        ) {
                                            Text(
                                                text = "${freq}h",
                                                fontSize = 12.sp,
                                                fontWeight = FontWeight.Bold,
                                                color = if (selectedFreq) Color.White else textPrimary,
                                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                                            )
                                        }
                                    }
                                }
                            }

                            OutlinedTextField(
                                value = item.duracionDias.toString(),
                                onValueChange = { raw ->
                                    val d = raw.filter { it.isDigit() }.toIntOrNull() ?: 7
                                    onActualizarItem(index, item.copy(duracionDias = d.coerceIn(1, 365)))
                                },
                                label = { Text("Días") },
                                singleLine = true,
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                modifier = Modifier.weight(0.6f),
                                shape = RoundedCornerShape(12.dp)
                            )
                        }

                        // Instrucciones de toma
                        OutlinedTextField(
                            value = item.instrucciones,
                            onValueChange = { onActualizarItem(index, item.copy(instrucciones = it)) },
                            label = { Text("Instrucciones de toma") },
                            singleLine = true,
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(12.dp)
                        )
                    }
                }
            }

            Spacer(Modifier.height(24.dp))
        }
    }
}

private fun EditablePrescriptionItem.dosageOrDosis(): String = this.dosis

private fun scaleBitmapForOcr(bitmap: Bitmap, maxDim: Int = 1280): Bitmap {
    val maxSide = max(bitmap.width, bitmap.height)
    if (maxSide <= maxDim) return bitmap
    val ratio = maxDim.toFloat() / maxSide.toFloat()
    val w = (bitmap.width * ratio).toInt().coerceAtLeast(1)
    val h = (bitmap.height * ratio).toInt().coerceAtLeast(1)
    return Bitmap.createScaledBitmap(bitmap, w, h, true)
}

private fun encodeBitmapJpegBase64(bitmap: Bitmap): String {
    val bos = ByteArrayOutputStream()
    bitmap.compress(Bitmap.CompressFormat.JPEG, 82, bos)
    return Base64.encodeToString(bos.toByteArray(), Base64.NO_WRAP)
}

private fun decodeBitmapFromUri(context: Context, uri: Uri, maxDim: Int = 1280): Bitmap? {
    return runCatching {
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        context.contentResolver.openInputStream(uri)?.use { stream ->
            BitmapFactory.decodeStream(stream, null, bounds)
        }
        val maxSide = max(bounds.outWidth, bounds.outHeight)
        var sampleSize = 1
        while (maxSide / sampleSize > maxDim * 2) {
            sampleSize *= 2
        }
        val decodeOpts = BitmapFactory.Options().apply { inSampleSize = sampleSize }
        context.contentResolver.openInputStream(uri)?.use { stream ->
            BitmapFactory.decodeStream(stream, null, decodeOpts)
        }
    }.getOrNull()
}

private suspend fun runMlKitOcr(bitmap: Bitmap): String = suspendCancellableCoroutine { cont ->
    val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
    val image = InputImage.fromBitmap(bitmap, 0)
    recognizer.process(image)
        .addOnSuccessListener { result ->
            recognizer.close()
            if (cont.isActive) cont.resume(result.text ?: "")
        }
        .addOnFailureListener {
            recognizer.close()
            if (cont.isActive) cont.resume("")
        }
}
