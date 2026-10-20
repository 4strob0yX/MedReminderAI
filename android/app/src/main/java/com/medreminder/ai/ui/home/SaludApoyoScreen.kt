package com.medreminder.ai.ui.home

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.ContactPhone
import androidx.compose.material.icons.outlined.HealthAndSafety
import androidx.compose.material.icons.outlined.MedicalServices
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.data.remote.AlergiaDto
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.CyanIconBg
import com.medreminder.ai.ui.theme.CyanIconTint
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

@Composable
fun SaludApoyoScreenContent(
    state: HomeUiState,
    onAgregarAlergia: (String, String, String?) -> Unit,
    onEliminarAlergia: (Int) -> Unit,
    onGuardarContacto: (Int?, String, String, String, String?, Boolean) -> Unit,
    onEliminarContacto: (Int) -> Unit
) {
    val context = LocalContext.current
    var showDialogAlergia by remember { mutableStateOf(false) }
    var showDialogContacto by remember { mutableStateOf(false) }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 18.dp, bottom = 96.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        // Encabezado
        item {
            Surface(
                shape = RoundedCornerShape(18.dp),
                color = SoftWarmSurface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)) {
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
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.HealthAndSafety,
                                    contentDescription = null,
                                    tint = TealBadgeText,
                                    modifier = Modifier.size(13.dp)
                                )
                                Spacer(Modifier.width(5.dp))
                                Text(
                                    text = "SEGURIDAD CLÍNICA",
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = TealBadgeText,
                                    letterSpacing = 0.5.sp
                                )
                            }
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(
                        text = "Alergias y Contacto de Apoyo",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                    Spacer(Modifier.height(3.dp))
                    Text(
                        text = "Validación cruzada de alergias y enlace rápido con tu red de cuidadores ante dosis críticas.",
                        fontSize = 12.5.sp,
                        color = TextSecondary,
                        lineHeight = 17.sp
                    )
                }
            }
        }

        // --- SECCIÓN 1: CONTACTO DE APOYO / EMERGENCIA ---
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.ContactPhone,
                        contentDescription = null,
                        tint = TealDark,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = "Contacto de Apoyo",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                if (state.contactosApoyo.isNotEmpty()) {
                    TextButton(onClick = { showDialogContacto = true }) {
                        Text("Modificar", color = TealPrimary, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }

        if (state.contactosApoyo.isEmpty()) {
            item {
                Surface(
                    shape = RoundedCornerShape(20.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier.padding(22.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Surface(
                            shape = CircleShape,
                            color = TealSoftBg,
                            modifier = Modifier.size(54.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.Phone,
                                    contentDescription = null,
                                    tint = TealDark,
                                    modifier = Modifier.size(26.dp)
                                )
                            }
                        }
                        Spacer(Modifier.height(12.dp))
                        Text(
                            text = "Sin contacto de apoyo registrado",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "Agrega a un familiar, cuidador o médico de confianza para llamarle rápidamente ante dosis críticas.",
                            fontSize = 13.sp,
                            color = TextSecondary,
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center
                        )
                        Spacer(Modifier.height(16.dp))
                        Button(
                            onClick = { showDialogContacto = true },
                            shape = RoundedCornerShape(14.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = TealPrimary)
                        ) {
                            Icon(Icons.Default.Add, contentDescription = null, tint = Color.White)
                            Spacer(Modifier.width(6.dp))
                            Text("Registrar Contacto de Apoyo", color = Color.White)
                        }
                    }
                }
            }
        } else {
            items(state.contactosApoyo, key = { it.idContacto }) { contacto ->
                Surface(
                    shape = RoundedCornerShape(20.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.Top
                        ) {
                            Surface(
                                shape = CircleShape,
                                color = CyanIconBg,
                                modifier = Modifier.size(44.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = Icons.Outlined.Person,
                                        contentDescription = null,
                                        tint = CyanIconTint,
                                        modifier = Modifier.size(24.dp)
                                    )
                                }
                            }
                            Spacer(Modifier.width(12.dp))
                            Column(
                                modifier = Modifier.weight(1f),
                                verticalArrangement = Arrangement.spacedBy(2.dp)
                            ) {
                                Text(
                                    text = contacto.nombreCompleto,
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                                if (contacto.esPrincipal) {
                                    Surface(
                                        shape = RoundedCornerShape(6.dp),
                                        color = TealBadgeBg
                                    ) {
                                        Text(
                                            text = "PRINCIPAL",
                                            color = TealBadgeText,
                                            fontSize = 9.5.sp,
                                            fontWeight = FontWeight.ExtraBold,
                                            maxLines = 1,
                                            softWrap = false,
                                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                        )
                                    }
                                }
                                Text(
                                    text = "${contacto.parentesco} • ${contacto.telefono}",
                                    fontSize = 13.sp,
                                    color = TextSecondary
                                )
                                if (!contacto.correo.isNullOrBlank()) {
                                    Text(
                                        text = contacto.correo,
                                        fontSize = 12.sp,
                                        color = TextMuted
                                    )
                                }
                            }
                            IconButton(
                                onClick = { onEliminarContacto(contacto.idContacto) },
                                modifier = Modifier.size(36.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Delete,
                                    contentDescription = "Eliminar contacto",
                                    tint = AlertRedText,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }

                        Button(
                            onClick = {
                                val intent = Intent(Intent.ACTION_DIAL).apply {
                                    data = Uri.parse("tel:${contacto.telefono}")
                                }
                                context.startActivity(intent)
                            },
                            shape = RoundedCornerShape(14.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = TealDark),
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(46.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Phone,
                                contentDescription = null,
                                tint = Color.White,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = "Llamar a ${contacto.nombreCompleto.take(24)}",
                                fontWeight = FontWeight.Bold,
                                fontSize = 14.sp
                            )
                        }
                    }
                }
            }
        }

        // --- SECCIÓN 2: ALERGIAS CLÍNICAS ---
        item {
            Spacer(Modifier.height(10.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Warning,
                        contentDescription = null,
                        tint = Color(0xFFD32F2F),
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = "Mis Alergias",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                TextButton(onClick = { showDialogAlergia = true }) {
                    Icon(Icons.Default.Add, contentDescription = null, tint = TealPrimary, modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(4.dp))
                    Text("Nueva Alergia", color = TealPrimary, fontWeight = FontWeight.Bold)
                }
            }
        }

        if (state.alergiasUsuario.isEmpty()) {
            item {
                Surface(
                    shape = RoundedCornerShape(20.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier.padding(22.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Surface(
                            shape = CircleShape,
                            color = Color(0xFFE8F5E9),
                            modifier = Modifier.size(54.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.Shield,
                                    contentDescription = null,
                                    tint = Color(0xFF2E7D32),
                                    modifier = Modifier.size(26.dp)
                                )
                            }
                        }
                        Spacer(Modifier.height(12.dp))
                        Text(
                            text = "No tienes alergias registradas",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "Si eres alérgico a la Penicilina, AINEs (Ibuprofeno/Aspirina), Sulfas u otros fármacos, regístralas para activar las alertas de contraindicación.",
                            fontSize = 13.sp,
                            color = TextSecondary,
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center
                        )
                        Spacer(Modifier.height(16.dp))
                        Button(
                            onClick = { showDialogAlergia = true },
                            shape = RoundedCornerShape(14.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFC62828))
                        ) {
                            Icon(Icons.Default.Add, contentDescription = null, tint = Color.White)
                            Spacer(Modifier.width(6.dp))
                            Text("Registrar Alergia Médica", color = Color.White)
                        }
                    }
                }
            }
        } else {
            items(state.alergiasUsuario) { alergia ->
                val colorFondoSeveridad = when (alergia.severidad.lowercase()) {
                    "grave" -> Color(0xFFFFEBEE)
                    "moderada" -> Color(0xFFFFF3E0)
                    else -> Color(0xFFE3F2FD)
                }
                val colorTextoSeveridad = when (alergia.severidad.lowercase()) {
                    "grave" -> Color(0xFFC62828)
                    "moderada" -> Color(0xFFE65100)
                    else -> Color(0xFF1565C0)
                }

                Surface(
                    shape = RoundedCornerShape(18.dp),
                    color = CardBackground,
                    border = BorderStroke(1.dp, InputBorderColor),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = colorFondoSeveridad,
                            modifier = Modifier.size(44.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.Outlined.Warning,
                                    contentDescription = null,
                                    tint = colorTextoSeveridad,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                        }
                        Spacer(Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    text = alergia.sustancia,
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TextPrimary
                                )
                                Spacer(Modifier.width(8.dp))
                                Surface(
                                    shape = RoundedCornerShape(6.dp),
                                    color = colorFondoSeveridad
                                ) {
                                    Text(
                                        text = alergia.severidad.uppercase(),
                                        color = colorTextoSeveridad,
                                        fontSize = 10.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                    )
                                }
                            }
                            if (!alergia.reaccion.isNullOrBlank()) {
                                Spacer(Modifier.height(2.dp))
                                Text(
                                    text = "Reacción: ${alergia.reaccion}",
                                    fontSize = 12.5.sp,
                                    color = TextSecondary
                                )
                            }
                        }
                        IconButton(onClick = { onEliminarAlergia(alergia.idAlergia) }) {
                            Icon(
                                imageVector = Icons.Default.Delete,
                                contentDescription = "Eliminar alergia",
                                tint = AlertRedText
                            )
                        }
                    }
                }
            }
        }
    }

    // Modal para agregar Alergia
    if (showDialogAlergia) {
        DialogAlergia(
            onDismiss = { showDialogAlergia = false },
            onGuardar = { sustancia, severidad, reaccion ->
                onAgregarAlergia(sustancia, severidad, reaccion)
                showDialogAlergia = false
            }
        )
    }

    // Modal para agregar/editar Contacto de Apoyo
    if (showDialogContacto) {
        val contactoExistente = state.contactosApoyo.firstOrNull()
        DialogContacto(
            contactoActual = contactoExistente,
            onDismiss = { showDialogContacto = false },
            onGuardar = { id, nom, tel, par, cor, prin ->
                onGuardarContacto(id, nom, tel, par, cor, prin)
                showDialogContacto = false
            }
        )
    }
}

