package com.medreminder.ai.data.local

import android.content.Context
import androidx.work.BackoffPolicy
import androidx.work.Constraints
import androidx.work.CoroutineWorker
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import com.medreminder.ai.MedReminderApp
import java.util.concurrent.TimeUnit

/**
 * Worker de WorkManager que drena la cola local de acciones de medicación
 * en cuanto el dispositivo recupera conectividad de red.
 */
class OfflineSyncWorker(
    appContext: Context,
    params: WorkerParameters
) : CoroutineWorker(appContext, params) {

    override suspend fun doWork(): Result {
        val app = applicationContext as? MedReminderApp ?: return Result.failure()
        val syncResult = app.container.medRepository.syncPendingActions()
        return if (syncResult.stillPending > 0 && syncResult.hitNetworkError) {
            Result.retry()
        } else {
            Result.success()
        }
    }

    companion object {
        private const val UNIQUE_WORK_NAME = "medreminder_offline_sync_work"

        fun enqueue(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()
            val request = OneTimeWorkRequestBuilder<OfflineSyncWorker>()
                .setConstraints(constraints)
                .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 15, TimeUnit.SECONDS)
                .build()
            WorkManager.getInstance(context.applicationContext).enqueueUniqueWork(
                UNIQUE_WORK_NAME,
                ExistingWorkPolicy.REPLACE,
                request
            )
        }
    }
}
