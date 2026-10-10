package com.medreminder.ai.ui.auth

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

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

/** Vista completamente pasiva: solo renderiza estado y emite eventos. */
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

    Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 24.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically)
        ) {
            Text(
                text = if (isRegister) "Crear cuenta" else "Iniciar sesión",
                style = MaterialTheme.typography.headlineLarge
            )

            if (isRegister) {
                AuthField(
                    value = state.nombre,
                    onChange = onNombreChange,
                    label = "Nombre completo",
                    error = state.nombreError,
                    enabled = !state.isLoading
                )
            }

            AuthField(
                value = state.email,
                onChange = onEmailChange,
                label = "Correo electrónico",
                error = state.emailError,
                enabled = !state.isLoading,
                keyboardType = KeyboardType.Email
            )

            AuthField(
                value = state.password,
                onChange = onPasswordChange,
                label = "Contraseña",
                error = state.passwordError,
                enabled = !state.isLoading,
                keyboardType = KeyboardType.Password,
                visualTransformation = if (state.passwordVisible) VisualTransformation.None
                else PasswordVisualTransformation(),
                trailing = {
                    TextButton(
                        onClick = onTogglePasswordVisibility,
                        modifier = Modifier.heightIn(min = 48.dp)
                    ) { Text(if (state.passwordVisible) "Ocultar" else "Mostrar") }
                }
            )

            Spacer(Modifier.height(8.dp))

            // Botón grande (>=56dp) y deshabilitado mientras carga: evita doble toque.
            Button(
                onClick = onSubmit,
                enabled = !state.isLoading,
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 56.dp)
            ) {
                if (state.isLoading) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.dp)
                } else {
                    Text(if (isRegister) "Registrarme" else "Entrar", fontSize = 18.sp)
                }
            }

            TextButton(
                onClick = onToggleMode,
                enabled = !state.isLoading,
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 56.dp)
            ) {
                Text(
                    if (isRegister) "¿Ya tienes cuenta? Inicia sesión"
                    else "¿No tienes cuenta? Regístrate",
                    fontSize = 16.sp
                )
            }
        }
    }
}

@Composable
private fun AuthField(
    value: String,
    onChange: (String) -> Unit,
    label: String,
    error: String?,
    enabled: Boolean,
    keyboardType: KeyboardType = KeyboardType.Text,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    trailing: @Composable (() -> Unit)? = null
) {
    OutlinedTextField(
        value = value,
        onValueChange = onChange,
        label = { Text(label) },
        isError = error != null,
        supportingText = error?.let { { Text(it) } },
        singleLine = true,
        enabled = enabled,
        keyboardOptions = KeyboardOptions(keyboardType = keyboardType),
        visualTransformation = visualTransformation,
        trailingIcon = trailing,
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 64.dp)
    )
}
