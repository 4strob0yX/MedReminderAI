package com.medreminder.ai.notifications

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.medreminder.ai.MedReminderApp
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withTimeoutOrNull

/**
 * Receptor de alarmas locales de medicación y acciones rápidas desde la notificación
 * ("Tomar" y "Posponer 30 min").
 */
class ReminderAlarmReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent?) {
        if (intent == null) return
        val idRecordatorio = intent.getIntExtra(EXTRA_ID_RECORDATORIO, -1)
        if (idRecordatorio <= 0) return

        val nombreMed = intent.getStringExtra(EXTRA_NOMBRE_MED) ?: "Medicamento programado"
        val dosis = intent.getStringExtra(EXTRA_DOSIS) ?: ""
        val horaFormateada = intent.getStringExtra(EXTRA_HORA_FORMATEADA) ?: ""
        val esCritico = intent.getBooleanExtra(EXTRA_ES_CRITICO, false)
        val permitePosponer = intent.getBooleanExtra(EXTRA_PERMITE_POSPONER, true)

        when (intent.action) {
            ACTION_TOMAR -> {
                ReminderAlarmScheduler.cancelAlarm(context, idRecordatorio)
                val pendingResult = goAsync()
                CoroutineScope(Dispatchers.IO).launch {
                    try {
                        val app = context.applicationContext as? MedReminderApp
                        app?.container?.medRepository?.tomarRecordatorio(idRecordatorio)
                    } catch (_: Exception) {
                        // Falla silenciosa si no hay red; se sincronizará al abrir la app
                    } finally {
                        pendingResult.finish()
                    }
                }
            }

            ACTION_POSPONER -> {
                NotificationHelper.cancelNotification(context, idRecordatorio)
                if (!esCritico && permitePosponer) {
                    ReminderAlarmScheduler.scheduleSnooze30Min(
                        context = context,
                        idRecordatorio = idRecordatorio,
                        nombreMedicamento = nombreMed,
                        dosisDetalle = dosis,
                        horaFormateada = horaFormateada
                    )
                    val pendingResult = goAsync()
                    CoroutineScope(Dispatchers.IO).launch {
                        try {
                            val app = context.applicationContext as? MedReminderApp
                            app?.container?.medRepository?.posponerRecordatorio(idRecordatorio)
                        } catch (_: Exception) {
                            // Si no hay conexión, la alarma local de 30 min ya quedó reprogramada
                        } finally {
                            pendingResult.finish()
                        }
                    }
                }
            }

            ACTION_DISPARAR_ALARMA, null -> {
                ReminderAlarmScheduler.markAlarmFired(context, idRecordatorio)
                val pendingResult = goAsync()
                val ttsDispatched = CompletableDeferred<Unit>()
                NotificationHelper.showReminderNotification(
                    context = context,
                    idRecordatorio = idRecordatorio,
                    nombreMedicamento = nombreMed,
                    dosisDetalle = dosis,
                    horaFormateada = horaFormateada,
                    esCritico = esCritico,
                    permitePosponer = permitePosponer,
                    onTtsDispatched = { ttsDispatched.complete(Unit) }
                )
                CoroutineScope(Dispatchers.IO).launch {
                    try {
                        withTimeoutOrNull(2_500L) {
                            ttsDispatched.await()
                        }
                    } finally {
                        pendingResult.finish()
                    }
                }
            }
        }
    }

    companion object {
        const val ACTION_DISPARAR_ALARMA = "com.medreminder.ai.ACTION_DISPARAR_ALARMA"
        const val ACTION_TOMAR = "com.medreminder.ai.ACTION_TOMAR_MEDICAMENTO"
        const val ACTION_POSPONER = "com.medreminder.ai.ACTION_POSPONER_MEDICAMENTO"

        const val EXTRA_ID_RECORDATORIO = "extra_id_recordatorio"
        const val EXTRA_NOMBRE_MED = "extra_nombre_medicamento"
        const val EXTRA_DOSIS = "extra_dosis_detalle"
        const val EXTRA_HORA_FORMATEADA = "extra_hora_formateada"
        const val EXTRA_ES_CRITICO = "extra_es_critico"
        const val EXTRA_PERMITE_POSPONER = "extra_permite_posponer"
    }
}
