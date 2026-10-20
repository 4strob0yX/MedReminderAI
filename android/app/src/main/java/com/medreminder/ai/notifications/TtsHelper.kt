package com.medreminder.ai.notifications

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioManager
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import com.medreminder.ai.ui.theme.AccessibilityPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.Locale

/**
 * Asistente nativo offline de lectura en voz alta (TextToSpeech) en español.
 * Diseñado con retroalimentación visual reactiva (StateFlow), audio attributes de accesibilidad
 * y soporte de reproducción/pausa inmediata (toggle) con 1 toque.
 */
object TtsHelper {
    private var tts: TextToSpeech? = null
    @Volatile
    private var isReady: Boolean = false
    @Volatile
    private var isInitializing: Boolean = false
    private var pendingUtterance: String? = null
    private var pendingKey: String? = null
    private var pendingCallback: (() -> Unit)? = null
    @Volatile
    private var currentUtteranceId: String? = null

    // Estados reactivos observables por Jetpack Compose para animar ondas de voz e iconos
    private val _isSpeaking = MutableStateFlow(false)
    val isSpeaking: StateFlow<Boolean> = _isSpeaking.asStateFlow()

    private val _currentKey = MutableStateFlow<String?>(null)
    val currentKey: StateFlow<String?> = _currentKey.asStateFlow()

    private val _currentText = MutableStateFlow<String?>(null)
    val currentText: StateFlow<String?> = _currentText.asStateFlow()

    /**
     * Pre-inicializa el motor TextToSpeech en segundo plano para que al pulsar cualquier botón
     * de escucha la respuesta de audio sea instantánea (sin lag de carga).
     */
    fun init(context: Context) {
        if (isReady || isInitializing) return
        val appContext = context.applicationContext
        synchronized(this) {
            if (isReady || isInitializing) return
            isInitializing = true
            createEngine(appContext)
        }
    }

