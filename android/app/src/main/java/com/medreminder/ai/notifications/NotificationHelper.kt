package com.medreminder.ai.notifications

import android.Manifest
import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioAttributes
import android.media.RingtoneManager
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.medreminder.ai.MainActivity
import com.medreminder.ai.R
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

data class ActiveNativeAlarmEvent(
    val idRecordatorio: Int,
    val nombreMedicamento: String,
    val dosisDetalle: String,
    val horaFormateada: String,
    val esCritico: Boolean,
    val permitePosponer: Boolean,
    val timestampMillis: Long = System.currentTimeMillis()
)

/**
 * Gestor de canales de notificación (`canal_estandar`, `canal_critico`, `canal_alarma_nativa`, `canal_cuidador`),
 * verificación de permisos en Android 12+/13+ y construcción de alarmas nativas y recordatorios
 * en la barra de notificaciones con botones de acción ("Tomar", "Posponer 30 min").
 */
object NotificationHelper {
    const val CHANNEL_ESTANDAR = "canal_estandar"
    const val CHANNEL_CRITICO = "canal_critico"
    const val CHANNEL_ALARMA_NATIVA = "canal_alarma_nativa_v2"
    const val CHANNEL_CUIDADOR = "canal_cuidador_alertas"
    private const val SUMMARY_NOTIFICATION_ID = 9901

    private val _activeAlarmEvent = MutableStateFlow<ActiveNativeAlarmEvent?>(null)
    val activeAlarmEvent: StateFlow<ActiveNativeAlarmEvent?> = _activeAlarmEvent.asStateFlow()

    fun dismissActiveAlarmEvent() {
        _activeAlarmEvent.value = null
    }

    fun emitInAppAlarmEvent(event: ActiveNativeAlarmEvent) {
        _activeAlarmEvent.value = event
    }

    fun ensureChannelsCreated(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager ?: return

        val alarmSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
            ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
        val alarmAudioAttrs = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_ALARM)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()

        val canalEstandar = NotificationChannel(
            CHANNEL_ESTANDAR,
            "Recordatorios de Medicación",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Recordatorios preventivos de tus tomas programadas en la barra de notificaciones"
            enableVibration(true)
            vibrationPattern = longArrayOf(0L, 250L, 150L, 250L)
            lockscreenVisibility = NotificationCompat.VISIBILITY_PUBLIC
        }

        val canalCritico = NotificationChannel(
            CHANNEL_CRITICO,
            "Dosis Críticas Impostergables",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Alertas de máxima prioridad para medicamentos críticos de ventana estricta"
            enableVibration(true)
            vibrationPattern = longArrayOf(0L, 500L, 200L, 500L, 200L, 600L)
            lockscreenVisibility = NotificationCompat.VISIBILITY_PUBLIC
            setBypassDnd(true)
            setSound(alarmSoundUri, alarmAudioAttrs)
        }

        val canalAlarmaNativa = NotificationChannel(
            CHANNEL_ALARMA_NATIVA,
            "Alarma Nativa de Toma Médica",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Alarma sonora nativa automática cuando llega la hora exacta de tomar un medicamento"
            enableVibration(true)
            vibrationPattern = longArrayOf(0L, 600L, 250L, 600L, 250L, 800L)
            lockscreenVisibility = NotificationCompat.VISIBILITY_PUBLIC
            setBypassDnd(true)
            setSound(alarmSoundUri, alarmAudioAttrs)
        }

        val canalCuidador = NotificationChannel(
            CHANNEL_CUIDADOR,
            "Supervisión y Alertas al Cuidador",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Avisos automáticos al cuidador por omisión o posposición de medicamentos en adultos mayores"
            enableVibration(true)
            vibrationPattern = longArrayOf(0L, 400L, 200L, 400L)
            lockscreenVisibility = NotificationCompat.VISIBILITY_PUBLIC
        }

