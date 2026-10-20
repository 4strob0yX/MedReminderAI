package com.medreminder.ai.notifications

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.Locale

/**
 * Gestor nativo offline/online de Reconocimiento de Voz y Dictado (Speech-to-Text) en español.
 * Permite a Medi "escuchar" la voz del usuario para hacer consultas clínicas o interactuar de forma intuitiva.
 */
object VoiceInputHelper {
    private var speechRecognizer: SpeechRecognizer? = null
    private val mainHandler = Handler(Looper.getMainLooper())

    private val _isListening = MutableStateFlow(false)
    val isListening: StateFlow<Boolean> = _isListening.asStateFlow()

    private val _liveSpokenText = MutableStateFlow("")
    val liveSpokenText: StateFlow<String> = _liveSpokenText.asStateFlow()

    private val _soundLevel = MutableStateFlow(0f)
    val soundLevel: StateFlow<Float> = _soundLevel.asStateFlow()

    private val _lastError = MutableStateFlow<String?>(null)
    val lastError: StateFlow<String?> = _lastError.asStateFlow()

    private var activeCallback: ((String) -> Unit)? = null
    private var activeErrorCallback: ((String) -> Unit)? = null

    fun isAvailable(context: Context): Boolean {
        return SpeechRecognizer.isRecognitionAvailable(context) ||
            SpeechRecognizer.isRecognitionAvailable(context.applicationContext)
    }

    /**
     * Construye un Intent nativo de reconocimiento del sistema para usar con
     * ActivityResultLauncher en caso de requerir diálogo del sistema operativo.
     */
    fun createSystemSpeechIntent(promptText: String = "Habla con Medi..."): Intent {
        val currentLocale = Locale.getDefault()
        return Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, currentLocale.toLanguageTag().ifBlank { "es-MX" })
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "es-MX")
            putExtra(RecognizerIntent.EXTRA_PROMPT, promptText)
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
        }
    }

    /**
     * Inicia la escucha por micrófono del usuario en español con detección en tiempo real.
     * @param onResult Callback que recibe el texto final dictado por el usuario.
     * @param onError Callback que recibe el mensaje de error para activar fallback si falla.
     */
    fun startListening(
        context: Context,
        onError: ((String) -> Unit)? = null,
        onResult: (String) -> Unit
    ) {
        val appContext = context.applicationContext

        mainHandler.post {
            cleanup()
            activeCallback = onResult
            activeErrorCallback = onError
            _liveSpokenText.value = ""
            _lastError.value = null
            _soundLevel.value = 0f

            val isAvailable = SpeechRecognizer.isRecognitionAvailable(context) ||
                SpeechRecognizer.isRecognitionAvailable(appContext)

            if (!isAvailable) {
                val err = "Reconocimiento de voz no disponible en este dispositivo"
                _lastError.value = err
                android.util.Log.w("MedReminderSTT", "SpeechRecognizer no disponible en el sistema")
                onError?.invoke(err)
                return@post
            }

            try {
                // Intentar primero con el contexto directo (necesario en Android 11+ para resolver el servicio de reconocimiento)
                val recognizer = runCatching {
                    SpeechRecognizer.createSpeechRecognizer(context)
                }.getOrElse {
                    SpeechRecognizer.createSpeechRecognizer(appContext)
                }

                speechRecognizer = recognizer

                val currentLang = Locale.getDefault().toLanguageTag().ifBlank { "es-MX" }
                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, currentLang)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, currentLang)
                    putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, context.packageName)
                    putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                    putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                    putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 2000L)
                    putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 1500L)
                }

                recognizer.setRecognitionListener(object : RecognitionListener {
                    override fun onReadyForSpeech(params: Bundle?) {
                        _isListening.value = true
                        _lastError.value = null
                        android.util.Log.i("MedReminderSTT", "Micrófono listo. Escuchando en $currentLang...")
                    }

                    override fun onBeginningOfSpeech() {
                        _isListening.value = true
                        _lastError.value = null
                    }

                    override fun onRmsChanged(rmsdB: Float) {
                        val normalized = ((rmsdB + 2f) / 14f).coerceIn(0f, 1f)
                        _soundLevel.value = normalized
                    }

                    override fun onBufferReceived(buffer: ByteArray?) {}

                    override fun onEndOfSpeech() {
                        _soundLevel.value = 0f
                        android.util.Log.i("MedReminderSTT", "Fin del habla detectado.")
                    }

                    override fun onError(error: Int) {
                        _isListening.value = false
                        _soundLevel.value = 0f
                        val errorMsg = when (error) {
                            SpeechRecognizer.ERROR_NO_MATCH -> "No se reconoció ninguna frase. Intenta de nuevo."
                            SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "No se detectó audio."
                            SpeechRecognizer.ERROR_AUDIO -> "Error de audio al acceder al micrófono."
                            SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Permiso de micrófono no otorgado."
                            SpeechRecognizer.ERROR_NETWORK, SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "Sin conexión para el servicio de voz."
                            SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "Micrófono ocupado."
                            SpeechRecognizer.ERROR_CLIENT -> "El servicio de voz local no respondió."
                            else -> "No fue posible escuchar ($error)."
                        }
                        _lastError.value = errorMsg
                        android.util.Log.w("MedReminderSTT", "Error STT ($error): $errorMsg")
                        val errCb = activeErrorCallback
                        cleanup()
                        errCb?.invoke(errorMsg)
                    }

                    override fun onResults(results: Bundle?) {
                        _isListening.value = false
                        _soundLevel.value = 0f
                        val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        val text = matches?.firstOrNull()?.trim() ?: ""
                        val cb = activeCallback
                        cleanup()
                        if (text.isNotBlank()) {
                            _liveSpokenText.value = text
                            android.util.Log.i("MedReminderSTT", "Texto reconocido con éxito: $text")
                            cb?.invoke(text)
                        }
                    }

                    override fun onPartialResults(partialResults: Bundle?) {
                        val partials = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        val partial = partials?.firstOrNull()?.trim() ?: ""
                        if (partial.isNotBlank()) {
                            _liveSpokenText.value = partial
                        }
                    }

                    override fun onEvent(eventType: Int, params: Bundle?) {}
                })

                recognizer.startListening(intent)
            } catch (e: Exception) {
                android.util.Log.e("MedReminderSTT", "Error al inicializar SpeechRecognizer", e)
                _isListening.value = false
                _lastError.value = "No se pudo activar el micrófono: ${e.localizedMessage ?: "error desconocido"}"
                cleanup()
            }
        }
    }

    /**
     * Termina la captura de audio pero conserva el reconocedor para procesar el resultado final.
     */
    fun stopListening() {
        mainHandler.post {
            try {
                speechRecognizer?.stopListening()
            } catch (_: Exception) {
                cleanup()
            }
        }
    }

    fun cancel() {
        mainHandler.post {
            try {
                speechRecognizer?.cancel()
            } catch (_: Exception) {}
            cleanup()
        }
    }

    private fun cleanup() {
        _isListening.value = false
        _soundLevel.value = 0f
        try {
            speechRecognizer?.destroy()
        } catch (_: Exception) {}
        speechRecognizer = null
        activeCallback = null
        activeErrorCallback = null
    }
}
