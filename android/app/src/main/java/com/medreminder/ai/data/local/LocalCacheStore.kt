package com.medreminder.ai.data.local

import android.content.Context
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.medreminder.ai.data.remote.EstadisticasOutDto
import com.medreminder.ai.data.repository.DashboardBundle
import java.util.UUID

data class PendingReminderAction(
    val id: String = UUID.randomUUID().toString(),
    val idRecordatorio: Int,
    val accion: String, // "tomar" | "posponer" | "omitir" | "revertir"
    val createdAtEpochMs: Long = System.currentTimeMillis()
)

/**
 * Caché local persistente para modo sin conexión y cola de sincronización diferida.
 * Sobrevive a cierres de proceso sin requerir infraestructura externa adicional.
 */
class LocalCacheStore(context: Context) {

    private val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    private val gson = Gson()
    private val lock = Any()

    fun saveDashboard(fechaKey: String, bundle: DashboardBundle) {
        synchronized(lock) {
            val json = gson.toJson(bundle)
            prefs.edit()
                .putString("$KEY_DASH_PREFIX$fechaKey", json)
                .putString(KEY_DASH_LATEST, json)
                .apply()
        }
    }

    fun loadDashboard(fechaKey: String): DashboardBundle? {
        synchronized(lock) {
            val raw = prefs.getString("$KEY_DASH_PREFIX$fechaKey", null)
                ?: (if (fechaKey == "hoy") prefs.getString(KEY_DASH_LATEST, null) else null)
                ?: return null
            return runCatching { gson.fromJson(raw, DashboardBundle::class.java) }.getOrNull()
        }
    }

    fun loadLatestDashboard(): DashboardBundle? {
        synchronized(lock) {
            val raw = prefs.getString(KEY_DASH_LATEST, null) ?: return null
            return runCatching { gson.fromJson(raw, DashboardBundle::class.java) }.getOrNull()
        }
    }

    fun saveEstadisticas(stats: EstadisticasOutDto) {
        synchronized(lock) {
            prefs.edit().putString(KEY_STATS, gson.toJson(stats)).apply()
        }
    }

    fun loadEstadisticas(): EstadisticasOutDto? {
        synchronized(lock) {
            val raw = prefs.getString(KEY_STATS, null) ?: return null
            return runCatching { gson.fromJson(raw, EstadisticasOutDto::class.java) }.getOrNull()
        }
    }

    fun getPendingActions(): List<PendingReminderAction> {
        synchronized(lock) {
            val raw = prefs.getString(KEY_QUEUE, null) ?: return emptyList()
            val listType = object : TypeToken<List<PendingReminderAction>>() {}.type
            return runCatching {
                gson.fromJson<List<PendingReminderAction>>(raw, listType)
            }.getOrNull().orEmpty()
        }
    }

    fun enqueuePendingAction(idRecordatorio: Int, accion: String): PendingReminderAction {
        synchronized(lock) {
            val current = getPendingActions().toMutableList()
            if (accion == "revertir") {
                val hadUnsyncedTerminal = current.any {
                    it.idRecordatorio == idRecordatorio && (it.accion == "tomar" || it.accion == "omitir")
                }
                if (hadUnsyncedTerminal) {
                    current.removeAll {
                        it.idRecordatorio == idRecordatorio && (it.accion == "tomar" || it.accion == "omitir")
                    }
                    saveQueueLocked(current)
                    applyOptimisticToAllCachedDashboardsLocked(idRecordatorio, "revertir")
                    return PendingReminderAction(idRecordatorio = idRecordatorio, accion = "revertir")
                }
            }
            if (accion == "tomar" || accion == "omitir") {
                current.removeAll { it.idRecordatorio == idRecordatorio && it.accion != "revertir" }
            }
            val item = PendingReminderAction(idRecordatorio = idRecordatorio, accion = accion)
            current.add(item)
            saveQueueLocked(current)
            applyOptimisticToAllCachedDashboardsLocked(idRecordatorio, accion)
            return item
        }
    }

    fun removePendingAction(id: String) {
        synchronized(lock) {
            val filtered = getPendingActions().filterNot { it.id == id }
            saveQueueLocked(filtered)
        }
    }

    fun pendingActionsCount(): Int = getPendingActions().size

    fun clearAll() {
        synchronized(lock) {
            prefs.edit().clear().apply()
        }
    }

    private fun saveQueueLocked(items: List<PendingReminderAction>) {
        prefs.edit().putString(KEY_QUEUE, gson.toJson(items)).apply()
    }

    private fun applyOptimisticToAllCachedDashboardsLocked(idRecordatorio: Int, accion: String) {
        val keys = prefs.all.keys.filter { it == KEY_DASH_LATEST || it.startsWith(KEY_DASH_PREFIX) }
        val editor = prefs.edit()
        for (key in keys) {
            val raw = prefs.getString(key, null) ?: continue
            val bundle = runCatching { gson.fromJson(raw, DashboardBundle::class.java) }.getOrNull() ?: continue
            val targetRec = bundle.recordatoriosHoy.firstOrNull { it.idRecordatorio == idRecordatorio } ?: continue
            val newEstado = when (accion) {
                "tomar" -> "tomado"
                "posponer" -> "pospuesto"
                "omitir" -> "omitido"
                "revertir" -> "pendiente"
                else -> targetRec.estado
            }
            val updatedRecs = bundle.recordatoriosHoy.map {
                if (it.idRecordatorio == idRecordatorio) {
                    it.copy(
                        estado = newEstado,
                        vecesPospuesto = if (accion == "posponer") it.vecesPospuesto + 1 else it.vecesPospuesto
                    )
                } else it
            }
            val updatedMeds = if (accion == "tomar" && targetRec.estado != "tomado") {
                bundle.medicamentos.map { med ->
                    if (med.idMedicamento == targetRec.idMedicamento ||
                        (targetRec.idMedicamento == null && med.nombre.equals(targetRec.nombreMedicamento, ignoreCase = true))
                    ) {
                        med.copy(cantidadStock = (med.cantidadStock - 1).coerceAtLeast(0))
                    } else med
                }
            } else if (accion == "revertir" && targetRec.estado == "tomado") {
                bundle.medicamentos.map { med ->
                    if (med.idMedicamento == targetRec.idMedicamento ||
                        (targetRec.idMedicamento == null && med.nombre.equals(targetRec.nombreMedicamento, ignoreCase = true))
                    ) {
                        med.copy(cantidadStock = med.cantidadStock + 1)
                    } else med
                }
            } else {
                bundle.medicamentos
            }
            editor.putString(
                key,
                gson.toJson(bundle.copy(medicamentos = updatedMeds, recordatoriosHoy = updatedRecs))
            )
        }
        editor.apply()
    }

    companion object {
        private const val PREFS_NAME = "medreminder_offline_cache"
        private const val KEY_DASH_PREFIX = "dash_fecha_"
        private const val KEY_DASH_LATEST = "dash_latest"
        private const val KEY_STATS = "estadisticas_latest"
        private const val KEY_QUEUE = "pending_actions_queue"
    }
}