        manager.createNotificationChannel(canalEstandar)
        manager.createNotificationChannel(canalCritico)
        manager.createNotificationChannel(canalAlarmaNativa)
        manager.createNotificationChannel(canalCuidador)
    }

    fun createNotificationChannels(context: Context) = ensureChannelsCreated(context)

    fun hasNotificationPermission(context: Context): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            NotificationManagerCompat.from(context).areNotificationsEnabled()
        }
    }

    fun canScheduleExactAlarms(context: Context): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as? AlarmManager
            alarmManager?.canScheduleExactAlarms() ?: false
        } else {
            true
        }
    }

    private fun triggerDeviceVibrationAndTone(context: Context, isCritical: Boolean) {
        runCatching {
            val vibrator = context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator
            if (vibrator != null && vibrator.hasVibrator()) {
                val pattern = if (isCritical) {
                    longArrayOf(0L, 500L, 180L, 500L, 180L, 650L)
                } else {
                    longArrayOf(0L, 350L, 150L, 350L)
                }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    vibrator.vibrate(VibrationEffect.createWaveform(pattern, -1))
                } else {
                    @Suppress("DEPRECATION")
                    vibrator.vibrate(pattern, -1)
                }
            }
        }
    }

    fun showReminderNotification(
        context: Context,
        idRecordatorio: Int,
        nombreMedicamento: String,
        dosisDetalle: String,
        horaFormateada: String = "",
        esCritico: Boolean = false,
        permitePosponer: Boolean = true,
        onTtsDispatched: (() -> Unit)? = null
    ) {
        ensureChannelsCreated(context)
        triggerDeviceVibrationAndTone(context, esCritico)

        // Emitir evento en vivo para que si la app está abierta (o al abrirse) salte el modal de alarma nativa
        _activeAlarmEvent.value = ActiveNativeAlarmEvent(
            idRecordatorio = idRecordatorio,
            nombreMedicamento = nombreMedicamento,
            dosisDetalle = dosisDetalle,
            horaFormateada = horaFormateada,
            esCritico = esCritico,
            permitePosponer = permitePosponer
        )

        if (!hasNotificationPermission(context)) {
            TtsHelper.speakMedicationReminder(
                context = context,
                nombreMedicamento = nombreMedicamento,
                dosisDetalle = dosisDetalle,
                horaFormateada = horaFormateada,
                esCritico = esCritico,
                force = true,
                onDispatched = onTtsDispatched
            )
            return
        }

        val channelId = if (esCritico) CHANNEL_CRITICO else CHANNEL_ALARMA_NATIVA

        val openAppIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(ReminderAlarmReceiver.EXTRA_ID_RECORDATORIO, idRecordatorio)
            putExtra(ReminderAlarmReceiver.EXTRA_NOMBRE_MED, nombreMedicamento)
            putExtra(ReminderAlarmReceiver.EXTRA_DOSIS, dosisDetalle)
            putExtra(ReminderAlarmReceiver.EXTRA_HORA_FORMATEADA, horaFormateada)
            putExtra(ReminderAlarmReceiver.EXTRA_ES_CRITICO, esCritico)
            putExtra(ReminderAlarmReceiver.EXTRA_PERMITE_POSPONER, permitePosponer)
        }
        val contentPendingIntent = PendingIntent.getActivity(
            context,
            idRecordatorio,
            openAppIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // Acción 1: Tomar medicamento
        val tomarIntent = Intent(context, ReminderAlarmReceiver::class.java).apply {
            action = ReminderAlarmReceiver.ACTION_TOMAR
            putExtra(ReminderAlarmReceiver.EXTRA_ID_RECORDATORIO, idRecordatorio)
            putExtra(ReminderAlarmReceiver.EXTRA_NOMBRE_MED, nombreMedicamento)
        }
        val tomarPendingIntent = PendingIntent.getBroadcast(
            context,
            idRecordatorio * 10 + 1,
            tomarIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val title = if (esCritico) {
            "ALARMA CRÍTICA: $nombreMedicamento"
        } else {
            "ALARMA DE MEDICAMENTO: $nombreMedicamento"
        }

        val bodyText = buildString {
            if (dosisDetalle.isNotBlank()) append(dosisDetalle)
            if (horaFormateada.isNotBlank()) {
                if (isNotEmpty()) append(" • ")
                append("Hora: $horaFormateada")
            }
            if (esCritico) {
                append("\nDosis crítica obligatoria: si se omite se alertará automáticamente a tu cuidador.")
            } else {
                append("\nToca para confirmar tu toma o usa los botones rápidos.")
            }
        }.ifBlank { "Es hora de tomar tu medicamento en MedReminder AI" }

        val alarmSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
            ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setColor(if (esCritico) 0xFFB71C1C.toInt() else 0xFF0D9488.toInt())
            .setContentTitle(title)
            .setContentText(bodyText)
            .setStyle(NotificationCompat.BigTextStyle().bigText(bodyText))
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setSound(alarmSoundUri)
            .setAutoCancel(true)
            .setContentIntent(contentPendingIntent)
            .setFullScreenIntent(contentPendingIntent, true)
            .addAction(0, "✓ Tomar ahora", tomarPendingIntent)

        // Acción 2: Posponer 30 min (solo si no es crítico y permite posponer)
        if (!esCritico && permitePosponer) {
            val posponerIntent = Intent(context, ReminderAlarmReceiver::class.java).apply {
                action = ReminderAlarmReceiver.ACTION_POSPONER
                putExtra(ReminderAlarmReceiver.EXTRA_ID_RECORDATORIO, idRecordatorio)
                putExtra(ReminderAlarmReceiver.EXTRA_NOMBRE_MED, nombreMedicamento)
                putExtra(ReminderAlarmReceiver.EXTRA_DOSIS, dosisDetalle)
                putExtra(ReminderAlarmReceiver.EXTRA_HORA_FORMATEADA, horaFormateada)
                putExtra(ReminderAlarmReceiver.EXTRA_ES_CRITICO, false)
                putExtra(ReminderAlarmReceiver.EXTRA_PERMITE_POSPONER, true)
            }
            val posponerPendingIntent = PendingIntent.getBroadcast(
                context,
                idRecordatorio * 10 + 2,
                posponerIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            builder.addAction(0, "⏰ Posponer 30m", posponerPendingIntent)
        }

        runCatching {
            NotificationManagerCompat.from(context).notify(idRecordatorio, builder.build())
        }

        // Anunciar por voz la alarma médica
        TtsHelper.speakMedicationReminder(
            context = context,
            nombreMedicamento = nombreMedicamento,
            dosisDetalle = dosisDetalle,
            horaFormateada = horaFormateada,
            esCritico = esCritico,
            force = true,
            onDispatched = onTtsDispatched
        )
    }

    /**
     * Publica un recordatorio preventivo en la barra de notificaciones con el resumen de las
     * próximas tomas del día para que el paciente siempre tenga visible su plan en Android.
     */
    fun showUpcomingSummaryNotification(
        context: Context,
        pendientesCount: Int,
        proximaMedNombre: String,
        proximaMedHora: String,
        proximaMedDosis: String,
        esCritico: Boolean
    ) {
        ensureChannelsCreated(context)
        if (!hasNotificationPermission(context) || pendientesCount <= 0) return

        val openAppIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val contentPendingIntent = PendingIntent.getActivity(
            context,
            SUMMARY_NOTIFICATION_ID,
            openAppIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val title = "Recordatorio Activo • $pendientesCount toma(s) pendiente(s) hoy"
        val body = "Próxima toma: $proximaMedNombre ($proximaMedDosis) programada a las $proximaMedHora" +
            if (esCritico) " • DOSIS CRÍTICA" else ""

        val notification = NotificationCompat.Builder(context, CHANNEL_ESTANDAR)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setColor(0xFF286675.toInt())
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setOngoing(false)
            .setAutoCancel(true)
            .setContentIntent(contentPendingIntent)
            .build()

        runCatching {
            NotificationManagerCompat.from(context).notify(SUMMARY_NOTIFICATION_ID, notification)
        }
    }

    /**
     * Notificación nativa cuando se alerta al cuidador (preventiva o crítica automática).
     */
    fun showCaregiverAlertNotification(
        context: Context,
        titulo: String,
        mensaje: String,
        esCritico: Boolean
    ) {
        ensureChannelsCreated(context)
        triggerDeviceVibrationAndTone(context, esCritico)
        if (!hasNotificationPermission(context)) return

        val openAppIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val contentPendingIntent = PendingIntent.getActivity(
            context,
            9902,
            openAppIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, CHANNEL_CUIDADOR)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setColor(if (esCritico) 0xFFB71C1C.toInt() else 0xFFE65100.toInt())
            .setContentTitle(titulo)
            .setContentText(mensaje)
            .setStyle(NotificationCompat.BigTextStyle().bigText(mensaje))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setAutoCancel(true)
            .setContentIntent(contentPendingIntent)
            .build()

        runCatching {
            NotificationManagerCompat.from(context).notify(
                if (esCritico) 9903 else 9902,
                notification
            )
        }
    }

    fun cancelNotification(context: Context, idRecordatorio: Int) {
        runCatching {
            NotificationManagerCompat.from(context).cancel(idRecordatorio)
        }
    }
}
