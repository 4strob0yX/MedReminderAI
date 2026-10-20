package com.medreminder.ai.ui.auth

import androidx.activity.compose.BackHandler
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
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.EaseInOutSine
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.Canvas
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.outlined.AccessAlarm
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Email
import androidx.compose.material.icons.outlined.HealthAndSafety
import androidx.compose.material.icons.outlined.Lock
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
import androidx.compose.material3.OutlinedButton
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
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
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
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.medreminder.ai.ui.components.MedBrandLogo
import com.medreminder.ai.ui.components.MediMascotView
import com.medreminder.ai.ui.components.MediMood
import com.medreminder.ai.ui.theme.AppBackground
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.LocalAccessibilitySettings
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
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
        onErrorShown = viewModel::onErrorShown,
        onOpenResetPassword = viewModel::onOpenResetPassword,
        onCloseResetPassword = viewModel::onCloseResetPassword,
        onResetEmailChange = viewModel::onResetEmailChange,
        onResetNewPasswordChange = viewModel::onResetNewPasswordChange,
        onSubmitResetPassword = viewModel::onSubmitResetPassword
    )
}

/** Vista completamente pasiva: diseña Login y Crear Cuenta fiel a los lineamientos de accesibilidad. */
@Composable
fun AuthScreen(
    state: AuthUiState,
    onNombreChange: (String) -> Unit,
    onEmailChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    onTogglePasswordVisibility: () -> Unit,
    onSubmit: () -> Unit,
    onToggleMode: () -> Unit,
    onErrorShown: () -> Unit,
    onOpenResetPassword: () -> Unit = {},
    onCloseResetPassword: () -> Unit = {},
    onResetEmailChange: (String) -> Unit = {},
    onResetNewPasswordChange: (String) -> Unit = {},
    onSubmitResetPassword: () -> Unit = {}
) {
    val snackbarHostState = remember { SnackbarHostState() }
    val isRegister = state.mode == AuthMode.REGISTER

    BackHandler(enabled = isRegister) {
        onToggleMode()
    }

    LaunchedEffect(state.errorMessage) {
        state.errorMessage?.let {
            snackbarHostState.showSnackbar(it)
            onErrorShown()
        }
    }

    Scaffold(
        containerColor = AppBackground,
        snackbarHost = { SnackbarHost(snackbarHostState, modifier = Modifier.navigationBarsPadding()) },
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
                modifier = Modifier
                    .padding(padding)
                    .navigationBarsPadding()
            )
        } else {
            LoginContent(
                state = state,
                onEmailChange = onEmailChange,
                onPasswordChange = onPasswordChange,
                onTogglePasswordVisibility = onTogglePasswordVisibility,
                onSubmit = onSubmit,
                onToggleMode = onToggleMode,
                onOpenResetPassword = onOpenResetPassword,
                modifier = Modifier
                    .padding(padding)
                    .navigationBarsPadding()
            )
        }

        if (state.showResetPasswordDialog) {
            ResetPasswordDialog(
                email = state.resetEmail,
                newPassword = state.resetNewPassword,
                emailError = state.resetEmailError,
                passwordError = state.resetPasswordError,
                isSubmitting = state.isResettingPassword,
                onEmailChange = onResetEmailChange,
                onNewPasswordChange = onResetNewPasswordChange,
                onDismiss = onCloseResetPassword,
                onConfirm = onSubmitResetPassword
            )
        }
    }
}