@Composable
private fun DialogAlergia(
    onDismiss: () -> Unit,
    onGuardar: (sustancia: String, severidad: String, reaccion: String?) -> Unit
) {
    var sustancia by remember { mutableStateOf("") }
    var severidad by remember { mutableStateOf("grave") }
    var reaccion by remember { mutableStateOf("") }

    Dialog(onDismissRequest = onDismiss, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(
            shape = RoundedCornerShape(24.dp),
            color = CardBackground,
            modifier = Modifier
                .fillMaxWidth(0.92f)
                .padding(16.dp)
        ) {
            Column(
                modifier = Modifier
                    .padding(22.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Registrar Alergia",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Cerrar")
                    }
                }
                Spacer(Modifier.height(14.dp))

                Text("Sustancia o Fármaco:", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(6.dp))
                OutlinedTextField(
                    value = sustancia,
                    onValueChange = { sustancia = it },
                    placeholder = { Text("ej. Penicilina, Ibuprofeno, Sulfas") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                // Chips rápidos de sugerencia
                Spacer(Modifier.height(8.dp))
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    listOf("Penicilina", "AINEs", "Sulfas", "Aspirina").forEach { chip ->
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = SoftWarmSurface,
                            modifier = Modifier
                                .clip(RoundedCornerShape(10.dp))
                                .clickable { sustancia = chip }
                        ) {
                            Text(
                                text = "+ $chip",
                                fontSize = 11.5.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = TealDark,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 5.dp)
                            )
                        }
                    }
                }

                Spacer(Modifier.height(16.dp))
                Text("Severidad:", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(6.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    listOf("grave" to "Grave", "moderada" to "Moderada", "leve" to "Leve").forEach { (key, label) ->
                        val isSelected = severidad == key
                        Surface(
                            shape = RoundedCornerShape(12.dp),
                            color = if (isSelected) TealDark else SoftWarmSurface,
                            border = if (isSelected) null else BorderStroke(1.dp, InputBorderColor),
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { severidad = key }
                        ) {
                            Box(
                                modifier = Modifier.padding(vertical = 8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = label,
                                    fontSize = 12.5.sp,
                                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                                    color = if (isSelected) Color.White else TextPrimary
                                )
                            }
                        }
                    }
                }

                Spacer(Modifier.height(16.dp))
                Text("Reacción / Síntomas observados (opcional):", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(6.dp))
                OutlinedTextField(
                    value = reaccion,
                    onValueChange = { reaccion = it },
                    placeholder = { Text("ej. Anafilaxia, erupción cutánea, broncoespasmo") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                Spacer(Modifier.height(20.dp))
                Button(
                    onClick = {
                        if (sustancia.isNotBlank()) {
                            onGuardar(sustancia.trim(), severidad, reaccion.trim().ifBlank { null })
                        }
                    },
                    shape = RoundedCornerShape(14.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFC62828)),
                    modifier = Modifier.fillMaxWidth().height(52.dp)
                ) {
                    Text("Guardar Alergia", fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
        }
    }
}

@Composable
private fun DialogContacto(
    contactoActual: ContactoApoyoDto?,
    onDismiss: () -> Unit,
    onGuardar: (id: Int?, nombre: String, telefono: String, parentesco: String, correo: String?, esPrincipal: Boolean) -> Unit
) {
    var nombre by remember { mutableStateOf(contactoActual?.nombreCompleto ?: "") }
    var telefono by remember { mutableStateOf(contactoActual?.telefono ?: "") }
    var parentesco by remember { mutableStateOf(contactoActual?.parentesco ?: "Familiar / Cuidador") }
    var correo by remember { mutableStateOf(contactoActual?.correo ?: "") }

    Dialog(onDismissRequest = onDismiss, properties = DialogProperties(usePlatformDefaultWidth = false)) {
        Surface(
            shape = RoundedCornerShape(24.dp),
            color = CardBackground,
            modifier = Modifier
                .fillMaxWidth(0.92f)
                .padding(16.dp)
        ) {
            Column(
                modifier = Modifier
                    .padding(22.dp)
                    .verticalScroll(rememberScrollState())
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = if (contactoActual != null) "Editar Contacto de Apoyo" else "Nuevo Contacto de Apoyo",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary
                    )
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Cerrar")
                    }
                }
                Spacer(Modifier.height(14.dp))

                Text("Nombre Completo:", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(4.dp))
                OutlinedTextField(
                    value = nombre,
                    onValueChange = { nombre = it },
                    placeholder = { Text("ej. María Gómez") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                Spacer(Modifier.height(12.dp))
                Text("Teléfono de Contacto (para llamadas directas):", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(4.dp))
                OutlinedTextField(
                    value = telefono,
                    onValueChange = { telefono = it },
                    placeholder = { Text("ej. +52 55 1234 5678") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                Spacer(Modifier.height(12.dp))
                Text("Parentesco o Rol:", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(4.dp))
                OutlinedTextField(
                    value = parentesco,
                    onValueChange = { parentesco = it },
                    placeholder = { Text("ej. Hijo/a, Cónyuge, Médico tratante") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                Spacer(Modifier.height(12.dp))
                Text("Correo Electrónico (opcional):", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = TextPrimary)
                Spacer(Modifier.height(4.dp))
                OutlinedTextField(
                    value = correo,
                    onValueChange = { correo = it },
                    placeholder = { Text("ej. contacto@ejemplo.com") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp)
                )

                Spacer(Modifier.height(20.dp))
                Button(
                    onClick = {
                        if (nombre.isNotBlank() && telefono.isNotBlank()) {
                            onGuardar(
                                contactoActual?.idContacto,
                                nombre.trim(),
                                telefono.trim(),
                                parentesco.trim(),
                                correo.trim().ifBlank { null },
                                true
                            )
                        }
                    },
                    shape = RoundedCornerShape(14.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                    modifier = Modifier.fillMaxWidth().height(52.dp)
                ) {
                    Text("Guardar Contacto", fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
        }
    }
}
