package com.medreminder.ai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import com.medreminder.ai.ui.auth.AuthRoute
import com.medreminder.ai.ui.auth.AuthViewModel
import com.medreminder.ai.ui.home.HomeRoute
import com.medreminder.ai.ui.home.HomeViewModel
import com.medreminder.ai.ui.theme.MedReminderAITheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val appContainer = (application as MedReminderApp).container
        val authViewModel: AuthViewModel by viewModels {
            AuthViewModel.Factory(appContainer.authRepository)
        }
        val homeViewModel: HomeViewModel by viewModels {
            HomeViewModel.Factory(appContainer.medRepository)
        }

        setContent {
            MedReminderAITheme {
                val authState by authViewModel.state.collectAsState()

                if (authState.isAuthenticated) {
                    HomeRoute(
                        viewModel = homeViewModel,
                        onLogout = { authViewModel.logout() }
                    )
                } else {
                    AuthRoute(
                        viewModel = authViewModel,
                        onAuthenticated = {
                            homeViewModel.cargarDatos()
                        }
                    )
                }
            }
        }
    }
}