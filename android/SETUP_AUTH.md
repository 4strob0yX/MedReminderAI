# Auth skeleton: configuración requerida

## `app/build.gradle.kts`
```kotlin
android {
    buildFeatures { compose = true; buildConfig = true }
    defaultConfig {
        // 10.0.2.2 = localhost del host desde el emulador
        buildConfigField("String", "API_BASE_URL", "\"http://10.0.2.2:8000/\"")
    }
    buildTypes {
        release {
            buildConfigField("String", "API_BASE_URL", "\"https://api.tudominio.com/\"")
        }
    }
}
dependencies {
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.4")
}
```

## `AndroidManifest.xml`
```xml
<uses-permission android:name="android.permission.INTERNET" />
<application android:name=".MedReminderApp"
    android:usesCleartextTraffic="true"> <!-- SOLO debug; mover a src/debug/ antes de release -->
```

## `MedReminderApp.kt`
```kotlin
class MedReminderApp : Application() {
    lateinit var container: AppContainer
    override fun onCreate() { super.onCreate(); container = AppContainer(this) }
}
```

## Uso en `MainActivity`
```kotlin
val container = (application as MedReminderApp).container
val vm: AuthViewModel by viewModels { AuthViewModel.Factory(container.authRepository) }
setContent { MaterialTheme { AuthRoute(vm, onAuthenticated = { /* navegar a Home */ }) } }
```

## Contrato esperado del backend
- `POST /auth/register` `{nombre, email, password}` -> `{access_token, refresh_token, token_type}`
- `POST /auth/login` `{email, password}` -> mismo formato
- Errores: `{"detail": "..."}`