@Composable
private fun RegisterTopBar(onBack: () -> Unit) {
    Column(
        modifier = Modifier
            .background(AppBackground)
            .statusBarsPadding()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = onBack,
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Volver a Iniciar Sesión",
                    tint = TextPrimary
                )
            }
            Spacer(Modifier.width(4.dp))
            MedBrandLogo(size = 38.dp, cornerRadius = 12.dp)
            Spacer(Modifier.width(12.dp))
            Text(
                text = "Crear Cuenta",
                fontSize = 20.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary,
                modifier = Modifier.weight(1f)
            )
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
    onOpenResetPassword: () -> Unit,
    modifier: Modifier = Modifier
) {
    val a11y = LocalAccessibilitySettings.current
    var isEntered by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) {
        isEntered = true
    }

    // Animación de pulso orgánico luminoso alrededor del logotipo
    val transition = rememberInfiniteTransition(label = "login_organic_pulse")
    val pulseScale by transition.animateFloat(
        initialValue = 0.96f,
        targetValue = 1.14f,
        animationSpec = infiniteRepeatable(
            animation = tween(2200, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_scale"
    )
    val pulseAlpha by transition.animateFloat(
        initialValue = 0.38f,
        targetValue = 0.12f,
        animationSpec = infiniteRepeatable(
            animation = tween(2200, easing = EaseInOutSine),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_alpha"
    )

    AnimatedVisibility(
        visible = isEntered,
        enter = fadeIn(animationSpec = tween(500)) + slideInVertically(
            initialOffsetY = { 35 },
            animationSpec = tween(500)
        )
    ) {
        Column(
            modifier = modifier
                .fillMaxSize()
                .imePadding()
                .padding(horizontal = 22.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(Modifier.height(10.dp))

            // Logo central con pulso orgánico luminoso y sutil halo clínico
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier.size(96.dp)
            ) {
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val cx = size.width / 2f
                    val cy = size.height / 2f
                    val pulseRadius = (size.width / 2f) * pulseScale

                    drawCircle(
                        brush = Brush.radialGradient(
                            colors = listOf(
                                if (a11y.isDarkTheme) Color(0xFF2DD4BF).copy(alpha = pulseAlpha)
                                else TealPrimary.copy(alpha = pulseAlpha),
                                if (a11y.isDarkTheme) Color(0xFF2DD4BF).copy(alpha = pulseAlpha * 0.3f)
                                else TealPrimary.copy(alpha = pulseAlpha * 0.3f),
                                Color.Transparent
                            ),
                            center = Offset(cx, cy),
                            radius = pulseRadius
                        ),
                        radius = pulseRadius,
                        center = Offset(cx, cy)
                    )
                }
                MedBrandLogo(size = 68.dp, cornerRadius = 22.dp)
            }

            Spacer(Modifier.height(8.dp))

            Text(
                text = "MedReminder AI",
                fontSize = 26.sp,
                fontWeight = FontWeight.ExtraBold,
                color = a11y.adaptiveTextPrimary,
                letterSpacing = (-0.5).sp
            )

            Spacer(Modifier.height(4.dp))

            Text(
                text = "Tu plan de medicación, seguro, puntual y siempre a tu lado.",
                fontSize = 14.sp,
                color = a11y.adaptiveTextSecondary,
                textAlign = TextAlign.Center,
                lineHeight = 19.sp
            )

            Spacer(Modifier.height(12.dp))

            // Tarjeta de bienvenida de la mascota amigable Medi
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = a11y.adaptiveSoftSurface,
                border = BorderStroke(
                    width = a11y.borderWidth,
                    color = if (a11y.isHighContrast) a11y.adaptiveBorder else TealPrimary.copy(alpha = 0.25f)
                ),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    MediMascotView(
                        size = 38.dp,
                        mood = MediMood.HAPPY
                    )
                    Spacer(Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "Medi te da la bienvenida",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = a11y.adaptiveTextPrimary
                            )
                            Spacer(Modifier.width(5.dp))
                            Box(
                                modifier = Modifier
                                    .size(6.dp)
                                    .clip(CircleShape)
                                    .background(if (a11y.isDarkTheme) Color(0xFF10B981) else Color(0xFF2E7D32))
                            )
                        }
                        Spacer(Modifier.height(2.dp))
                        Text(
                            text = "Inicia sesión para revisar tus tomas de hoy y cuidar tu racha.",
                            fontSize = 12.sp,
                            color = a11y.adaptiveTextSecondary,
                            lineHeight = 16.sp
                        )
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Fila de píldoras de valor clínico (CERO EMOJIS, vectores limpios)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                listOf(
                    Icons.Outlined.AccessAlarm to "Alarmas",
                    Icons.Outlined.Shield to "Cifrado",
                    Icons.Outlined.CheckCircle to "Rachas"
                ).forEach { (icon, label) ->
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = if (a11y.isDarkTheme) Color(0xFF142024) else TealBadgeBg.copy(alpha = 0.45f),
                        border = BorderStroke(1.dp, if (a11y.isHighContrast) a11y.adaptiveBorder else InputBorderColor),
                        modifier = Modifier.weight(1f)
                    ) {
                        Row(
                            modifier = Modifier.padding(vertical = 5.dp, horizontal = 6.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.Center
                        ) {
                            Icon(
                                imageVector = icon,
                                contentDescription = null,
                                tint = if (a11y.isDarkTheme) Color(0xFF2DD4BF) else TealDark,
                                modifier = Modifier.size(13.dp)
                            )
                            Spacer(Modifier.width(4.dp))
                            Text(
                                text = label,
                                fontSize = 11.5.sp,
                                fontWeight = FontWeight.Bold,
                                color = a11y.adaptiveTextPrimary
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(14.dp))

            // Campo Correo electrónico
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Outlined.Email,
                    contentDescription = null,
                    tint = a11y.adaptivePrimary,
                    modifier = Modifier.size(17.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = "Correo electrónico",
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 14.5.sp,
                    color = a11y.adaptiveTextPrimary
                )
            }
            Spacer(Modifier.height(6.dp))
            ClinicalTextField(
                value = state.email,
                onValueChange = onEmailChange,
                placeholder = "ejemplo@correo.com",
                error = state.emailError,
                enabled = !state.isLoading,
                keyboardType = KeyboardType.Email
            )

            Spacer(Modifier.height(12.dp))

            // Campo Contraseña + Botón accesible "¿La olvidaste?"
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Outlined.Lock,
                        contentDescription = null,
                        tint = a11y.adaptivePrimary,
                        modifier = Modifier.size(17.dp)
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = "Contraseña",
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 14.5.sp,
                        color = a11y.adaptiveTextPrimary
                    )
                }
                Box(
                    modifier = Modifier
                        .heightIn(min = 40.dp)
                        .clip(RoundedCornerShape(10.dp))
                        .clickable(enabled = !state.isLoading) { onOpenResetPassword() }
                        .padding(horizontal = 6.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "¿La olvidaste?",
                        fontSize = 13.5.sp,
                        fontWeight = FontWeight.Bold,
                        color = if (a11y.isDarkTheme) Color(0xFF2DD4BF) else TealPrimary
                    )
                }
            }
            Spacer(Modifier.height(4.dp))
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
                            tint = a11y.adaptiveTextSecondary
                        )
                    }
                }
            )

            Spacer(Modifier.height(18.dp))

            // Botón Iniciar Sesión (>= 54dp, con feedback de carga)
            Button(
                onClick = onSubmit,
                enabled = !state.isLoading,
                shape = RoundedCornerShape(18.dp),
                colors = ButtonDefaults.buttonColors(containerColor = a11y.adaptivePrimary),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 54.dp)
            ) {
                if (state.isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(22.dp),
                        color = Color.White,
                        strokeWidth = 2.dp
                    )
                } else {
                    Text(
                        text = "Iniciar Sesión",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Spacer(Modifier.width(8.dp))
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(19.dp)
                    )
                }
            }

            Spacer(Modifier.height(10.dp))

            // Enlace "¿No tienes cuenta? Regístrate"
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 44.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .clickable(enabled = !state.isLoading) { onToggleMode() },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = buildAnnotatedString {
                        withStyle(SpanStyle(color = a11y.adaptiveTextSecondary, fontWeight = FontWeight.SemiBold)) {
                            append("¿No tienes cuenta? ")
                        }
                        withStyle(
                            SpanStyle(
                                color = if (a11y.isDarkTheme) Color(0xFF2DD4BF) else TealDark,
                                fontWeight = FontWeight.Bold,
                                textDecoration = TextDecoration.Underline
                            )
                        ) {
                            append("Regístrate")
                        }
                    },
                    fontSize = 14.5.sp
                )
            }

            Spacer(Modifier.height(12.dp))
        }
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

        Text(
            text = "Tu bienestar empieza aquí",
            fontSize = 26.sp,
            fontWeight = FontWeight.ExtraBold,
            color = TextPrimary
        )

        Spacer(Modifier.height(6.dp))

        Text(
            text = "Configura tu perfil en un solo paso para recibir recordatorios puntuales y llevar tu racha de salud.",
            fontSize = 15.sp,
            color = TextSecondary,
            lineHeight = 21.sp
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

        // Contraseña (ortografía corregida: "caracteres")
        FieldLabelRow(label = "Contraseña", rightHint = "Mín. 8 caracteres")
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
            shape = RoundedCornerShape(20.dp),
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

        // Botón Crear Cuenta (>= 60dp)
        Button(
            onClick = onSubmit,
            enabled = !state.isLoading,
            shape = RoundedCornerShape(20.dp),
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
                    text = "Crear Cuenta",
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
                .clip(RoundedCornerShape(14.dp))
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
private fun ResetPasswordDialog(
    email: String,
    newPassword: String,
    emailError: String?,
    passwordError: String?,
    isSubmitting: Boolean,
    onEmailChange: (String) -> Unit,
    onNewPasswordChange: (String) -> Unit,
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
            shadowElevation = 10.dp,
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
                        text = "Recuperar Contraseña",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                    IconButton(onClick = onDismiss, enabled = !isSubmitting) {
                        Icon(
                            imageVector = Icons.Default.Close,
                            contentDescription = "Cerrar",
                            tint = TextSecondary
                        )
                    }
                }
                Spacer(Modifier.height(6.dp))
                Text(
                    text = "Ingresa el correo electrónico de tu cuenta y define tu nueva contraseña segura (mínimo 8 caracteres).",
                    fontSize = 13.5.sp,
                    color = TextSecondary,
                    lineHeight = 19.sp
                )
                Spacer(Modifier.height(16.dp))

                FieldLabelRow(label = "Correo registrado", rightHint = "Requerido")
                Spacer(Modifier.height(6.dp))
                ClinicalTextField(
                    value = email,
                    onValueChange = onEmailChange,
                    placeholder = "ejemplo@correo.com",
                    error = emailError,
                    enabled = !isSubmitting,
                    keyboardType = KeyboardType.Email,
                    leadingIcon = Icons.Outlined.Email
                )

                Spacer(Modifier.height(14.dp))

                FieldLabelRow(label = "Nueva contraseña", rightHint = "Mín. 8 caracteres")
                Spacer(Modifier.height(6.dp))
                ClinicalTextField(
                    value = newPassword,
                    onValueChange = onNewPasswordChange,
                    placeholder = "Nueva contraseña segura",
                    error = passwordError,
                    enabled = !isSubmitting,
                    keyboardType = KeyboardType.Password,
                    leadingIcon = Icons.Outlined.Lock,
                    visualTransformation = PasswordVisualTransformation()
                )

                Spacer(Modifier.height(22.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedButton(
                        onClick = onDismiss,
                        enabled = !isSubmitting,
                        shape = RoundedCornerShape(16.dp),
                        border = BorderStroke(1.dp, InputBorderColor),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 56.dp)
                    ) {
                        Text("Cancelar", fontWeight = FontWeight.Bold, color = TextSecondary)
                    }
                    Button(
                        onClick = onConfirm,
                        enabled = !isSubmitting,
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = TealPrimary),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 56.dp)
                    ) {
                        if (isSubmitting) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(20.dp),
                                color = Color.White,
                                strokeWidth = 2.dp
                            )
                        } else {
                            Text("Actualizar", fontWeight = FontWeight.Bold, color = Color.White)
                        }
                    }
                }
            }
        }
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
            shape = RoundedCornerShape(18.dp),
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
                shape = RoundedCornerShape(18.dp),
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

