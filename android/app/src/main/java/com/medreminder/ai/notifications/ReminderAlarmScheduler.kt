package com.medreminder.ai.notifications

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import org.json.JSONArray
import org.json.JSONObject
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.ZoneId

/**
 * Programador de alarmas exactas con AlarmManager (`setExactAndAllowWhileIdle`)
 * y respaldo seguro con `setWindow` / `setAndAllowWhileIdle` cuando el permiso
 * `SCHEDULE_EXACT_ALARM` aún no ha sido concedido (evitando `SecurityException`).
 * Persiste alarmas activas localmente para restaurarlas en `BootCompletedReceiver`.
 */
object ReminderAlarmScheduler {
    private const val PREFS_ALARMS = "medreminder_scheduled_alarms"
    private const val KEY_ALARM_LIST = "scheduled_items_json"

    fun scheduleAlarm(
        context: Context,
        idRecordatorio: Int,
        triggerAtMillis: Long,
        nombreMedicamento: String,
        dosisDetalle: String,
        horaFormateada: String = "",
        esCritico: Boolean = false,
        permitePosponer: Boolean = true
    ) {
        val appContext = context.applicationContext
        NotificationHelper.ensureChannelsCreated(appContext)

        val alarmManager = appContext.getSystemService(Context.ALARM_SERVICE) as? AlarmManager ?: return
        val safeTriggerMillis = maxOf(triggerAtMillis, System.currentTimeMillis() + 2_000L)

        val intent = Intent(appContext, ReminderAlarmReceiver::class.java).apply {
            action = ReminderAlarmReceiver.ACTION_DISPARAR_ALARMA
            putExtra(ReminderAlarmReceiver.EXTRA_ID_RECORDATORIO, idRecordatorio)
            putExtra(ReminderAlarmReceiver.EXTRA_NOMBRE_MED, nombreMedicamento)
            putExtra(ReminderAlarmReceiver.EXTRA_DOSIS, dosisDetalle)
            putExtra(ReminderAlarmReceiver.EXTRA_HORA_FORMATEADA, horaFormateada)
            putExtra(ReminderAlarmReceiver.EXTRA_ES_CRITICO, esCritico)
            putExtra(ReminderAlarmReceiver.EXTRA_PERMITE_POSPONER, permitePosponer)
        }

        val pendingIntent = PendingIntent.getBroadcast(
            appContext,
            idRecordatorio,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        try {
            if (NotificationHelper.canScheduleExactAlarms(appContext)) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    alarmManager.setExactAndAllowWhileIdle(
                        AlarmManager.RTC_WAKEUP,
                        safeTriggerMillis,
                        pendingIntent
                    )
                } else {
                    alarmManager.setExact(
                        AlarmManager.RTC_WAKEUP,
                        safeTriggerMillis,
                        pendingIntent
                    )
                }
            } else {
                // Fallback seguro sin permiso de alarma exacta: ventana de hasta 1 minuto
                alarmManager.setWindow(
                    AlarmManager.RTC_WAKEUP,
                    safeTriggerMillis,
                    60_000L,
                    pendingIntent
                )
            }
        } catch (_: SecurityException) {
            // Protección garantizada ante revocación de permisos en tiempo de ejecución
            runCatching {
                alarmManager.setWindow(
                    AlarmManager.RTC_WAKEUP,
                    safeTriggerMillis,
                    60_000L,
                    pendingIntent
                )
            }
        }

