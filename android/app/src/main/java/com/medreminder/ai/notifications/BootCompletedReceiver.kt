package com.medreminder.ai.notifications

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

/**
 * Restaura los canales de notificación y reprograma las alarmas pendientes
 * cuando el dispositivo Android se reinicia (`ACTION_BOOT_COMPLETED`).
 */
class BootCompletedReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent?) {
        val action = intent?.action ?: return
        if (action == Intent.ACTION_BOOT_COMPLETED ||
            action == Intent.ACTION_MY_PACKAGE_REPLACED ||
            action == "android.intent.action.QUICKBOOT_POWERON"
        ) {
            NotificationHelper.ensureChannelsCreated(context)
            ReminderAlarmScheduler.restoreScheduledAlarms(context)
        }
    }
}