    /**
     * Lee en voz alta el texto indicado en español.
     * Si ya se está reproduciendo el MISMO `key`, se detiene de inmediato (comportamiento toggle).
     *
     * @param key Identificador semántico de lo que se lee (ej. "plan", "toma_12", "medi_dialog").
     * @param force Si es true (por defecto), habla aunque vozActiva esté en preferencias desactivado.
     */
    fun speak(
        context: Context,
        text: String,
        key: String = "general",
        force: Boolean = true,
        onDispatched: (() -> Unit)? = null
    ) {
        if (text.isBlank()) {
            onDispatched?.invoke()
            return
        }

        // Si ya está leyendo exactamente este elemento, el usuario volvió a pulsar para detenerlo
        if (_isSpeaking.value && _currentKey.value == key) {
            stop()
            onDispatched?.invoke()
            return
        }

        val appContext = context.applicationContext
        AccessibilityPreferences.ensureLoaded(appContext)
        if (!force && !AccessibilityPreferences.state.value.vozActiva) {
            onDispatched?.invoke()
            return
        }

        // Asegurar que el volumen multimedia no esté silenciado en el sistema
        ensureAudibleVolume(appContext)

        synchronized(this) {
            val engine = tts
            if (engine != null && isReady) {
                _currentKey.value = key
                _currentText.value = text
                _isSpeaking.value = true

                val params = Bundle().apply {
                    putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, 1.0f)
                }

                val utteranceId = "med_${key}_${System.currentTimeMillis()}"
                currentUtteranceId = utteranceId
                android.util.Log.i("MedReminderTTS", "TTS despachando ($key): $text")

                val res = engine.speak(
                    text,
                    TextToSpeech.QUEUE_FLUSH,
                    params,
                    utteranceId
                )

                if (res != TextToSpeech.ERROR) {
                    onDispatched?.invoke()
                    return
                }

                // Si falló por desvinculación del servicio, reintentamos reiniciar
                runCatching { engine.shutdown() }
                tts = null
                isReady = false
            }

            pendingUtterance = text
            pendingKey = key
            val previousCallback = pendingCallback
            pendingCallback = if (previousCallback != null && onDispatched != null) {
                {
                    previousCallback.invoke()
                    onDispatched.invoke()
                }
            } else {
                onDispatched ?: previousCallback
            }

            if (isInitializing) return
            isInitializing = true
            createEngine(appContext)
        }
    }

    private fun ensureAudibleVolume(context: Context) {
        try {
            val am = context.getSystemService(Context.AUDIO_SERVICE) as? AudioManager ?: return
            val currentVol = am.getStreamVolume(AudioManager.STREAM_MUSIC)
            val maxVol = am.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
            if (currentVol == 0 && maxVol > 0) {
                // Si el usuario tenía el volumen multimedia en 0, lo elevamos suavemente al 60%
                val audibleVol = (maxVol * 0.60f).toInt().coerceAtLeast(1)
                am.setStreamVolume(AudioManager.STREAM_MUSIC, audibleVol, 0)
                android.util.Log.i("MedReminderTTS", "Volumen multimedia elevado de 0 a $audibleVol/$maxVol para accesibilidad")
            }
        } catch (e: Exception) {
            android.util.Log.w("MedReminderTTS", "No se pudo ajustar volumen: ${e.message}")
        }
    }

    private fun createEngine(appContext: Context) {
        android.util.Log.i("MedReminderTTS", "Iniciando motor TextToSpeech...")
        val holder = arrayOfNulls<TextToSpeech>(1)
        val created = TextToSpeech(appContext) { status ->
            val engine = holder[0] ?: tts
            if (engine != null) handleInit(engine, status)
        }
        holder[0] = created
        tts = created
    }

    private fun handleInit(instance: TextToSpeech, status: Int) {
        run {
            var callbackToInvoke: (() -> Unit)? = null
            synchronized(this@TtsHelper) {
                isInitializing = false
                callbackToInvoke = pendingCallback
                pendingCallback = null

                if (status == TextToSpeech.SUCCESS) {
                    if (tts === instance) {
                        configureAudioAttributes(instance)
                        configureLanguage(instance)
                        setupProgressListener(instance)

                        instance.setSpeechRate(0.95f)
                        instance.setPitch(1.0f)
                        isReady = true
                        android.util.Log.i("MedReminderTTS", "TTS inicializado con éxito.")

                        val queued = pendingUtterance
                        val queuedKey = pendingKey ?: "general"
                        if (queued != null) {
                            pendingUtterance = null
                            pendingKey = null
                            _currentKey.value = queuedKey
                            _currentText.value = queued
                            _isSpeaking.value = true

                            val params = Bundle().apply {
                                putFloat(TextToSpeech.Engine.KEY_PARAM_VOLUME, 1.0f)
                            }
                            val queuedId = "med_${queuedKey}_${System.currentTimeMillis()}"
                            currentUtteranceId = queuedId
                            val qres = instance.speak(queued, TextToSpeech.QUEUE_FLUSH, params, queuedId)
                            if (qres == TextToSpeech.ERROR) {
                                _isSpeaking.value = false
                                _currentKey.value = null
                                _currentText.value = null
                            }
                        }
                    }
                } else {
                    isReady = false
                    _isSpeaking.value = false
                    _currentKey.value = null
                    _currentText.value = null
                    android.util.Log.w("MedReminderTTS", "Fallo al inicializar TextToSpeech. Status: $status")
                }
            }
            callbackToInvoke?.invoke()
        }
    }

    private fun configureAudioAttributes(instance: TextToSpeech) {
        try {
            val audioAttributes = AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                .build()
            instance.setAudioAttributes(audioAttributes)
        } catch (e: Exception) {
            android.util.Log.w("MedReminderTTS", "Error configurando AudioAttributes: ${e.message}")
        }
    }

    private fun configureLanguage(instance: TextToSpeech) {
        val candidates = listOf(
            Locale("es", "MX"),
            Locale.forLanguageTag("es-MX"),
            Locale("es", "ES"),
            Locale("es"),
            Locale.getDefault()
        )
        for (loc in candidates) {
            val res = instance.setLanguage(loc)
            if (res != TextToSpeech.LANG_MISSING_DATA && res != TextToSpeech.LANG_NOT_SUPPORTED) {
                android.util.Log.i("MedReminderTTS", "Idioma TTS establecido: $loc")
                return
            }
        }
    }

    private fun setupProgressListener(instance: TextToSpeech) {
        instance.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
            override fun onStart(utteranceId: String?) {
                if (utteranceId != currentUtteranceId) return
                _isSpeaking.value = true
                android.util.Log.i("MedReminderTTS", "Audio iniciado: $utteranceId")
            }

            override fun onDone(utteranceId: String?) {
                // Ignorar el fin de una frase vieja que fue reemplazada por otra más reciente
                if (utteranceId != currentUtteranceId) return
                finishSpeaking()
                android.util.Log.i("MedReminderTTS", "Audio concluido: $utteranceId")
            }

            @Deprecated("Deprecated in Java")
            override fun onError(utteranceId: String?) {
                if (utteranceId != currentUtteranceId) return
                finishSpeaking()
                android.util.Log.w("MedReminderTTS", "Audio terminado con error: $utteranceId")
            }

            override fun onError(utteranceId: String?, errorCode: Int) {
                if (utteranceId != currentUtteranceId) return
                finishSpeaking()
                android.util.Log.w("MedReminderTTS", "Audio con error ($errorCode): $utteranceId")
            }

            override fun onStop(utteranceId: String?, interrupted: Boolean) {
                if (utteranceId != currentUtteranceId) return
                finishSpeaking()
            }
        })
    }

    private fun finishSpeaking() {
        _isSpeaking.value = false
        _currentKey.value = null
        _currentText.value = null
    }

    /**
     * Construye y lee una frase clara de recordatorio clínico para una toma.
     */
    fun speakMedicationReminder(
        context: Context,
        tomaId: String = "",
        nombreMedicamento: String,
        dosisDetalle: String,
        horaFormateada: String,
        esCritico: Boolean = false,
        contraindicaciones: String? = null,
        force: Boolean = true,
        onDispatched: (() -> Unit)? = null
    ) {
        val key = "toma_$tomaId"
        val builder = StringBuilder()
        if (esCritico) {
            builder.append("Atención: Dosis crítica. ")
        }
        builder.append("Hora de tomar ")
        builder.append(nombreMedicamento)
        if (dosisDetalle.isNotBlank()) {
            builder.append(", dosis: ").append(dosisDetalle.replace("•", ", "))
        }
        if (horaFormateada.isNotBlank()) {
            builder.append(", programada a las ").append(horaFormateada)
        }
        if (!contraindicaciones.isNullOrBlank()) {
            builder.append(". Precaución: ").append(contraindicaciones)
        }
        builder.append(".")
        speak(context, builder.toString(), key = key, force = force, onDispatched = onDispatched)
    }

    fun stop() {
        var callbackToInvoke: (() -> Unit)? = null
        synchronized(this) {
            pendingUtterance = null
            pendingKey = null
            callbackToInvoke = pendingCallback
            pendingCallback = null
            currentUtteranceId = null
            _isSpeaking.value = false
            _currentKey.value = null
            _currentText.value = null
            runCatching { tts?.stop() }
        }
        callbackToInvoke?.invoke()
    }

    fun shutdown() {
        var callbackToInvoke: (() -> Unit)? = null
        synchronized(this) {
            pendingUtterance = null
            pendingKey = null
            callbackToInvoke = pendingCallback
            pendingCallback = null
            isReady = false
            isInitializing = false
            _isSpeaking.value = false
            _currentKey.value = null
            _currentText.value = null
            runCatching {
                tts?.stop()
                tts?.shutdown()
            }
            tts = null
        }
        callbackToInvoke?.invoke()
    }
}