        saveScheduledAlarm(
            context = appContext,
            idRecordatorio = idRecordatorio,
            triggerAtMillis = safeTriggerMillis,
            nombreMedicamento = nombreMedicamento,
            dosisDetalle = dosisDetalle,
            horaFormateada = horaFormateada,
            esCritico = esCritico,
            permitePosponer = permitePosponer
        )
    }

    /**
     * Programa una alarma a partir de una hora formateada (ej. "08:00 AM", "14:30 PM", "21:00")
     * si aún está en el futuro del día de hoy.
     */
    fun scheduleFromHoraFormateada(
        context: Context,
        idRecordatorio: Int,
        horaFormateada: String,
        nombreMedicamento: String,
        dosisDetalle: String,
        esCritico: Boolean = false,
        permitePosponer: Boolean = true
    ) {
        val triggerMillis = parseHoraToTodayMillis(horaFormateada) ?: return
        if (triggerMillis <= System.currentTimeMillis()) return
        scheduleAlarm(
            context = context,
            idRecordatorio = idRecordatorio,
            triggerAtMillis = triggerMillis,
            nombreMedicamento = nombreMedicamento,
            dosisDetalle = dosisDetalle,
            horaFormateada = horaFormateada,
            esCritico = esCritico,
            permitePosponer = permitePosponer
        )
    }

    fun scheduleSnooze30Min(
        context: Context,
        idRecordatorio: Int,
        nombreMedicamento: String,
        dosisDetalle: String,
        horaFormateada: String = ""
    ) {
        val triggerMillis = System.currentTimeMillis() + 30L * 60L * 1000L
        scheduleAlarm(
            context = context,
            idRecordatorio = idRecordatorio,
            triggerAtMillis = triggerMillis,
            nombreMedicamento = nombreMedicamento,
            dosisDetalle = dosisDetalle,
            horaFormateada = horaFormateada,
            esCritico = false,
            permitePosponer = true
        )
    }

    fun cancelAlarm(context: Context, idRecordatorio: Int) {
        val appContext = context.applicationContext
        val alarmManager = appContext.getSystemService(Context.ALARM_SERVICE) as? AlarmManager
        val intent = Intent(appContext, ReminderAlarmReceiver::class.java).apply {
            action = ReminderAlarmReceiver.ACTION_DISPARAR_ALARMA
        }
        val pendingIntent = PendingIntent.getBroadcast(
            appContext,
            idRecordatorio,
            intent,
            PendingIntent.FLAG_NO_CREATE or PendingIntent.FLAG_IMMUTABLE
        )
        if (pendingIntent != null && alarmManager != null) {
            runCatching { alarmManager.cancel(pendingIntent) }
            runCatching { pendingIntent.cancel() }
        }
        NotificationHelper.cancelNotification(appContext, idRecordatorio)
        removeScheduledAlarm(appContext, idRecordatorio)
    }

    fun markAlarmFired(context: Context, idRecordatorio: Int) {
        removeScheduledAlarm(context.applicationContext, idRecordatorio)
    }

    fun restoreScheduledAlarms(context: Context) {
        val appContext = context.applicationContext
        val prefs = appContext.getSharedPreferences(PREFS_ALARMS, Context.MODE_PRIVATE)
        val rawJson = prefs.getString(KEY_ALARM_LIST, "[]") ?: "[]"
        val now = System.currentTimeMillis()

        runCatching {
            val array = JSONArray(rawJson)
            val updatedArray = JSONArray()
            for (i in 0 until array.length()) {
                val obj = array.optJSONObject(i) ?: continue
                val triggerAt = obj.optLong("triggerAtMillis", 0L)
                val idRec = obj.optInt("idRecordatorio", -1)
                if (idRec <= 0 || triggerAt <= now - 5 * 60 * 1000L) continue

                updatedArray.put(obj)
                scheduleAlarm(
                    context = appContext,
                    idRecordatorio = idRec,
                    triggerAtMillis = maxOf(triggerAt, now + 5_000L),
                    nombreMedicamento = obj.optString("nombreMedicamento", "Medicamento"),
                    dosisDetalle = obj.optString("dosisDetalle", ""),
                    horaFormateada = obj.optString("horaFormateada", ""),
                    esCritico = obj.optBoolean("esCritico", false),
                    permitePosponer = obj.optBoolean("permitePosponer", true)
                )
            }
            prefs.edit().putString(KEY_ALARM_LIST, updatedArray.toString()).apply()
        }
    }

    internal fun parseHoraToTodayMillis(horaFormateada: String): Long? {
        return runCatching {
            val normalized = horaFormateada
                .trim()
                .uppercase()
                .replace(".", "")
                .replace("\u00A0", " ")
                .replace(Regex("\\s+"), " ")
            val isPm = normalized.contains("PM") || normalized.contains("P M")
            val isAm = normalized.contains("AM") || normalized.contains("A M")
            val timePart = normalized
                .replace("P M", "")
                .replace("A M", "")
                .replace("PM", "")
                .replace("AM", "")
                .trim()
            val parts = timePart.split(":")
            if (parts.size < 2) return null
            var hour = parts[0].filter { it.isDigit() }.toInt()
            val minute = parts[1].filter { it.isDigit() }.take(2).toInt()
            if (isPm && hour in 1..11) hour += 12
            if (isAm && hour == 12) hour = 0

            val localDateTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(hour, minute))
            localDateTime.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
        }.getOrNull()
    }

    private fun saveScheduledAlarm(
        context: Context,
        idRecordatorio: Int,
        triggerAtMillis: Long,
        nombreMedicamento: String,
        dosisDetalle: String,
        horaFormateada: String,
        esCritico: Boolean,
        permitePosponer: Boolean
    ) {
        runCatching {
            val prefs = context.getSharedPreferences(PREFS_ALARMS, Context.MODE_PRIVATE)
            val array = JSONArray(prefs.getString(KEY_ALARM_LIST, "[]") ?: "[]")
            val newArray = JSONArray()
            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue
                if (item.optInt("idRecordatorio") != idRecordatorio) {
                    newArray.put(item)
                }
            }
            newArray.put(
                JSONObject().apply {
                    put("idRecordatorio", idRecordatorio)
                    put("triggerAtMillis", triggerAtMillis)
                    put("nombreMedicamento", nombreMedicamento)
                    put("dosisDetalle", dosisDetalle)
                    put("horaFormateada", horaFormateada)
                    put("esCritico", esCritico)
                    put("permitePosponer", permitePosponer)
                }
            )
            prefs.edit().putString(KEY_ALARM_LIST, newArray.toString()).apply()
        }
    }

    private fun removeScheduledAlarm(context: Context, idRecordatorio: Int) {
        runCatching {
            val prefs = context.getSharedPreferences(PREFS_ALARMS, Context.MODE_PRIVATE)
            val array = JSONArray(prefs.getString(KEY_ALARM_LIST, "[]") ?: "[]")
            val newArray = JSONArray()
            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue
                if (item.optInt("idRecordatorio") != idRecordatorio) {
                    newArray.put(item)
                }
            }
            prefs.edit().putString(KEY_ALARM_LIST, newArray.toString()).apply()
        }
    }
}
