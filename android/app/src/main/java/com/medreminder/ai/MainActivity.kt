package com.medreminder.ai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.medreminder.ai.ui.theme.MedReminderAITheme

import androidx.activity.viewModels
import com.medreminder.ai.ui.auth.AuthRoute
import com.medreminder.ai.ui.auth.AuthViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val appContainer = (application as MedReminderApp).container
        val authViewModel: AuthViewModel by viewModels {
            AuthViewModel.Factory(appContainer.authRepository)
        }

        setContent {
            MedReminderAITheme {
                AuthRoute(
                    viewModel = authViewModel,
                    onAuthenticated = {
                        // Navegación a Home pendiente de directiva
                    }
                )
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MedReminderAITheme {
        Greeting("Android")
    }
}