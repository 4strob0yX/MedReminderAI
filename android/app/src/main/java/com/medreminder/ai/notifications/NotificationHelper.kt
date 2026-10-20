package com.medreminder.ai.notifications

import android.Manifest
import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.medreminder.ai.MainActivity
import com.medreminder.ai.R

/**
 * Gestor de canales de notificación (`canal_estandar` y `canal_critico`),
 * verificación de permisos en Android 12+/13+ y construcción de notificaciones clínicas
 * con botones de acción ("Tomar", "Posponer 30 min").
 */
object NotificationHelper {
    const val CHANNEL_ESTANDAR = "canal_estandar"
    const val CHANNEL_CRITICO = "canal_critico"

    fun ensureChannelsCreated(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as? NotificationManager ?: return

        val canalEstandar = NotificationChannel(
            CHANNEL_ESTANDAR,
            "Recordatorios de Medicación",
            NotificationManager.IMPORTANCE_HIGH
        ).apply {
            description = "Alertas puntuales para tomas programadas del plan diario"
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
        }

        manager.createNotificationChannel(canalEstandar)
        manager.createNotificationChannel(canalCritico)
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
        if (!hasNotificationPermission(context)) {
            onTtsDispatched?.invoke()
            return
        }

        val channelId = if (esCritico) CHANNEL_CRITICO else CHANNEL_ESTANDAR

        val openAppIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra(ReminderAlarmReceiver.EXTRA_ID_RECORDATORIO, idRecordatorio)
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
            "DOSIS CRÍTICA: $nombreMedicamento"
        } else {
            "Hora de tu medicamento: $nombreMedicamento"
        }

        val bodyText = buildString {
            if (dosisDetalle.isNotBlank()) append(dosisDetalle)
            if (horaFormateada.isNotBlank()) {
                if (isNotEmpty()) append(" • ")
                append("Programada: $horaFormateada")
            }
            if (esCritico) {
                append("\nMedicamento crítico: No se recomienda posponer.")
            }
        }.ifBlank { "Confirma tu toma en MedReminder AI" }

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setColor(if (esCritico) 0xFFB71C1C.toInt() else 0xFF286675.toInt())
            .setContentTitle(title)
            .setContentText(bodyText)
            .setStyle(NotificationCompat.BigTextStyle().bigText(bodyText))
            .setPriority(if (esCritico) NotificationCompat.PRIORITY_MAX else NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setAutoCancel(true)
            .setContentIntent(contentPendingIntent)
            .addAction(0, "Tomar", tomarPendingIntent)

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
            builder.addAction(0, "Posponer 30 min", posponerPendingIntent)
        }

        runCatching {
            NotificationManagerCompat.from(context).notify(idRecordatorio, builder.build())
        }

        // Si el usuario tiene activada la lectura por voz automática en accesibilidad, anuncia la toma
        TtsHelper.speakMedicationReminder(
            context = context,
            nombreMedicamento = nombreMedicamento,
            dosisDetalle = dosisDetalle,
            horaFormateada = horaFormateada,
            esCritico = esCritico,
            force = false,
            onDispatched = onTtsDispatched
        )
    }

    fun cancelNotification(context: Context, idRecordatorio: Int) {
        runCatching {
            NotificationManagerCompat.from(context).cancel(idRecordatorio)
        }
    }
}
