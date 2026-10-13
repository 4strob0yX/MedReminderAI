package com.medreminder.ai.ui.auth

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
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.outlined.Email
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.MedicalServices
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
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

/** Contenedor: conecta el ViewModel con la vista pasiva. */
@Composable
fun AuthRoute(viewModel: AuthViewModel, onAuthenticated: () -> Unit) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(state.isAuthenticated) {
        if (state.isAuthenticated) onAuthenticated()
    }

    AuthScreen(
        state = state,
        onNombreChange = viewModel::onNombreChange,
        onEmailChange = viewModel::onEmailChange,
        onPasswordChange = viewModel::onPasswordChange,
        onTogglePasswordVisibility = viewModel::onTogglePasswordVisibility,
        onSubmit = viewModel::onSubmit,
        onToggleMode = viewModel::onToggleMode,
        onErrorShown = viewModel::onErrorShown
    )
}

/** Vista completamente pasiva: diseña Login y Crear Cuenta fiel a los mockups clínicos. */
@Composable
fun AuthScreen(
    state: AuthUiState,
    onNombreChange: (String) -> Unit,
    onEmailChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    onTogglePasswordVisibility: () -> Unit,
    onSubmit: () -> Unit,
    onToggleMode: () -> Unit,
    onErrorShown: () -> Unit
) {
    val snackbarHostState = remember { SnackbarHostState() }
    val isRegister = state.mode == AuthMode.REGISTER

    LaunchedEffect(state.errorMessage) {
        state.errorMessage?.let {
            snackbarHostState.showSnackbar(it)
            onErrorShown()
        }
    }

    Scaffold(
        containerColor = AppBackground,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            if (isRegister) {
                RegisterTopBar(onBack = onToggleMode)
            }
        }
    ) { padding ->
        if (isRegister) {
            RegisterContent(
                state = state,
                onNombreChange = onNombreChange,
                onEmailChange = onEmailChange,
                onPasswordChange = onPasswordChange,
                onTogglePasswordVisibility = onTogglePasswordVisibility,
                onSubmit = onSubmit,
                onToggleMode = onToggleMode,
                modifier = Modifier.padding(padding)
            )
        } else {
            LoginContent(
                state = state,
                onEmailChange = onEmailChange,
                onPasswordChange = onPasswordChange,
                onTogglePasswordVisibility = onTogglePasswordVisibility,
                onSubmit = onSubmit,
                onToggleMode = onToggleMode,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun RegisterTopBar(onBack: () -> Unit) {
    Column(modifier = Modifier.background(AppBackground)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onBack) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Volver",
                    tint = TextPrimary
                )
            }
            Surface(
                shape = RoundedCornerShape(10.dp),
                color = TealSoftBg,
                modifier = Modifier.size(36.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Outlined.MedicalServices,
                        contentDescription = null,
                        tint = TealPrimary,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
            Spacer(Modifier.width(12.dp))
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
                modifier = Modifier.size(38.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Outlined.Person,
                        contentDescription = "Perfil",
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
private fun LoginContent(
    state: AuthUiState,
    onEmailChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    onTogglePasswordVisibility: () -> Unit,
    onSubmit: () -> Unit,
    onToggleMode: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.height(48.dp))

        // Logo superior en tarjeta elevada suave
        Surface(
            shape = RoundedCornerShape(24.dp),
            color = CardBackground,
            shadowElevation = 2.dp,
            modifier = Modifier.size(88.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Surface(
                    shape = RoundedCornerShape(18.dp),
                    color = TealSoftBg,
                    modifier = Modifier.size(64.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Outlined.MedicalServices,
                            contentDescription = "Logo MedReminder",
                            tint = TealPrimary,
                            modifier = Modifier.size(34.dp)
                        )
                    }
                }
            }
        }

        Spacer(Modifier.height(22.dp))

        Text(
            text = "MedReminder",
            fontSize = 30.sp,
            fontWeight = FontWeight.ExtraBold,
            color = TextPrimary
        )

        Spacer(Modifier.height(8.dp))

        Text(
            text = "Gestión inteligente y puntual de tus\ntomas",
            fontSize = 16.sp,
            color = TextSecondary,
            textAlign = TextAlign.Center,
            lineHeight = 22.sp
        )

        Spacer(Modifier.height(36.dp))

        // Campo Correo electrónico
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Outlined.Email,
                contentDescription = null,
                tint = TealPrimary,
                modifier = Modifier.size(18.dp)
            )
            Spacer(Modifier.width(8.dp))
            Text(
                text = "Correo electrónico",
                fontWeight = FontWeight.SemiBold,
                fontSize = 15.sp,
                color = TextPrimary
            )
        }
        Spacer(Modifier.height(8.dp))
        ClinicalTextField(
            value = state.email,
            onValueChange = onEmailChange,
            placeholder = "ejemplo@correo.com",
            error = state.emailError,
            enabled = !state.isLoading,
            keyboardType = KeyboardType.Email
        )

        Spacer(Modifier.height(20.dp))

        // Campo Contraseña
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Outlined.Lock,
                    contentDescription = null,
                    tint = TealPrimary,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = "Contraseña",
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 15.sp,
                    color = TextPrimary
                )
            }
            Text(
                text = "¿La olvidaste?",
                fontSize = 13.sp,
                fontWeight = FontWeight.SemiBold,
                color = TealPrimary
            )
        }
        Spacer(Modifier.height(8.dp))
        ClinicalTextField(
            value = state.password,
            onValueChange = onPasswordChange,
            placeholder = "••••••••",
            error = state.passwordError,
            enabled = !state.isLoading,
            keyboardType = KeyboardType.Password,
            visualTransformation = if (state.passwordVisible) VisualTransformation.None
            else PasswordVisualTransformation(),
            trailingIcon = {
                IconButton(onClick = onTogglePasswordVisibility) {
                    Icon(
                        imageVector = if (state.passwordVisible) Icons.Outlined.VisibilityOff
                        else Icons.Outlined.Visibility,
                        contentDescription = "Mostrar u ocultar contraseña",
                        tint = TextSecondary
                    )
                }
            }
        )

        Spacer(Modifier.height(28.dp))

        // Botón Iniciar Sesión (>= 56dp, bloqueado mientras carga)
        Button(
            onClick = onSubmit,
            enabled = !state.isLoading,
            shape = RoundedCornerShape(18.dp),
            colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 60.dp)
        ) {
            if (state.isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = Color.White,
                    strokeWidth = 2.dp
                )
            } else {
                Text(
                    text = "Iniciar Sesión",
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Spacer(Modifier.width(8.dp))
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(20.dp)
                )
            }
        }

        Spacer(Modifier.height(24.dp))

        // Banner informativo de seguridad
        Surface(
            shape = RoundedCornerShape(18.dp),
            color = TealSoftBg.copy(alpha = 0.65f),
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    shape = CircleShape,
                    color = TealBadgeBg,
                    modifier = Modifier.size(44.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Outlined.Shield,
                            contentDescription = null,
                            tint = TealPrimary,
                            modifier = Modifier.size(22.dp)
                        )
                    }
                }
                Spacer(Modifier.width(14.dp))
                Text(
                    text = "Acceso seguro validado para pacientes y cuidadores familiares.",
                    fontSize = 14.sp,
                    color = TextSecondary,
                    lineHeight = 20.sp
                )
            }
        }

        Spacer(Modifier.height(48.dp))

        // Enlace inferior ¿No tienes cuenta? Regístrate
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 56.dp)
                .clip(RoundedCornerShape(12.dp))
                .clickable(enabled = !state.isLoading) { onToggleMode() },
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = buildAnnotatedString {
                    withStyle(SpanStyle(color = TealDark, fontWeight = FontWeight.SemiBold)) {
                        append("¿No tienes cuenta? ")
                    }
                    withStyle(
                        SpanStyle(
                            color = TealDark,
                            fontWeight = FontWeight.Bold,
                            textDecoration = TextDecoration.Underline
                        )
                    ) {
                        append("Regístrate")
                    }
                },
                fontSize = 16.sp
            )
        }

        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun RegisterContent(
    state: AuthUiState,
    onNombreChange: (String) -> Unit,
    onEmailChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    onTogglePasswordVisibility: () -> Unit,
    onSubmit: () -> Unit,
    onToggleMode: () -> Unit,
    modifier: Modifier = Modifier
) {
    val passLen = state.password.length
    val strengthBars = when {
        passLen >= 10 -> 3
        passLen >= 8 -> 2
        passLen >= 1 -> 1
        else -> 0
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp)
            .verticalScroll(rememberScrollState())
    ) {
        Spacer(Modifier.height(20.dp))

        // Pill "Paso 1 de 2"
        Surface(
            shape = RoundedCornerShape(50),
            color = TealBadgeBg
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Outlined.Shield,
                    contentDescription = null,
                    tint = TealBadgeText,
                    modifier = Modifier.size(14.dp)
                )
                Spacer(Modifier.width(6.dp))
                Text(
                    text = "Paso 1 de 2",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = TealBadgeText
                )
            }
        }

        Spacer(Modifier.height(14.dp))

        Text(
            text = "Crear Cuenta",
            fontSize = 28.sp,
            fontWeight = FontWeight.ExtraBold,
            color = TextPrimary
        )

        Spacer(Modifier.height(6.dp))

        Text(
            text = "Configura tu perfil para no olvidar ninguna dosis.",
            fontSize = 15.sp,
            color = TextSecondary
        )

        Spacer(Modifier.height(24.dp))

        // Nombre completo
        FieldLabelRow(label = "Nombre completo", rightHint = "Requerido")
        Spacer(Modifier.height(8.dp))
        ClinicalTextField(
            value = state.nombre,
            onValueChange = onNombreChange,
            placeholder = "Tu nombre y apellido",
            error = state.nombreError,
            enabled = !state.isLoading,
            leadingIcon = Icons.Outlined.Person
        )

        Spacer(Modifier.height(18.dp))

        // Correo electrónico
        FieldLabelRow(label = "Correo electrónico", rightHint = "Requerido")
        Spacer(Modifier.height(8.dp))
        ClinicalTextField(
            value = state.email,
            onValueChange = onEmailChange,
            placeholder = "correo@ejemplo.com",
            error = state.emailError,
            enabled = !state.isLoading,
            keyboardType = KeyboardType.Email,
            leadingIcon = Icons.Outlined.Email
        )

        Spacer(Modifier.height(18.dp))

        // Contraseña
        FieldLabelRow(label = "Contraseña", rightHint = "Mín. 8 carácteres")
        Spacer(Modifier.height(8.dp))
        ClinicalTextField(
            value = state.password,
            onValueChange = onPasswordChange,
            placeholder = "Mínimo 8 caracteres",
            error = state.passwordError,
            enabled = !state.isLoading,
            keyboardType = KeyboardType.Password,
            leadingIcon = Icons.Outlined.Lock,
            visualTransformation = if (state.passwordVisible) VisualTransformation.None
            else PasswordVisualTransformation(),
            trailingIcon = {
                IconButton(onClick = onTogglePasswordVisibility) {
                    Icon(
                        imageVector = if (state.passwordVisible) Icons.Outlined.VisibilityOff
                        else Icons.Outlined.Visibility,
                        contentDescription = "Mostrar u ocultar contraseña",
                        tint = TextSecondary
                    )
                }
            }
        )

        Spacer(Modifier.height(10.dp))

        // Barras de fortaleza de contraseña + texto "Seguridad"
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            repeat(3) { index ->
                val active = index < strengthBars
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height(5.dp)
                        .clip(RoundedCornerShape(50))
                        .background(if (active) TealPrimary else Color(0xFFE2E0DD))
                )
                Spacer(Modifier.width(8.dp))
            }
            Text(
                text = "Seguridad",
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                color = TextSecondary
            )
        }

        Spacer(Modifier.height(24.dp))

        // Tarjeta "Privacidad de grado clínico"
        Surface(
            shape = RoundedCornerShape(18.dp),
            color = SoftWarmSurface,
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.padding(18.dp),
                verticalAlignment = Alignment.Top
            ) {
                Surface(
                    shape = CircleShape,
                    color = TealPrimary,
                    modifier = Modifier.size(38.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Outlined.Shield,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
                Spacer(Modifier.width(14.dp))
                Column {
                    Text(
                        text = "Privacidad de grado clínico",
                        fontWeight = FontWeight.Bold,
                        fontSize = 15.sp,
                        color = TextPrimary
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = "Tus datos médicos se almacenan de forma segura y privada bajo cifrado de extremo a extremo.",
                        fontSize = 13.5.sp,
                        color = TextSecondary,
                        lineHeight = 19.sp
                    )
                }
            }
        }

        Spacer(Modifier.height(28.dp))

        // Botón Registrar (>= 56dp)
        Button(
            onClick = onSubmit,
            enabled = !state.isLoading,
            shape = RoundedCornerShape(18.dp),
            colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 60.dp)
        ) {
            if (state.isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = Color.White,
                    strokeWidth = 2.dp
                )
            } else {
                Text(
                    text = "Registrar",
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Spacer(Modifier.width(8.dp))
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(20.dp)
                )
            }
        }

        Spacer(Modifier.height(16.dp))

        // ¿Ya tienes cuenta? Iniciar sesión
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 56.dp)
                .clip(RoundedCornerShape(12.dp))
                .clickable(enabled = !state.isLoading) { onToggleMode() },
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "¿Ya tienes cuenta?  ",
                fontSize = 15.sp,
                color = TextSecondary
            )
            Text(
                text = "Iniciar sesión",
                fontSize = 15.sp,
                fontWeight = FontWeight.Bold,
                color = TealDark
            )
        }

        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun FieldLabelRow(label: String, rightHint: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            fontWeight = FontWeight.Bold,
            fontSize = 15.sp,
            color = TextPrimary
        )
        Text(
            text = rightHint,
            fontSize = 12.5.sp,
            color = TextSecondary
        )
    }
}

