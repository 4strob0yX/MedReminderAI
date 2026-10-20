package com.medreminder.ai.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.medreminder.ai.data.repository.AuthRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

enum class AuthMode { LOGIN, REGISTER }

data class AuthUiState(
    val mode: AuthMode = AuthMode.LOGIN,
    val nombre: String = "",
    val email: String = "",
    val password: String = "",
    val passwordVisible: Boolean = false,
    val nombreError: String? = null,
    val emailError: String? = null,
    val passwordError: String? = null,
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val isAuthenticated: Boolean = false,
    val showResetPasswordDialog: Boolean = false,
    val resetEmail: String = "",
    val resetNewPassword: String = "",
    val resetEmailError: String? = null,
    val resetPasswordError: String? = null,
    val isResettingPassword: Boolean = false
)

/** Toda la lógica (validación, modo, llamadas) vive aquí; la vista es pasiva. */
class AuthViewModel(private val repository: AuthRepository) : ViewModel() {

    private val _state = MutableStateFlow(AuthUiState(isAuthenticated = repository.isLoggedIn()))
    val state: StateFlow<AuthUiState> = _state.asStateFlow()

    fun onNombreChange(v: String) = _state.update { it.copy(nombre = v, nombreError = null, errorMessage = null) }
    fun onEmailChange(v: String) = _state.update { it.copy(email = v.trim(), emailError = null, errorMessage = null) }
    fun onPasswordChange(v: String) = _state.update { it.copy(password = v, passwordError = null, errorMessage = null) }
    fun onTogglePasswordVisibility() = _state.update { it.copy(passwordVisible = !it.passwordVisible) }
    fun onErrorShown() = _state.update { it.copy(errorMessage = null) }

    fun onToggleMode() = _state.update {
        AuthUiState(mode = if (it.mode == AuthMode.LOGIN) AuthMode.REGISTER else AuthMode.LOGIN, email = it.email)
    }

    fun onOpenResetPassword() = _state.update {
        it.copy(
            showResetPasswordDialog = true,
            resetEmail = it.email,
            resetNewPassword = "",
            resetEmailError = null,
            resetPasswordError = null
        )
    }

    fun onCloseResetPassword() = _state.update {
        if (it.isResettingPassword) it else it.copy(showResetPasswordDialog = false)
    }

    fun onResetEmailChange(v: String) = _state.update {
        it.copy(resetEmail = v.trim(), resetEmailError = null)
    }

    fun onResetNewPasswordChange(v: String) = _state.update {
        it.copy(resetNewPassword = v, resetPasswordError = null)
    }

    fun onSubmitResetPassword() {
        val s = _state.value
        if (s.isResettingPassword) return

        val emailErr = if (!android.util.Patterns.EMAIL_ADDRESS.matcher(s.resetEmail).matches()) {
            "Ingresa un correo electrónico válido"
        } else null
        val passErr = if (s.resetNewPassword.length < 8) {
            "La nueva contraseña debe tener mínimo 8 caracteres"
        } else null

        if (emailErr != null || passErr != null) {
            _state.update { it.copy(resetEmailError = emailErr, resetPasswordError = passErr) }
            return
        }

        _state.update { it.copy(isResettingPassword = true, errorMessage = null) }
        viewModelScope.launch {
            val res = repository.resetPassword(s.resetEmail, s.resetNewPassword)
            _state.update {
                res.fold(
                    onSuccess = { msg ->
                        it.copy(
                            isResettingPassword = false,
                            showResetPasswordDialog = false,
                            email = s.resetEmail,
                            password = "",
                            errorMessage = msg
                        )
                    },
                    onFailure = { err ->
                        it.copy(
                            isResettingPassword = false,
                            resetPasswordError = err.message ?: "No se pudo restablecer la contraseña"
                        )
                    }
                )
            }
        }
    }

    fun logout() {
        repository.logout()
        _state.value = AuthUiState(isAuthenticated = false)
    }

    fun onSubmit() {
        val s = _state.value
        if (s.isLoading || !validate(s)) return

        _state.update { it.copy(isLoading = true, errorMessage = null) }
        viewModelScope.launch {
            val result = when (s.mode) {
                AuthMode.LOGIN -> repository.login(s.email, s.password)
                AuthMode.REGISTER -> repository.register(s.nombre.trim(), s.email, s.password)
            }
            _state.update {
                result.fold(
                    onSuccess = { _ -> it.copy(isLoading = false, isAuthenticated = true) },
                    onFailure = { e -> it.copy(isLoading = false, errorMessage = e.message) }
                )
            }
        }
    }

    private fun validate(s: AuthUiState): Boolean {
        val nombreErr = if (s.mode == AuthMode.REGISTER && s.nombre.isBlank()) "Ingresa tu nombre" else null
        val emailErr = if (!android.util.Patterns.EMAIL_ADDRESS.matcher(s.email).matches()) "Correo no válido" else null
        val passErr = when {
            s.password.isEmpty() -> "Ingresa tu contraseña"
            s.mode == AuthMode.REGISTER && s.password.length < 8 -> "Mínimo 8 caracteres"
            else -> null
        }
        _state.update { it.copy(nombreError = nombreErr, emailError = emailErr, passwordError = passErr) }
        return nombreErr == null && emailErr == null && passErr == null
    }

    class Factory(private val repository: AuthRepository) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T = AuthViewModel(repository) as T
    }
}

