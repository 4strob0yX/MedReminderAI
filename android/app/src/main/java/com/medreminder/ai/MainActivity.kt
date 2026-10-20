package com.medreminder.ai

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.core.content.ContextCompat
import com.medreminder.ai.ui.auth.AuthRoute
import com.medreminder.ai.ui.auth.AuthViewModel
import com.medreminder.ai.ui.components.MediSplashScreen
import com.medreminder.ai.ui.home.HomeRoute
import com.medreminder.ai.ui.home.HomeViewModel
import com.medreminder.ai.ui.theme.MedReminderAITheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(
                android.graphics.Color.TRANSPARENT,
                android.graphics.Color.TRANSPARENT
            ),
            navigationBarStyle = SystemBarStyle.light(
                android.graphics.Color.TRANSPARENT,
                android.graphics.Color.TRANSPARENT
            )
        )

        val appContainer = (application as MedReminderApp).container
        val authViewModel: AuthViewModel by viewModels {
            AuthViewModel.Factory(appContainer.authRepository)
        }
        val homeViewModel: HomeViewModel by viewModels {
            HomeViewModel.Factory(appContainer.medRepository)
        }

        // Calentar motor TextToSpeech para respuesta instantánea de lectura
        com.medreminder.ai.notifications.TtsHelper.init(this)

        setContent {
            MedReminderAITheme {
                val authState by authViewModel.state.collectAsState()
                var splashCompleted by remember { mutableStateOf(false) }

                val notificationPermissionLauncher = rememberLauncherForActivityResult(
                    contract = ActivityResultContracts.RequestPermission()
                ) { _ -> }

                LaunchedEffect(authState.isAuthenticated) {
                    if (authState.isAuthenticated) {
                        homeViewModel.cargarDatos()
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                            val granted = ContextCompat.checkSelfPermission(
                                this@MainActivity,
                                Manifest.permission.POST_NOTIFICATIONS
                            ) == PackageManager.PERMISSION_GRANTED
                            if (!granted) {
                                notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
                            }
                        }
                    } else {
                        homeViewModel.limpiarSesion()
                    }
                }

                Box(modifier = Modifier.fillMaxSize()) {
                    // Capa base: la aplicación principal se renderiza y precarga sus datos en segundo plano
                    if (authState.isAuthenticated) {
                        HomeRoute(
                            viewModel = homeViewModel,
                            onLogout = {
                                homeViewModel.limpiarSesion()
                                authViewModel.logout()
                            }
                        )
                    } else {
                        AuthRoute(
                            viewModel = authViewModel,
                            onAuthenticated = {
                                // Handled reactively by LaunchedEffect(authState.isAuthenticated)
                            }
                        )
                    }

                    // Capa superior: Animación de entrada estilo YouTube con nuestra mascota Medi
                    if (!splashCompleted) {
                        MediSplashScreen(
                            onSplashFinished = {
                                splashCompleted = true
                            },
                            minDisplayTimeMillis = 1800L
                        )
                    }
                }
            }
        }
    }
}