@Composable
private fun ClinicalTextField(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String,
    error: String?,
    enabled: Boolean,
    keyboardType: KeyboardType = KeyboardType.Text,
    leadingIcon: ImageVector? = null,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    trailingIcon: @Composable (() -> Unit)? = null
) {
    Column {
        Surface(
            shape = RoundedCornerShape(16.dp),
            color = CardBackground,
            border = BorderStroke(
                width = 1.dp,
                color = if (error != null) MaterialTheme.colorScheme.error else InputBorderColor
            )
        ) {
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
                leadingIcon = leadingIcon?.let { icon ->
                    {
                        Icon(
                            imageVector = icon,
                            contentDescription = null,
                            tint = TextSecondary,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                },
                trailingIcon = trailingIcon,
                singleLine = true,
                enabled = enabled,
                keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
                visualTransformation = visualTransformation,
                shape = RoundedCornerShape(16.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = CardBackground,
                    unfocusedContainerColor = CardBackground,
                    disabledContainerColor = CardBackground,
                    focusedBorderColor = TealPrimary,
                    unfocusedBorderColor = Color.Transparent,
                    disabledBorderColor = Color.Transparent
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 58.dp)
            )
        }
        if (error != null) {
            Text(
                text = error,
                color = MaterialTheme.colorScheme.error,
                fontSize = 12.sp,
                modifier = Modifier.padding(start = 12.dp, top = 4.dp)
            )
        }
    }
}
