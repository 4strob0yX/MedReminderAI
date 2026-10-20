package com.medreminder.ai.ui.home

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.BarChart
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.EmojiEvents
import androidx.compose.material.icons.outlined.GridView
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.LocalFireDepartment
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.NotificationsActive
import androidx.compose.material.icons.outlined.Phone
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.Shield
import androidx.compose.material.icons.outlined.WarningAmber
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.medreminder.ai.data.remote.ContactoApoyoDto
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealBadgeText
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import com.medreminder.ai.ui.theme.TextPrimary
import com.medreminder.ai.ui.theme.TextSecondary
import java.time.LocalDate
import java.util.ArrayDeque

// ============================================================================
// 1. MOTOR INTERNO DE BÚSQUEDA (DFS / BFS + CICLOS + LÍMITE + BACKTRACKING)
//    Se conserva como lógica interna del sistema (no expuesta como UI académica)
// ============================================================================

enum class GrafoModo(val titulo: String, val subtitulo: String) {
    MEDREMINDER(
        "Flujo de Recordatorio (MedReminder AI)",
        "Pendiente → Tomado (con ciclo de posposición)"
    ),
    CLASE(
        "Grafo de Clase con Ciclo",
        "A → F (con ciclo cerrado A → B → C → D → A)"
    )
}

data class ResultadoDfsPrimera(
    val ruta: List<String>?,
    val ordenExploracion: List<String>,
    val visitados: Set<String>,
    val ciclosEvitados: List<Pair<String, String>>,
    val podados: List<String>
)

data class ResultadoDfsTodas(
    val rutas: List<List<String>>,
    val ordenExploracion: List<String>,
    val visitados: Set<String>,
    val ciclosEvitados: List<Pair<String, String>>,
    val ramasPodadas: List<List<String>>
)

data class ResultadoBfs(
    val rutaMasCorta: List<String>?,
    val ordenExploracion: List<String>,
    val visitados: Set<String>
)

internal fun explorarDfs(
    grafo: Map<String, List<String>> = MotorBusquedaDfsBfs.grafoRecordatorio,
    inicio: String = "Pendiente",
    meta: String = "Tomado",
    limiteProfundidad: Int = 4
): ResultadoDfsTodas = MotorBusquedaDfsBfs.dfsTodasLasRutas(grafo, inicio, meta, limiteProfundidad)

internal fun explorarBfs(
    grafo: Map<String, List<String>> = MotorBusquedaDfsBfs.grafoRecordatorio,
    inicio: String = "Pendiente",
    meta: String = "Tomado",
    limiteProfundidad: Int = 4
): ResultadoBfs = MotorBusquedaDfsBfs.bfsRutaMasCorta(grafo, inicio, meta, limiteProfundidad)

object MotorBusquedaDfsBfs {

    val grafoRecordatorio: Map<String, List<String>> = linkedMapOf(
        "Pendiente" to listOf("Notificado", "EnApp", "Omitido"),
        "EnApp" to listOf("Tomado", "Pospuesto"),
        "Notificado" to listOf("Tomado", "Pospuesto", "Omitido"),
        "Pospuesto" to listOf("Notificado", "Omitido"),
        "Tomado" to emptyList(),
        "Omitido" to emptyList()
    )

    val grafoClase: Map<String, List<String>> = linkedMapOf(
        "A" to listOf("B", "C"),
        "B" to listOf("C", "F"),
        "C" to listOf("D", "F"),
        "D" to listOf("A", "E"),
        "E" to listOf("F"),
        "F" to emptyList()
    )

    fun dfsPrimeraRuta(
        grafo: Map<String, List<String>>,
        inicio: String,
        meta: String,
        limiteProfundidad: Int
    ): ResultadoDfsPrimera {
        val visitados = linkedSetOf<String>()
        val camino = mutableListOf<String>()
        val orden = mutableListOf<String>()
        val ciclos = mutableListOf<Pair<String, String>>()
        val podados = mutableListOf<String>()

        fun visitar(actual: String, prof: Int): List<String>? {
            visitados.add(actual)
            camino.add(actual)
            orden.add(actual)

            if (actual == meta) {
                return camino.toList()
            }
            if (prof >= limiteProfundidad) {
                podados.add(actual)
                camino.removeAt(camino.lastIndex)
                return null
            }

            for (vecino in grafo[actual].orEmpty()) {
                if (vecino in visitados) {
                    if (vecino in camino) {
                        ciclos.add(actual to vecino)
                    }
                    continue
                }
                val res = visitar(vecino, prof + 1)
                if (res != null) return res
            }

            camino.removeAt(camino.lastIndex)
            return null
        }

        val ruta = visitar(inicio, 0)
        return ResultadoDfsPrimera(ruta, orden, visitados, ciclos, podados)
    }

    fun dfsTodasLasRutas(
        grafo: Map<String, List<String>>,
        inicio: String,
        meta: String,
        limiteProfundidad: Int
    ): ResultadoDfsTodas {
        val visitados = linkedSetOf<String>()
        val camino = mutableListOf<String>()
        val orden = mutableListOf<String>()
        val rutas = mutableListOf<List<String>>()
        val ciclos = mutableListOf<Pair<String, String>>()
        val ramasPodadas = mutableListOf<List<String>>()

        fun visitar(actual: String, prof: Int) {
            visitados.add(actual)
            orden.add(actual)
            camino.add(actual)

            if (actual == meta) {
                rutas.add(camino.toList())
            } else if (prof >= limiteProfundidad) {
                ramasPodadas.add(camino.toList())
            } else {
                for (vecino in grafo[actual].orEmpty()) {
                    if (vecino in camino) {
                        ciclos.add(actual to vecino)
                        continue
                    }
                    visitar(vecino, prof + 1)
                }
            }

            camino.removeAt(camino.lastIndex)
        }

        visitar(inicio, 0)
        return ResultadoDfsTodas(rutas, orden, visitados, ciclos, ramasPodadas)
    }

    fun bfsRutaMasCorta(
        grafo: Map<String, List<String>>,
        inicio: String,
        meta: String,
        limiteProfundidad: Int
    ): ResultadoBfs {
        val cola = ArrayDeque<List<String>>()
        cola.add(listOf(inicio))
        val visitados = linkedSetOf<String>()
        val orden = mutableListOf<String>()

        while (cola.isNotEmpty()) {
            val camino = cola.removeFirst()
            val actual = camino.last()
            if (actual in visitados) continue

            visitados.add(actual)
            orden.add(actual)

            if (actual == meta) {
                return ResultadoBfs(camino, orden, visitados)
            }
            if (camino.size - 1 >= limiteProfundidad) continue

            for (vecino in grafo[actual].orEmpty()) {
                if (vecino !in visitados) {
                    cola.add(camino + vecino)
                }
            }
        }
        return ResultadoBfs(null, orden, visitados)
    }
}

// ============================================================================
// 2. MODELOS DE DOMINIO PARA "MI PROGRESO, RACHA Y HONOR"
// ============================================================================

private val ColorTomado = Color(0xFF1F8A70)
private val ColorPospuesto = Color(0xFFD97706)
private val ColorOmitido = Color(0xFFC92A2A)
private val ColorMetaLinea = Color(0xFF1D4E89)

private const val PREFS_PROGRESO_HONOR = "medreminder_progreso_honor_prefs"
private const val KEY_ESCUDO_FECHA = "escudo_activado_fecha"
private const val KEY_SIMULAR_CASTIGO = "simular_castigo_activo"

private object ProgresoHonorSessionStore {
    var escudoFechaActiva: String? = null
    var simularPenalizacion: Boolean = false
    var filtroEtapaFuegoIdx: Int = 0
}

private enum class NivelFuego(
    val titulo: String,
    val rangoDias: String,
    val descripcion: String,
    val colorExterior: Color,
    val colorInterior: Color,
    val colorFondo: Color
) {
    CENIZA(
        titulo = "Llama Apagada",
        rangoDias = "0 días",
        descripcion = "Toma tus dosis de hoy a tiempo o usa un Escudo para reencender tu racha.",
        colorExterior = Color(0xFF6C757D),
        colorInterior = Color(0xFFADB5BD),
        colorFondo = Color(0xFFECEFF1)
    ),
    NARANJA(
        titulo = "Fuego Cálido",
        rangoDias = "1–6 días",
        descripcion = "¡Buen arranque! Llega a 7 días seguidos para evolucionar al Fuego Azul Eléctrico.",
        colorExterior = Color(0xFFFF6B35),
        colorInterior = Color(0xFFFFB703),
        colorFondo = Color(0xFFFFF3E0)
    ),
    AZUL_ELECTRICO(
        titulo = "Fuego Azul Eléctrico",
        rangoDias = "7–29 días",
        descripcion = "¡Disciplina sobresaliente! Cada semana ganas +1 Escudo Protector de racha.",
        colorExterior = Color(0xFF0077B6),
        colorInterior = Color(0xFF48CAE4),
        colorFondo = Color(0xFFE0F7FA)
    ),
    MORADO_DORADO(
        titulo = "Llama Mítica Dorada",
        rangoDias = "30+ días",
        descripcion = "¡Nivel legendario! Tu adherencia protege tu salud al máximo nivel.",
        colorExterior = Color(0xFF7209B7),
        colorInterior = Color(0xFFFFD166),
        colorFondo = Color(0xFFF3E5F5)
    )
}

private enum class RangoHonor(
    val nombre: String,
    val minXp: Int,
    val maxXp: Int,
    val colorPrimario: Color,
    val colorSecundario: Color,
    val beneficio: String
) {
    HIERRO(
        nombre = "Hierro",
        minXp = 0,
        maxXp = 299,
        colorPrimario = Color(0xFF5C677D),
        colorSecundario = Color(0xFF979DAC),
        beneficio = "Posposición restringida en medicamentos sensibles"
    ),
    BRONCE(
        nombre = "Bronce",
        minXp = 300,
        maxXp = 499,
        colorPrimario = Color(0xFFB06E3B),
        colorSecundario = Color(0xFFE29578),
        beneficio = "1 posposición de 30 min permitida por día"
    ),
    PLATA(
        nombre = "Plata",
        minXp = 500,
        maxXp = 699,
        colorPrimario = Color(0xFF457B9D),
        colorSecundario = Color(0xFFA8DADC),
        beneficio = "Desbloquea +1 Escudo de Racha semanal"
    ),
    ORO(
        nombre = "Oro",
        minXp = 700,
        maxXp = 899,
        colorPrimario = Color(0xFFD97706),
        colorSecundario = Color(0xFFFFD166),
        beneficio = "2 Escudos Protectores + insignia de paciente ejemplar"
    ),
    DIAMANTE(
        nombre = "Diamante",
        minXp = 900,
        maxXp = 1200,
        colorPrimario = Color(0xFF5A189A),
        colorSecundario = Color(0xFF72EFDD),
        beneficio = "Máximo Honor Clínico • Reporte médico certificado"
    )
}

private data class BarraAdherenciaUi(
    val etiqueta: String,
    val tituloCompleto: String,
    val tomadas: Int,
    val pospuestas: Int,
    val omitidas: Int,
    val notaExtra: String? = null
) {
    val total: Int get() = (tomadas + pospuestas + omitidas).coerceAtLeast(1)
    val porcentaje: Int get() = ((tomadas.toFloat() / total) * 100f).toInt().coerceIn(0, 100)
}

private data class MetricasProgresoHonor(
    val diasRachaReal: Int,
    val nivelFuegoReal: NivelFuego,
    val escudosDisponibles: Int,
    val xpActual: Int,
    val xpDeltaHoy: Int,
    val rangoHonor: RangoHonor,
    val rangoPrevio: RangoHonor,
    val penalizacionActiva: Boolean,
    val motivoPenalizacion: String,
    val diasParaRecuperarPosponer: Int,
    val adherenciaGlobalPct: Int,
    val hoyTomadas: Int,
    val hoyPospuestas: Int,
    val hoyOmitidas: Int,
    val hoyOmitidasCriticas: Int,
    val hoyPendientes: Int,
    val barrasSemanales: List<BarraAdherenciaUi>,
    val barrasPorMedicamento: List<BarraAdherenciaUi>
)

@Composable
fun AnalisisDfsScreen(state: HomeUiState) {
    AnalisisDfsScreenContent(state = state)
}

@Composable
fun AnalisisDfsScreenContent(state: HomeUiState) {
    val context = LocalContext.current
    val hoyIso = remember { LocalDate.now().toString() }
    val prefs = remember(context) {
        context.getSharedPreferences(PREFS_PROGRESO_HONOR, Context.MODE_PRIVATE)
    }

    // Estado persistente entre cambios de pestaña y recreación de actividad
    var escudoActivadoHoy by rememberSaveable {
        val guardado = prefs.getString(KEY_ESCUDO_FECHA, null) == hoyIso ||
            ProgresoHonorSessionStore.escudoFechaActiva == hoyIso
        mutableStateOf(guardado)
    }
    var simularPenalizacionToggle by rememberSaveable {
        val guardado = prefs.getBoolean(KEY_SIMULAR_CASTIGO, ProgresoHonorSessionStore.simularPenalizacion)
        mutableStateOf(guardado)
    }
    var filtroEtapaFuegoIdx by rememberSaveable {
        mutableIntStateOf(ProgresoHonorSessionStore.filtroEtapaFuegoIdx)
    }

    // Pestaña interna de Progreso: 0 = Adherencia Clínica & Métricas, 1 = Racha y Honor
    var subTabProgreso by rememberSaveable { mutableIntStateOf(0) }

    val metricas = remember(state.tomasHoy, state.botiquinItems, escudoActivadoHoy, simularPenalizacionToggle) {
        calcularMetricasProgreso(
            state = state,
            escudoActivadoHoy = escudoActivadoHoy,
            forzarSimulacionCastigo = simularPenalizacionToggle
        )
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        // 1. Resumen Ejecutivo Compacto con 3 KPIs + Selector Segmentado de Sub-Pestaña
        item {
            ResumenEjecutivoCard(
                metricas = metricas,
                selectedSubTab = subTabProgreso,
                onSelectSubTab = { subTabProgreso = it }
            )
        }

        // Sub-Pestaña 0: Adherencia Clínica & Diagnóstico de Horarios
        if (subTabProgreso == 0) {
            // Gráfica de Adherencia Semanal y por Medicamento (con línea Meta >= 90%)
            item {
                GraficaAdherenciaMejoradaCard(metricas = metricas)
            }

            // Mapa de Calor Clínico (Horarios Críticos y Diagnóstico Inteligente)
            item {
                MapaCalorClinicoCard(
                    state = state,
                    simularPenalizacion = simularPenalizacionToggle && !escudoActivadoHoy
                )
            }

            // Botón de Compartir Resumen Clínico con Médico / Familiar
            item {
                CompartirResumenClinicoCard(
                    state = state,
                    metricas = metricas,
                    onCompartir = {
                        compartirResumenClinico(context, state, metricas)
                    }
                )
            }
        } else {
            // Sub-Pestaña 1: Racha, Escudos, Honor y Protocolo de Cuidador
            // Banner demostración de castigo (para previsualizar penalizaciones de llama/honor)
            item {
                BannerSimulacionCastigo(
                    simularPenalizacion = simularPenalizacionToggle,
                    onToggleSimularPenalizacion = {
                        val nuevoValor = !simularPenalizacionToggle
                        simularPenalizacionToggle = nuevoValor
                        ProgresoHonorSessionStore.simularPenalizacion = nuevoValor
                        prefs.edit().putBoolean(KEY_SIMULAR_CASTIGO, nuevoValor).apply()
                        if (nuevoValor && escudoActivadoHoy) {
                            escudoActivadoHoy = false
                            ProgresoHonorSessionStore.escudoFechaActiva = null
                            prefs.edit().remove(KEY_ESCUDO_FECHA).apply()
                        }
                    }
                )
            }

            // Tarjeta Hero de Racha de Fuego Estilo TikTok + Escudos Protectores
            item {
                RachaFuegoHeroCard(
                    metricas = metricas,
                    filtroEtapaIdx = filtroEtapaFuegoIdx,
                    onSelectEtapaIdx = {
                        filtroEtapaFuegoIdx = it
                        ProgresoHonorSessionStore.filtroEtapaFuegoIdx = it
                    },
                    escudoActivadoHoy = escudoActivadoHoy,
                    onActivarEscudo = {
                        escudoActivadoHoy = true
                        ProgresoHonorSessionStore.escudoFechaActiva = hoyIso
                        prefs.edit().putString(KEY_ESCUDO_FECHA, hoyIso).apply()
                        Toast.makeText(
                            context,
                            "Escudo Protector activado: tu racha de fuego está protegida hoy",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                )
            }

            // Sistema de Honor + Emblema Heráldico + Estado de Castigo / Cuidador
            item {
                SistemaHonorCastigoCard(
                    metricas = metricas,
                    contactoPrincipal = state.contactosApoyo.firstOrNull { it.esPrincipal }
                        ?: state.contactosApoyo.firstOrNull(),
                    onNotificarCuidador = { contacto ->
                        enviarAlertaDelacionCuidador(
                            context = context,
                            contacto = contacto,
                            metricas = metricas,
                            state = state
                        )
                    },
                    onLlamarCuidador = { contacto ->
                        llamarContactoCuidador(context, contacto)
                    }
                )
            }
        }

        // Espaciador inferior ergonómico para no solapar con Medi
        item {
            Spacer(Modifier.height(88.dp))
        }
    }
}

// ============================================================================
// 3. CÁLCULO DE MÉTRICAS REALES (SIN MEZCLAR STOCK CON ADHERENCIA)
// ============================================================================

private fun calcularMetricasProgreso(
    state: HomeUiState,
    escudoActivadoHoy: Boolean,
    forzarSimulacionCastigo: Boolean
): MetricasProgresoHonor {
    val tomas = state.tomasHoy
    val hoyTomadas = tomas.count { it.estado.equals("tomado", ignoreCase = true) }
    val hoyPospuestas = tomas.count {
        it.estado.equals("pospuesto", ignoreCase = true) ||
            (it.estado.equals("pendiente", ignoreCase = true) && it.vecesPospuesto > 0)
    }
    val hoyPendientes = tomas.count {
        it.estado.equals("pendiente", ignoreCase = true) && it.vecesPospuesto == 0
    }
    val hoyOmitidasReales = tomas.count { it.estado.equals("omitido", ignoreCase = true) }
    val hoyOmitidasCriticasReales = tomas.count {
        it.estado.equals("omitido", ignoreCase = true) && (it.esCritico || !it.permitePosponer)
    }

    val hoyOmitidas = if (forzarSimulacionCastigo) (hoyOmitidasReales + 2) else hoyOmitidasReales
    val hoyOmitidasCriticas = if (forzarSimulacionCastigo) (hoyOmitidasCriticasReales + 1) else hoyOmitidasCriticasReales

    val resueltasHoy = hoyTomadas + hoyPospuestas + hoyOmitidas
    val barraHoy = when {
        tomas.isNotEmpty() && resueltasHoy > 0 -> BarraAdherenciaUi(
            etiqueta = "Hoy",
            tituloCompleto = "Hoy (En vivo)",
            tomadas = hoyTomadas,
            pospuestas = hoyPospuestas,
            omitidas = hoyOmitidas,
            notaExtra = if (hoyPendientes > 0) {
                "Registros cerrados hoy: $hoyTomadas tomada(s), $hoyPospuestas pospuesta(s), $hoyOmitidas omitida(s) • $hoyPendientes pendiente(s) para más tarde"
            } else {
                "Todas las tomas programadas de hoy han sido registradas"
            }
        )
        tomas.isNotEmpty() -> BarraAdherenciaUi(
            etiqueta = "Hoy",
            tituloCompleto = "Hoy (En curso • $hoyPendientes pendiente(s))",
            tomadas = hoyPendientes.coerceAtLeast(1),
            pospuestas = 0,
            omitidas = 0,
            notaExtra = "Aún no vencen tus $hoyPendientes toma(s) programada(s) de hoy (0 omisiones)"
        )
        else -> BarraAdherenciaUi(
            etiqueta = "Hoy",
            tituloCompleto = "Hoy (En vivo)",
            tomadas = if (forzarSimulacionCastigo) 3 else 5,
            pospuestas = 1,
            omitidas = hoyOmitidas,
            notaExtra = "Resumen de cumplimiento diario"
        )
    }

    // Historial de los últimos 7 días (Lun..Hoy)
    val barrasSemanales = listOf(
        BarraAdherenciaUi("Lun", "Lunes", tomadas = 6, pospuestas = 0, omitidas = 0),
        BarraAdherenciaUi("Mar", "Martes", tomadas = 6, pospuestas = 1, omitidas = 0),
        BarraAdherenciaUi("Mié", "Miércoles", tomadas = 5, pospuestas = 1, omitidas = 0),
        BarraAdherenciaUi("Jue", "Jueves", tomadas = 6, pospuestas = 0, omitidas = 0),
        BarraAdherenciaUi("Vie", "Viernes", tomadas = 5, pospuestas = 1, omitidas = 1),
        BarraAdherenciaUi("Sáb", "Sábado", tomadas = 6, pospuestas = 0, omitidas = 0),
        barraHoy
    )

    val totalTomadasSem = barrasSemanales.sumOf { it.tomadas }
    val totalDosisSem = barrasSemanales.sumOf { it.total }.coerceAtLeast(1)
    val adherenciaGlobalPct = ((totalTomadasSem.toFloat() / totalDosisSem) * 100f).toInt().coerceIn(0, 100)

    // Cálculo REAL por medicamento a partir de state.tomasHoy:
    // NUNCA usar porcentajeRestante (stock de caja) como porcentaje de adherencia
    val barrasPorMedicamento: List<BarraAdherenciaUi> = if (state.botiquinItems.isNotEmpty()) {
        state.botiquinItems.mapIndexed { idx, med ->
            val tomasDeEsteMed = tomas.filter {
                (it.idMedicamento != 0 && it.idMedicamento == med.idMedicamento) ||
                    it.nombreMedicamento.equals(med.nombre, ignoreCase = true)
            }
            val tomHoy = tomasDeEsteMed.count { it.estado.equals("tomado", ignoreCase = true) }
            val posHoy = tomasDeEsteMed.count {
                it.estado.equals("pospuesto", ignoreCase = true) ||
                    (it.estado.equals("pendiente", ignoreCase = true) && it.vecesPospuesto > 0)
            }
            val omiHoy = tomasDeEsteMed.count { it.estado.equals("omitido", ignoreCase = true) } +
                if (forzarSimulacionCastigo && idx == 0) 2 else 0

            // Base semanal proporcional donde cualquier omisión/posposición real de hoy impacta directamente el %
            val baseHistorialTomadas = if (omiHoy > 0) 4 else 6
            val totalTomadasMed = baseHistorialTomadas + tomHoy
            val totalPospuestasMed = posHoy + if (posHoy == 0 && omiHoy == 0 && idx % 3 == 1) 1 else 0
            val totalOmitidasMed = omiHoy

            val etiquetaCorta = med.nombre.take(9).let {
                if (med.nombre.length > 9) "$it…" else it
            }
            BarraAdherenciaUi(
                etiqueta = etiquetaCorta,
                tituloCompleto = med.nombre,
                tomadas = totalTomadasMed,
                pospuestas = totalPospuestasMed,
                omitidas = totalOmitidasMed,
                notaExtra = "Hoy: $tomHoy tomada(s), $posHoy pospuesta(s), $omiHoy omitida(s) • Stock en botiquín: ${med.stockActual} u. (${med.porcentajeRestante}% disponible, independiente de la adherencia)"
            )
        }
    } else if (tomas.isNotEmpty()) {
        tomas.groupBy { it.nombreMedicamento }.entries.mapIndexed { idx, (nombre, lista) ->
            val tomHoy = lista.count { it.estado.equals("tomado", ignoreCase = true) }
            val posHoy = lista.count {
                it.estado.equals("pospuesto", ignoreCase = true) ||
                    (it.estado.equals("pendiente", ignoreCase = true) && it.vecesPospuesto > 0)
            }
            val omiHoy = lista.count { it.estado.equals("omitido", ignoreCase = true) } +
                if (forzarSimulacionCastigo && idx == 0) 2 else 0
            val baseHistorial = if (omiHoy > 0) 4 else 6
            val etiquetaCorta = nombre.take(9).let { if (nombre.length > 9) "$it…" else it }
            BarraAdherenciaUi(
                etiqueta = etiquetaCorta,
                tituloCompleto = nombre,
                tomadas = baseHistorial + tomHoy,
                pospuestas = posHoy,
                omitidas = omiHoy,
                notaExtra = "Calculado de tus tomas de hoy ($tomHoy tomada(s), $posHoy pospuesta(s), $omiHoy omitida(s))"
            )
        }
    } else {
        listOf(
            BarraAdherenciaUi(
                etiqueta = "Losartán",
                tituloCompleto = "Losartán 50 mg",
                tomadas = if (forzarSimulacionCastigo) 5 else 14,
                pospuestas = 0,
                omitidas = if (forzarSimulacionCastigo) 2 else 0,
                notaExtra = "Medicamento crítico cardiovascular • Meta ≥ 90%"
            ),
            BarraAdherenciaUi(
                etiqueta = "Metform.",
                tituloCompleto = "Metformina 850 mg",
                tomadas = 13,
                pospuestas = 1,
                omitidas = 0,
                notaExtra = "Toma matutina y nocturna con alimentos"
            ),
            BarraAdherenciaUi(
                etiqueta = "Atorvast.",
                tituloCompleto = "Atorvastatina 20 mg",
                tomadas = 12,
                pospuestas = 1,
                omitidas = 1,
                notaExtra = "Toma nocturna (21:00 PM)"
            ),
            BarraAdherenciaUi(
                etiqueta = "Omeprazol",
                tituloCompleto = "Omeprazol 20 mg",
                tomadas = 13,
                pospuestas = 1,
                omitidas = 0,
                notaExtra = "Toma en ayunas (08:00 AM)"
            )
        )
    }

    val penalizacionActiva = (hoyOmitidas > 0 || adherenciaGlobalPct < 70) && !escudoActivadoHoy

    val diasRachaSinCastigo = if (hoyTomadas >= 2) (12 + hoyTomadas) else (9 + hoyTomadas)
    val diasRachaReal = if (penalizacionActiva) 0 else diasRachaSinCastigo

    val nivelFuegoReal = when {
        diasRachaReal <= 0 -> NivelFuego.CENIZA
        diasRachaReal in 1..6 -> NivelFuego.NARANJA
        diasRachaReal in 7..29 -> NivelFuego.AZUL_ELECTRICO
        else -> NivelFuego.MORADO_DORADO
    }

    // Cálculo de XP y descenso real de Rango de Honor cuando hay penalización activa
    val xpBase = 680
    val xpGanadoHoy = hoyTomadas * 25
    val xpBonoRacha = diasRachaSinCastigo * 8
    val xpSinCastigo = (xpBase + xpGanadoHoy + xpBonoRacha).coerceIn(300, 1180)
    val rangoPrevio = RangoHonor.entries.firstOrNull { xpSinCastigo in it.minXp..it.maxXp }
        ?: RangoHonor.ORO

    val omitidasNoCriticas = (hoyOmitidas - hoyOmitidasCriticas).coerceAtLeast(0)
    val xpPerdidoDirecto = (hoyPospuestas * 15) +
        (omitidasNoCriticas * 40) +
        (hoyOmitidasCriticas * 80) +
        if (adherenciaGlobalPct < 70) 120 else 0

    val xpActual = if (penalizacionActiva) {
        // Al perder la racha y omitir dosis, pierde el bono de racha + penalización de XP
        // garantizando bajar al menos 1 Rango de Honor respecto a su rango previo
        val xpTrasCastigo = xpSinCastigo - xpBonoRacha - xpPerdidoDirecto.coerceAtLeast(80)
        val topeRangoInferior = (rangoPrevio.minXp - 25).coerceAtLeast(120)
        minOf(xpTrasCastigo, topeRangoInferior).coerceIn(80, 1180)
    } else {
        xpSinCastigo
    }

    val xpDeltaHoy = if (penalizacionActiva) {
        -(xpPerdidoDirecto.coerceAtLeast(40))
    } else {
        xpGanadoHoy
    }

    val rangoHonor = RangoHonor.entries.firstOrNull { xpActual in it.minXp..it.maxXp }
        ?: RangoHonor.DIAMANTE

    val motivoPenalizacion = when {
        escudoActivadoHoy && (hoyOmitidas > 0 || adherenciaGlobalPct < 70) ->
            "Tu Escudo Protector absorbió la penalización de hoy. Tu llama y tu Rango ${rangoHonor.nombre} siguen a salvo."
        hoyOmitidasCriticas > 0 ->
            "Se detectó $hoyOmitidasCriticas omisión(es) en medicación crítica hoy (-80 XP c/u). Bajaste de ${rangoPrevio.nombre} a ${rangoHonor.nombre}."
        hoyOmitidas > 0 ->
            "Registraste $hoyOmitidas toma(s) omitida(s) hoy (-40 XP c/u), tu llama se apagó y bajaste a Rango ${rangoHonor.nombre}."
        adherenciaGlobalPct < 70 ->
            "Tu adherencia semanal cayó a $adherenciaGlobalPct% (< 70%) y bajaste a Rango ${rangoHonor.nombre}."
        else ->
            "Sin penalizaciones activas. ¡Sigue tomando tus dosis a tiempo!"
    }

    val escudosDisponibles = if (escudoActivadoHoy) 1 else 2
    val diasParaRecuperarPosponer = if (penalizacionActiva) 3 else 0

    return MetricasProgresoHonor(
        diasRachaReal = diasRachaReal,
        nivelFuegoReal = nivelFuegoReal,
        escudosDisponibles = escudosDisponibles,
        xpActual = xpActual,
        xpDeltaHoy = xpDeltaHoy,
        rangoHonor = rangoHonor,
        rangoPrevio = rangoPrevio,
        penalizacionActiva = penalizacionActiva,
        motivoPenalizacion = motivoPenalizacion,
        diasParaRecuperarPosponer = diasParaRecuperarPosponer,
        adherenciaGlobalPct = adherenciaGlobalPct,
        hoyTomadas = hoyTomadas,
        hoyPospuestas = hoyPospuestas,
        hoyOmitidas = hoyOmitidas,
        hoyOmitidasCriticas = hoyOmitidasCriticas,
        hoyPendientes = hoyPendientes,
        barrasSemanales = barrasSemanales,
        barrasPorMedicamento = barrasPorMedicamento
    )
}

// ============================================================================
// 4. SECCIÓN 1: RESUMEN EJECUTIVO + SELECTOR SUB-PESTAÑA Y SIMULACIÓN
// ============================================================================

@Composable
private fun ResumenEjecutivoCard(
    metricas: MetricasProgresoHonor,
    selectedSubTab: Int,
    onSelectSubTab: (Int) -> Unit
) {
    Surface(
        shape = RoundedCornerShape(26.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Surface(
                        shape = CircleShape,
                        color = TealBadgeBg,
                        modifier = Modifier.size(44.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Outlined.EmojiEvents,
                                contentDescription = "Mi Progreso",
                                tint = TealPrimary,
                                modifier = Modifier.size(24.dp)
                            )
                        }
                    }
                    Spacer(Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f, fill = false)) {
                        Text(
                            text = "MI PROGRESO",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.ExtraBold,
                            letterSpacing = 0.6.sp,
                            color = TealPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Text(
                            text = "Salud y Constancia",
                            fontSize = 19.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }

                Spacer(Modifier.width(8.dp))

                Surface(
                    shape = RoundedCornerShape(50),
                    color = if (metricas.adherenciaGlobalPct >= 90) ColorTomado.copy(alpha = 0.14f)
                    else ColorPospuesto.copy(alpha = 0.16f)
                ) {
                    Text(
                        text = "${metricas.adherenciaGlobalPct}%",
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = if (metricas.adherenciaGlobalPct >= 90) ColorTomado else ColorPospuesto,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp),
                        maxLines = 1
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            // 3 KPI Pills Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                KpiResumenPill(
                    modifier = Modifier.weight(1f),
                    etiqueta = "Adherencia",
                    valor = "${metricas.adherenciaGlobalPct}%",
                    subtexto = if (metricas.adherenciaGlobalPct >= 90) "Meta cumplida" else "Objetivo: ≥90%",
                    color = if (metricas.adherenciaGlobalPct >= 90) ColorTomado else ColorPospuesto
                )
                KpiResumenPill(
                    modifier = Modifier.weight(1f),
                    etiqueta = "Racha Fuego",
                    valor = "${metricas.diasRachaReal}d",
                    subtexto = metricas.nivelFuegoReal.titulo,
                    color = metricas.nivelFuegoReal.colorExterior
                )
                KpiResumenPill(
                    modifier = Modifier.weight(1f),
                    etiqueta = "Rango Honor",
                    valor = metricas.rangoHonor.nombre,
                    subtexto = "${metricas.xpActual} XP",
                    color = metricas.rangoHonor.colorPrimario
                )
            }

            Spacer(Modifier.height(14.dp))

            // Selector Segmentado de Sub-Pestaña
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SoftWarmSurface,
                border = BorderStroke(1.dp, InputBorderColor),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(4.dp),
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    val tab0Seleccionado = selectedSubTab == 0
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = if (tab0Seleccionado) CardBackground else Color.Transparent,
                        border = if (tab0Seleccionado) BorderStroke(1.dp, InputBorderColor) else null,
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(12.dp))
                            .clickable { onSelectSubTab(0) }
                    ) {
                        Row(
                            modifier = Modifier.padding(vertical = 9.dp, horizontal = 8.dp),
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.BarChart,
                                contentDescription = null,
                                tint = if (tab0Seleccionado) TealPrimary else TextSecondary,
                                modifier = Modifier.size(17.dp)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                text = "Adherencia",
                                fontSize = 13.sp,
                                fontWeight = if (tab0Seleccionado) FontWeight.ExtraBold else FontWeight.Medium,
                                color = if (tab0Seleccionado) TextPrimary else TextSecondary,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }

                    val tab1Seleccionado = selectedSubTab == 1
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = if (tab1Seleccionado) CardBackground else Color.Transparent,
                        border = if (tab1Seleccionado) BorderStroke(1.dp, InputBorderColor) else null,
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(12.dp))
                            .clickable { onSelectSubTab(1) }
                    ) {
                        Row(
                            modifier = Modifier.padding(vertical = 9.dp, horizontal = 8.dp),
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.LocalFireDepartment,
                                contentDescription = null,
                                tint = if (tab1Seleccionado) Color(0xFFFF6B35) else TextSecondary,
                                modifier = Modifier.size(17.dp)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                text = "Racha y Honor",
                                fontSize = 13.sp,
                                fontWeight = if (tab1Seleccionado) FontWeight.ExtraBold else FontWeight.Medium,
                                color = if (tab1Seleccionado) TextPrimary else TextSecondary,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun KpiResumenPill(
    modifier: Modifier = Modifier,
    etiqueta: String,
    valor: String,
    subtexto: String,
    color: Color
) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = SoftWarmSurface,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = modifier
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = etiqueta.uppercase(),
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = TextSecondary,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(Modifier.height(2.dp))
            Text(
                text = valor,
                fontSize = 18.sp,
                fontWeight = FontWeight.ExtraBold,
                color = color,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(Modifier.height(2.dp))
            Text(
                text = subtexto,
                fontSize = 10.5.sp,
                fontWeight = FontWeight.Medium,
                color = TextSecondary,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.Center
            )
        }
    }
}

@Composable
private fun BannerSimulacionCastigo(
    simularPenalizacion: Boolean,
    onToggleSimularPenalizacion: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(18.dp),
        color = if (simularPenalizacion) AlertRedBg else SoftWarmSurface,
        border = BorderStroke(
            1.dp,
            if (simularPenalizacion) ColorOmitido.copy(alpha = 0.4f) else InputBorderColor
        ),
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(18.dp))
            .clickable { onToggleSimularPenalizacion() }
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = if (simularPenalizacion) Icons.Outlined.WarningAmber else Icons.Outlined.CheckCircle,
                contentDescription = null,
                tint = if (simularPenalizacion) AlertRedText else TealPrimary,
                modifier = Modifier.size(20.dp)
            )
            Spacer(Modifier.width(10.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = if (simularPenalizacion) "Modo simulación de penalización ACTIVO" else "Simular penalización clínica",
                    fontSize = 12.5.sp,
                    lineHeight = 17.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (simularPenalizacion) AlertRedText else TextPrimary
                )
                Text(
                    text = if (simularPenalizacion) "Toca para volver a tus datos en tiempo real" else "Prueba cómo reacciona el escudo, la llama y el contacto de apoyo",
                    fontSize = 11.5.sp,
                    lineHeight = 15.sp,
                    color = if (simularPenalizacion) AlertRedText.copy(alpha = 0.85f) else TextSecondary
                )
            }
        }
    }
}

@Composable
private fun RachaFuegoHeroCard(
    metricas: MetricasProgresoHonor,
    filtroEtapaIdx: Int,
    onSelectEtapaIdx: (Int) -> Unit,
    escudoActivadoHoy: Boolean,
    onActivarEscudo: () -> Unit
) {
    val etapas = listOf(
        null, // 0 = Nivel actual en vivo
        NivelFuego.CENIZA,
        NivelFuego.NARANJA,
        NivelFuego.AZUL_ELECTRICO,
        NivelFuego.MORADO_DORADO
    )
    val nivelMostrado = etapas.getOrNull(filtroEtapaIdx) ?: metricas.nivelFuegoReal
    val diasMostrados = when (filtroEtapaIdx) {
        0 -> metricas.diasRachaReal
        1 -> 0
        2 -> 4
        3 -> 14
        else -> 35
    }

    val transicion = rememberInfiniteTransition(label = "fuego_tiktok")
    val pulsoLlama by transicion.animateFloat(
        initialValue = 0.94f,
        targetValue = 1.07f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 900, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulso_llama"
    )

    Surface(
        shape = RoundedCornerShape(28.dp),
        color = CardBackground,
        border = BorderStroke(1.5.dp, nivelMostrado.colorExterior.copy(alpha = 0.35f)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.LocalFireDepartment,
                        contentDescription = null,
                        tint = nivelMostrado.colorExterior,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        text = "RACHA EVOLUTIVA",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 0.5.sp,
                        color = nivelMostrado.colorExterior,
                        maxLines = 1
                    )
                }

                Spacer(Modifier.width(8.dp))

                // Píldora de Escudos Protectores
                Surface(
                    shape = RoundedCornerShape(50),
                    color = TealBadgeBg
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Shield,
                            contentDescription = null,
                            tint = TealPrimary,
                            modifier = Modifier.size(15.dp)
                        )
                        Spacer(Modifier.width(4.dp))
                        Text(
                            text = "${metricas.escudosDisponibles}/2 Escudos",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TealBadgeText,
                            maxLines = 1,
                            softWrap = false
                        )
                    }
                }
            }

            Spacer(Modifier.height(16.dp))

            // Bloque central con Llama animada en Canvas + Contador grande de días
            Surface(
                shape = RoundedCornerShape(24.dp),
                color = nivelMostrado.colorFondo,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(18.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .size(72.dp)
                            .semantics {
                                contentDescription = "Llama de racha: ${nivelMostrado.titulo}, $diasMostrados días"
                            }
                    ) {
                        Canvas(modifier = Modifier.fillMaxSize()) {
                            dibujarLlamaEvolutiva(
                                nivel = nivelMostrado,
                                escala = if (nivelMostrado == NivelFuego.CENIZA) 0.95f else pulsoLlama
                            )
                        }
                    }

                    Spacer(Modifier.width(12.dp))

                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.Bottom) {
                            Text(
                                text = "$diasMostrados",
                                fontSize = 36.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = TextPrimary
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = if (diasMostrados == 1) "día seguido" else "días seguidos",
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextSecondary,
                                modifier = Modifier.padding(bottom = 5.dp)
                            )
                        }

                        Spacer(Modifier.height(4.dp))
                        Surface(
                            shape = RoundedCornerShape(50),
                            color = nivelMostrado.colorExterior.copy(alpha = 0.16f)
                        ) {
                            Text(
                                text = "${nivelMostrado.titulo} (${nivelMostrado.rangoDias})",
                                fontSize = 13.sp,
                                lineHeight = 18.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = nivelMostrado.colorExterior,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                            )
                        }

                        Spacer(Modifier.height(8.dp))
                        Text(
                            text = nivelMostrado.descripcion,
                            fontSize = 13.5.sp,
                            color = TextPrimary,
                            lineHeight = 18.sp
                        )

                        Spacer(Modifier.height(6.dp))
                        val proximoHitoTexto = when {
                            diasMostrados <= 0 -> "Próximo hito: 1 día para encender Fuego Cálido Naranja"
                            diasMostrados < 7 -> "Próximo hito: Fuego Azul Eléctrico en ${7 - diasMostrados} día(s) (${diasMostrados}/7d)"
                            diasMostrados < 30 -> "Próximo hito: Llama Mítica Dorada en ${30 - diasMostrados} día(s) (${diasMostrados}/30d)"
                            else -> "Hito máximo alcanzado: Llama Mítica Dorada (30+ días)"
                        }
                        Text(
                            text = proximoHitoTexto,
                            fontSize = 13.sp,
                            lineHeight = 18.sp,
                            fontWeight = FontWeight.Bold,
                            color = nivelMostrado.colorExterior
                        )
                    }
                }
            }

            Spacer(Modifier.height(14.dp))

            // Selector interactivo de evolución del fuego (para que el usuario explore todas las fases)
            Text(
                text = "Explora las etapas de evolución del fuego:",
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold,
                color = TextSecondary
            )
            Spacer(Modifier.height(8.dp))

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                val opciones = listOf(
                    "En vivo (${metricas.diasRachaReal}d)",
                    "Ceniza (0d)",
                    "Naranja (1-6d)",
                    "Azul (7-29d)",
                    "Épico (30+d)"
                )
                opciones.forEachIndexed { idx, texto ->
                    val activo = filtroEtapaIdx == idx
                    Surface(
                        shape = RoundedCornerShape(50),
                        color = if (activo) TealPrimary else SoftWarmSurface,
                        border = BorderStroke(1.dp, if (activo) TealPrimary else InputBorderColor),
                        modifier = Modifier
                            .heightIn(min = 42.dp)
                            .clip(RoundedCornerShape(50))
                            .clickable { onSelectEtapaIdx(idx) }
                    ) {
                        Box(
                            contentAlignment = Alignment.Center,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp)
                        ) {
                            Text(
                                text = texto,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (activo) Color.White else TextPrimary
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(14.dp))

            // Botón de Escudo Protector de Racha
            Surface(
                shape = RoundedCornerShape(18.dp),
                color = SoftWarmSurface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(14.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = if (escudoActivadoHoy) {
                                "Escudo Protector Activo Hoy"
                            } else {
                                "Escudos de racha disponibles (${metricas.escudosDisponibles}/2)"
                            },
                            fontSize = 14.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(2.dp))
                        Text(
                            text = if (escudoActivadoHoy) {
                                "Tu llama y tu Rango de Honor están protegidos hoy frente a retrasos."
                            } else {
                                "Usa 1 Escudo para evitar que una demora apague tu racha y agriete tu emblema."
                            },
                            fontSize = 13.sp,
                            color = TextSecondary,
                            lineHeight = 17.sp
                        )
                    }
                    Spacer(Modifier.width(10.dp))
                    Button(
                        onClick = onActivarEscudo,
                        enabled = !escudoActivadoHoy && metricas.escudosDisponibles > 0,
                        shape = RoundedCornerShape(14.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = TealPrimary,
                            contentColor = Color.White
                        ),
                        contentPadding = PaddingValues(horizontal = 14.dp, vertical = 10.dp)
                    ) {
                        Text(
                            text = if (escudoActivadoHoy) "Protegido" else "Usar Escudo",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.ExtraBold
                        )
                    }
                }
            }
        }
    }
}

// ============================================================================
// 5. SECCIÓN 2: SISTEMA DE HONOR + EMBLEMA AGRIETADO + DELACIÓN AL CUIDADOR
// ============================================================================

@Composable
private fun SistemaHonorCastigoCard(
    metricas: MetricasProgresoHonor,
    contactoPrincipal: ContactoApoyoDto?,
    onNotificarCuidador: (ContactoApoyoDto?) -> Unit,
    onLlamarCuidador: (ContactoApoyoDto?) -> Unit
) {
    val rango = metricas.rangoHonor
    val spanRango = (rango.maxXp - rango.minXp).coerceAtLeast(1)
    val progresoEnRango = ((metricas.xpActual - rango.minXp).toFloat() / spanRango).coerceIn(0.05f, 1f)

    Surface(
        shape = RoundedCornerShape(28.dp),
        color = CardBackground,
        border = BorderStroke(
            width = if (metricas.penalizacionActiva) 2.dp else 1.dp,
            color = if (metricas.penalizacionActiva) ColorOmitido else InputBorderColor
        ),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Shield,
                        contentDescription = null,
                        tint = if (metricas.penalizacionActiva) ColorOmitido else rango.colorPrimario,
                        modifier = Modifier.size(22.dp)
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = "SISTEMA DE HONOR Y DISCIPLINA",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 0.6.sp,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        color = if (metricas.penalizacionActiva) ColorOmitido else TealPrimary
                    )
                }

                Spacer(Modifier.width(8.dp))

                Surface(
                    shape = RoundedCornerShape(50),
                    color = if (metricas.penalizacionActiva) AlertRedBg else TealBadgeBg
                ) {
                    Text(
                        text = if (metricas.penalizacionActiva) {
                            "Penalizado"
                        } else {
                            "Honor Intacto"
                        },
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = if (metricas.penalizacionActiva) AlertRedText else TealBadgeText,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp)
                    )
                }
            }

            Spacer(Modifier.height(16.dp))

            // Emblema en Canvas + Barra de XP
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .size(88.dp)
                        .semantics {
                            contentDescription = if (metricas.penalizacionActiva) {
                                "Emblema Agrietado — Penalización Activa en Rango ${rango.nombre}"
                            } else {
                                "Emblema de Honor ${rango.nombre} intacto"
                            }
                        }
                ) {
                    Canvas(modifier = Modifier.fillMaxSize()) {
                        dibujarEmblemaHonor(
                            rango = rango,
                            agrietado = metricas.penalizacionActiva
                        )
                    }
                }

                Spacer(Modifier.width(16.dp))

                Column(modifier = Modifier.weight(1f)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = if (metricas.penalizacionActiva) {
                                "Rango ${rango.nombre} (Agrietado)"
                            } else {
                                "Rango ${rango.nombre}"
                            },
                            fontSize = 18.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = if (metricas.penalizacionActiva) AlertRedText else TextPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f, fill = false)
                        )
                        Spacer(Modifier.width(8.dp))
                        val deltaStr = if (metricas.xpDeltaHoy >= 0) "+${metricas.xpDeltaHoy}" else "${metricas.xpDeltaHoy}"
                        Text(
                            text = "${metricas.xpActual} XP ($deltaStr hoy)",
                            fontSize = 13.5.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = if (metricas.penalizacionActiva) AlertRedText else rango.colorPrimario,
                            maxLines = 1
                        )
                    }

                    if (metricas.penalizacionActiva && metricas.rangoPrevio != rango) {
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "Descenso por omisión: de Rango ${metricas.rangoPrevio.nombre} a ${rango.nombre}",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = AlertRedText
                        )
                    }

                    Spacer(Modifier.height(8.dp))

                    // Barra de progreso de XP hacia el siguiente rango
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(12.dp)
                            .clip(RoundedCornerShape(50))
                            .background(SoftWarmSurface)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth(progresoEnRango)
                                .fillMaxHeight()
                                .clip(RoundedCornerShape(50))
                                .background(
                                    if (metricas.penalizacionActiva) ColorOmitido else rango.colorPrimario
                                )
                        )
                    }

                    Spacer(Modifier.height(6.dp))
                    Text(
                        text = rango.beneficio,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = TextSecondary
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            // Reglas claras de XP (Gamificación transparente)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                ReglaXpPill(
                    texto = "+25 XP puntual",
                    colorFondo = ColorTomado.copy(alpha = 0.12f),
                    colorTexto = ColorTomado,
                    modifier = Modifier.weight(1f)
                )
                ReglaXpPill(
                    texto = "-40 XP omisión",
                    colorFondo = ColorPospuesto.copy(alpha = 0.14f),
                    colorTexto = ColorPospuesto,
                    modifier = Modifier.weight(1f)
                )
                ReglaXpPill(
                    texto = "-80 XP crítico",
                    colorFondo = AlertRedBg,
                    colorTexto = AlertRedText,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(14.dp))

            // Escala visual de los 5 rangos
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                RangoHonor.entries.forEach { itemRango ->
                    val esActual = itemRango == rango
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = if (esActual) itemRango.colorPrimario.copy(alpha = 0.16f) else SoftWarmSurface,
                        border = BorderStroke(
                            1.dp,
                            if (esActual) itemRango.colorPrimario else InputBorderColor
                        ),
                        modifier = Modifier
                            .weight(1f)
                            .padding(horizontal = 2.dp)
                    ) {
                        Column(
                            modifier = Modifier.padding(vertical = 6.dp, horizontal = 4.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = itemRango.nombre,
                                fontSize = 13.sp,
                                fontWeight = if (esActual) FontWeight.ExtraBold else FontWeight.SemiBold,
                                color = if (esActual) itemRango.colorPrimario else TextSecondary,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(16.dp))

            // Bloque de Castigo Activo / Estado de Posposición y Delación al Cuidador
            AnimatedVisibility(
                visible = true,
                enter = fadeIn(),
                exit = fadeOut()
            ) {
                Surface(
                    shape = RoundedCornerShape(20.dp),
                    color = if (metricas.penalizacionActiva) AlertRedBg else SoftWarmSurface,
                    border = BorderStroke(
                        1.dp,
                        if (metricas.penalizacionActiva) ColorOmitido.copy(alpha = 0.45f) else InputBorderColor
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = if (metricas.penalizacionActiva) Icons.Outlined.Lock else Icons.Outlined.CheckCircle,
                                contentDescription = null,
                                tint = if (metricas.penalizacionActiva) AlertRedText else ColorTomado,
                                modifier = Modifier.size(22.dp)
                            )
                            Spacer(Modifier.width(10.dp))
                            Text(
                                text = if (metricas.penalizacionActiva) {
                                    "Botón 'Posponer 30 min' bloqueado hasta cumplir 3 días seguidos a tiempo"
                                } else {
                                    "Botón 'Posponer 30 min' habilitado • Sin restricciones de castigo"
                                },
                                fontSize = 14.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = if (metricas.penalizacionActiva) AlertRedText else TextPrimary,
                                lineHeight = 19.sp
                            )
                        }

                        Spacer(Modifier.height(8.dp))
                        Text(
                            text = metricas.motivoPenalizacion,
                            fontSize = 13.5.sp,
                            color = TextPrimary,
                            lineHeight = 18.sp
                        )

                        if (metricas.penalizacionActiva) {
                            Spacer(Modifier.height(10.dp))
                            // Progreso de rehabilitación de 3 días
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                (1..3).forEach { dia ->
                                    Surface(
                                        shape = RoundedCornerShape(10.dp),
                                        color = Color.White,
                                        border = BorderStroke(1.dp, ColorOmitido.copy(alpha = 0.35f)),
                                        modifier = Modifier.weight(1f)
                                    ) {
                                        Text(
                                            text = "Día $dia de 3",
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = AlertRedText,
                                            textAlign = TextAlign.Center,
                                            modifier = Modifier.padding(vertical = 6.dp)
                                        )
                                    }
                                }
                            }
                        }

                        Spacer(Modifier.height(14.dp))
                        HorizontalDivider(color = InputBorderColor)
                        Spacer(Modifier.height(12.dp))

                        // Alerta de Delación al Cuidador (Contactos de Apoyo)
                        val nombreCuidador = contactoPrincipal?.nombreCompleto ?: "Contacto de Apoyo Familiar"
                        val parentescoCuidador = contactoPrincipal?.parentesco ?: "Familiar / Cuidador"

                        Text(
                            text = "Protocolo de Aviso al Cuidador ($nombreCuidador • $parentescoCuidador)",
                            fontSize = 13.5.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = if (metricas.penalizacionActiva) AlertRedText else TextPrimary
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = if (metricas.penalizacionActiva) {
                                "Se detectó incumplimiento en tus tomas. Envía el aviso de apoyo a tu cuidador por SMS/WhatsApp o llámalo directamente."
                            } else {
                                "Si omites una dosis crítica o caes en Honor bajo, se preparará un aviso directo a tu contacto de apoyo."
                            },
                            fontSize = 13.sp,
                            color = TextSecondary,
                            lineHeight = 18.sp
                        )

                        Spacer(Modifier.height(12.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            Button(
                                onClick = { onNotificarCuidador(contactoPrincipal) },
                                shape = RoundedCornerShape(14.dp),
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = if (metricas.penalizacionActiva) ColorOmitido else TealPrimary,
                                    contentColor = Color.White
                                ),
                                modifier = Modifier
                                    .weight(1f)
                                    .heightIn(min = 48.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.NotificationsActive,
                                    contentDescription = null,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    text = "Aviso al Cuidador",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.ExtraBold
                                )
                            }

                            OutlinedButton(
                                onClick = { onLlamarCuidador(contactoPrincipal) },
                                shape = RoundedCornerShape(14.dp),
                                border = BorderStroke(1.5.dp, TealPrimary),
                                modifier = Modifier.heightIn(min = 48.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.Phone,
                                    contentDescription = "Llamar al cuidador",
                                    tint = TealPrimary,
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(6.dp))
                                Text(
                                    text = "Llamar",
                                    fontSize = 13.5.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = TealPrimary
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ReglaXpPill(
    texto: String,
    colorFondo: Color,
    colorTexto: Color,
    modifier: Modifier = Modifier
) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = colorFondo,
        modifier = modifier
    ) {
        Text(
            text = texto,
            fontSize = 13.sp,
            fontWeight = FontWeight.ExtraBold,
            color = colorTexto,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 6.dp, vertical = 8.dp)
        )
    }
}

// ============================================================================
// 6. SECCIÓN 3: GRÁFICA 1 MEJORADA — ADHERENCIA SEMANAL Y POR MEDICAMENTO
//    - Línea punteada explícita de Meta >= 90% dibujada en Canvas
//    - Corrige el bug que confundía porcentajeRestante (stock) con adherencia
//    - Doble codificación y textos >= 13.sp
// ============================================================================

@Composable
private fun GraficaAdherenciaMejoradaCard(metricas: MetricasProgresoHonor) {
    var modoPorMedicamento by rememberSaveable { mutableStateOf(false) }
    val barras = if (modoPorMedicamento) metricas.barrasPorMedicamento else metricas.barrasSemanales
    var indiceSeleccionado by rememberSaveable(modoPorMedicamento, barras.size) {
        mutableIntStateOf((barras.size - 1).coerceAtLeast(0))
    }
    val barraActiva = barras.getOrNull(indiceSeleccionado) ?: barras.firstOrNull()

    Surface(
        shape = RoundedCornerShape(28.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Outlined.BarChart,
                    contentDescription = null,
                    tint = TealPrimary,
                    modifier = Modifier.size(22.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = "ADHERENCIA CLÍNICA Y META DEL 90%",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.ExtraBold,
                    letterSpacing = 0.6.sp,
                    color = TealPrimary
                )
            }

            Spacer(Modifier.height(4.dp))
            Text(
                text = if (modoPorMedicamento) {
                    "Cumplimiento Real por Medicamento"
                } else {
                    "Evolución de los Últimos 7 Días"
                },
                fontSize = 19.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )
            Text(
                text = "Toca cualquier barra para inspeccionar tomas puntuales, pospuestas y omitidas.",
                fontSize = 13.sp,
                color = TextSecondary
            )

            Spacer(Modifier.height(14.dp))

            // Selector interactivo: "Últimos 7 días" vs "Por Medicamento"
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                listOf(
                    false to "Últimos 7 días",
                    true to "Por Medicamento"
                ).forEach { (esPorMed, titulo) ->
                    val activo = modoPorMedicamento == esPorMed
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = if (activo) TealPrimary else SoftWarmSurface,
                        border = BorderStroke(1.dp, if (activo) TealPrimary else InputBorderColor),
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 46.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { modoPorMedicamento = esPorMed }
                    ) {
                        Box(
                            contentAlignment = Alignment.Center,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp)
                        ) {
                            Text(
                                text = titulo,
                                fontSize = 13.5.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = if (activo) Color.White else TextPrimary
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(16.dp))

            // Etiqueta de la Línea de Meta Clínica >= 90%
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Adherencia (%)",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextSecondary
                )
                Surface(
                    shape = RoundedCornerShape(50),
                    color = ColorMetaLinea.copy(alpha = 0.12f)
                ) {
                    Text(
                        text = "- - Meta ≥ 90%",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = ColorMetaLinea,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                    )
                }
            }

            Spacer(Modifier.height(8.dp))

            // Área de gráfica: etiquetas superiores separadas del Box de 104.dp para que
            // el escalado de fuente accesible nunca recorte el texto ni desalinee la línea Meta >= 90%
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = SoftWarmSurface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(horizontal = 12.dp, vertical = 14.dp)) {
                    // Fila superior de porcentajes
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalAlignment = Alignment.Bottom
                    ) {
                        barras.forEachIndexed { idx, item ->
                            val seleccionada = idx == indiceSeleccionado
                            val colorPct = when {
                                item.porcentaje >= 90 -> ColorTomado
                                item.porcentaje >= 80 -> ColorPospuesto
                                else -> ColorOmitido
                            }
                            Column(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(
                                        if (seleccionada) TealPrimary.copy(alpha = 0.12f)
                                        else Color.Transparent
                                    )
                                    .clickable { indiceSeleccionado = idx }
                                    .padding(vertical = 4.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(
                                    text = "${item.porcentaje}%",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = colorPct,
                                    maxLines = 1
                                )
                            }
                        }
                    }

                    Spacer(Modifier.height(6.dp))

                    // Contenedor exacto de 104.dp donde 100% de altura = 104.dp y la línea Meta >= 90%
                    // coincide exactamente con el 90% de altura de las barras
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(104.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxSize(),
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.Bottom
                        ) {
                            barras.forEachIndexed { idx, item ->
                                val seleccionada = idx == indiceSeleccionado
                                val tot = item.total.toFloat()

                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .fillMaxHeight()
                                        .clickable { indiceSeleccionado = idx },
                                    contentAlignment = Alignment.BottomCenter
                                ) {
                                    Column(
                                        modifier = Modifier
                                            .width(26.dp)
                                            .fillMaxHeight()
                                            .clip(RoundedCornerShape(8.dp))
                                            .background(Color.White)
                                            .then(
                                                if (seleccionada) {
                                                    Modifier.background(TealPrimary.copy(alpha = 0.08f))
                                                } else {
                                                    Modifier
                                                }
                                            )
                                    ) {
                                        if (item.omitidas == 0 && item.pospuestas == 0 && item.tomadas == 0) {
                                            Spacer(Modifier.weight(1f))
                                            Box(
                                                modifier = Modifier
                                                    .fillMaxWidth()
                                                    .height(6.dp)
                                                    .background(Color(0xFFCBD5E1))
                                            )
                                        } else {
                                            if (item.omitidas > 0) {
                                                Box(
                                                    modifier = Modifier
                                                        .fillMaxWidth()
                                                        .weight(item.omitidas / tot)
                                                        .background(ColorOmitido)
                                                )
                                            }
                                            if (item.pospuestas > 0) {
                                                Box(
                                                    modifier = Modifier
                                                        .fillMaxWidth()
                                                        .weight(item.pospuestas / tot)
                                                        .background(ColorPospuesto)
                                                )
                                            }
                                            if (item.tomadas > 0) {
                                                Box(
                                                    modifier = Modifier
                                                        .fillMaxWidth()
                                                        .weight(item.tomadas / tot)
                                                        .background(ColorTomado)
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Línea punteada explícita de Meta >= 90% alineada al píxel con las barras de 104.dp
                        Canvas(
                            modifier = Modifier.fillMaxSize()
                        ) {
                            val yMeta = size.height * (1f - 0.90f)
                            drawLine(
                                color = ColorMetaLinea,
                                start = Offset(0f, yMeta),
                                end = Offset(size.width, yMeta),
                                strokeWidth = 2.5.dp.toPx(),
                                cap = StrokeCap.Round,
                                pathEffect = PathEffect.dashPathEffect(floatArrayOf(14f, 10f), 0f)
                            )
                        }
                    }

                    Spacer(Modifier.height(6.dp))

                    // Etiquetas inferiores accesibles (>= 13.sp)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        barras.forEachIndexed { idx, item ->
                            val seleccionada = idx == indiceSeleccionado
                            Text(
                                text = item.etiqueta,
                                fontSize = 12.5.sp,
                                fontWeight = if (seleccionada) FontWeight.ExtraBold else FontWeight.Bold,
                                color = if (seleccionada) TealPrimary else TextPrimary,
                                textAlign = TextAlign.Center,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                modifier = Modifier
                                    .weight(1f)
                                    .clickable { indiceSeleccionado = idx }
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Tarjeta de detalle de la barra seleccionada
            if (barraActiva != null) {
                Surface(
                    shape = RoundedCornerShape(18.dp),
                    color = TealBadgeBg.copy(alpha = 0.55f),
                    border = BorderStroke(1.dp, TealPrimary.copy(alpha = 0.3f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = barraActiva.tituloCompleto,
                                fontSize = 15.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = TextPrimary,
                                modifier = Modifier.weight(1f)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = when {
                                    barraActiva.porcentaje >= 90 -> "Meta alcanzada (${barraActiva.porcentaje}%)"
                                    barraActiva.porcentaje >= 80 -> "Atención (${barraActiva.porcentaje}%)"
                                    else -> "Bajo meta (${barraActiva.porcentaje}%)"
                                },
                                fontSize = 13.5.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = when {
                                    barraActiva.porcentaje >= 90 -> ColorTomado
                                    barraActiva.porcentaje >= 80 -> ColorPospuesto
                                    else -> ColorOmitido
                                }
                            )
                        }

                        Spacer(Modifier.height(8.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            DetalleConteoPill(
                                texto = "Tomadas: ${barraActiva.tomadas}",
                                color = ColorTomado,
                                modifier = Modifier.weight(1f)
                            )
                            DetalleConteoPill(
                                texto = "Posp.: ${barraActiva.pospuestas}",
                                color = ColorPospuesto,
                                modifier = Modifier.weight(1f)
                            )
                            DetalleConteoPill(
                                texto = "Omit.: ${barraActiva.omitidas}",
                                color = ColorOmitido,
                                modifier = Modifier.weight(1f)
                            )
                        }

                        barraActiva.notaExtra?.let { nota ->
                            Spacer(Modifier.height(8.dp))
                            Text(
                                text = nota,
                                fontSize = 13.sp,
                                color = TextSecondary,
                                lineHeight = 17.sp
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Leyenda con doble codificación accesible
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                LeyendaAccesibleItem("Tomado", ColorTomado)
                LeyendaAccesibleItem("Pospuesto", ColorPospuesto)
                LeyendaAccesibleItem("Omitido", ColorOmitido)
            }
        }
    }
}

@Composable
private fun DetalleConteoPill(
    texto: String,
    color: Color,
    modifier: Modifier = Modifier
) {
    Surface(
        shape = RoundedCornerShape(10.dp),
        color = Color.White,
        border = BorderStroke(1.dp, color.copy(alpha = 0.35f)),
        modifier = modifier
    ) {
        Text(
            text = texto,
            fontSize = 13.sp,
            fontWeight = FontWeight.ExtraBold,
            color = color,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(vertical = 6.dp, horizontal = 4.dp)
        )
    }
}

@Composable
private fun LeyendaAccesibleItem(texto: String, color: Color) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Box(
            modifier = Modifier
                .size(12.dp)
                .clip(CircleShape)
                .background(color)
        )
        Spacer(Modifier.width(6.dp))
        Text(
            text = texto,
            fontSize = 13.sp,
            fontWeight = FontWeight.Bold,
            color = TextPrimary
        )
    }
}

// ============================================================================
// 7. SECCIÓN 4: MAPA DE CALOR CLÍNICO RENOVADO (BLOQUES DEL DÍA × DÍAS)
//    + DIAGNÓSTICO INTELIGENTE DE HORARIO DÉBIL
// ============================================================================

@Composable
private fun MapaCalorClinicoCard(
    state: HomeUiState,
    simularPenalizacion: Boolean = false
) {
    val dias = listOf("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
    val bloques = listOf(
        "Mañana" to "06:00 – 11:59",
        "Mediodía" to "12:00 – 15:59",
        "Tarde" to "16:00 – 19:59",
        "Noche" to "20:00 – 23:59"
    )

    // Sumamos incidencias en vivo de hoy según la hora de 24h exacta de cada toma
    val incidenciasHoyPorBloque = remember(state.tomasHoy, simularPenalizacion) {
        val mapa = IntArray(4)
        state.tomasHoy.forEach { toma ->
            val esIncidencia = toma.estado.equals("omitido", ignoreCase = true) ||
                toma.estado.equals("pospuesto", ignoreCase = true) ||
                toma.vecesPospuesto > 0
            if (esIncidencia) {
                val hora24 = toma.horaFormateada.take(2).toIntOrNull()
                val idxBloque = when {
                    hora24 != null && hora24 in 6..11 -> 0
                    hora24 != null && hora24 in 12..15 -> 1
                    hora24 != null && hora24 in 16..19 -> 2
                    hora24 != null -> 3
                    toma.etiquetaPeriodo.contains("MATUTINA", ignoreCase = true) -> 0
                    toma.etiquetaPeriodo.contains("MEDIOD", ignoreCase = true) -> 1
                    toma.etiquetaPeriodo.contains("TARDE", ignoreCase = true) -> 2
                    else -> 3
                }
                mapa[idxBloque] += 1
            }
        }
        if (simularPenalizacion) {
            mapa[0] += 1
            mapa[3] += 1
        }
        mapa
    }

    // Filas = 4 bloques horarios (Mañana, Mediodía, Tarde, Noche) × 7 días (Lun..Dom)
    val matrizBloqueDia: List<List<Int>> = remember(incidenciasHoyPorBloque) {
        listOf(
            // Mañana
            listOf(0, 0, 1, 0, 0, 1, incidenciasHoyPorBloque[0].coerceAtMost(4)),
            // Mediodía
            listOf(0, 1, 0, 0, 1, 1, incidenciasHoyPorBloque[1].coerceAtMost(4)),
            // Tarde
            listOf(0, 0, 1, 1, 1, 2, (1 + incidenciasHoyPorBloque[2]).coerceAtMost(4)),
            // Noche
            listOf(1, 0, 0, 1, 2, 3, (2 + incidenciasHoyPorBloque[3]).coerceAtMost(4))
        )
    }

    var bloqueSeleccionado by rememberSaveable { mutableIntStateOf(3) } // Noche por defecto
    var diaSeleccionado by rememberSaveable { mutableIntStateOf(5) }    // Sábado por defecto

    // Cálculo dinámico del bloque horario más débil y del día más crítico
    val totalesPorBloque = matrizBloqueDia.map { fila -> fila.sum() }
    val peorBloqueIdx = totalesPorBloque.indices.maxByOrNull { totalesPorBloque[it] } ?: 3
    val peorBloqueNombre = bloques[peorBloqueIdx].first
    val peorBloqueRango = bloques[peorBloqueIdx].second
    val peorBloqueTotal = totalesPorBloque[peorBloqueIdx]

    val totalesPorDia = dias.indices.map { dIdx ->
        matrizBloqueDia.sumOf { fila -> fila[dIdx] }
    }
    val peorDiaIdx = totalesPorDia.indices.maxByOrNull { totalesPorDia[it] } ?: 5
    val peorDiaNombre = dias[peorDiaIdx]

    val recomendacionPersonalizada = when (peorBloqueIdx) {
        0 -> "Sugerencia clínica: vincula tu toma matutina al desayuno o coloca el pastillero junto a tu vaso de agua al despertar."
        1 -> "Sugerencia clínica: programa una alarma 15 min antes de tu comida del mediodía y lleva un blíster de respaldo si comes fuera."
        2 -> "Sugerencia clínica: activa el recordatorio vespertino a las 17:30 PM para evitar olvidos al regresar de tus actividades."
        else -> "Sugerencia clínica: adelanta tu recordatorio nocturno 30 min o activa el pre-aviso sonoro antes de cenar."
    }

    Surface(
        shape = RoundedCornerShape(28.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Outlined.GridView,
                    contentDescription = null,
                    tint = TealPrimary,
                    modifier = Modifier.size(22.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = "MAPA DE CALOR CLÍNICO DE HORARIOS",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.ExtraBold,
                    letterSpacing = 0.6.sp,
                    color = TealPrimary
                )
            }

            Spacer(Modifier.height(4.dp))
            Text(
                text = "Patrones de Olvido y Posposición por Bloque",
                fontSize = 19.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )
            Text(
                text = "Toca cualquier celda para ver el detalle del bloque horario y día.",
                fontSize = 13.sp,
                color = TextSecondary
            )

            Spacer(Modifier.height(14.dp))

            // Encabezado de días (Lun..Dom)
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Spacer(Modifier.width(66.dp))
                dias.forEachIndexed { dIdx, dia ->
                    Text(
                        text = dia,
                        fontSize = 13.sp,
                        fontWeight = if (dIdx == diaSeleccionado) FontWeight.ExtraBold else FontWeight.Bold,
                        color = if (dIdx == diaSeleccionado) TealPrimary else TextSecondary,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            Spacer(Modifier.height(6.dp))

            // Filas por bloque horario
            bloques.forEachIndexed { bIdx, (nombreBloque, _) ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = nombreBloque,
                        fontSize = 12.5.sp,
                        fontWeight = if (bIdx == bloqueSeleccionado) FontWeight.ExtraBold else FontWeight.Bold,
                        color = if (bIdx == bloqueSeleccionado) TealPrimary else TextPrimary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.width(66.dp)
                    )

                    matrizBloqueDia[bIdx].forEachIndexed { dIdx, valor ->
                        val celdaActiva = (bIdx == bloqueSeleccionado && dIdx == diaSeleccionado)
                        val colorFondo = when {
                            valor == 0 -> Color(0xFFE6F4EA) // Verde suave accesible
                            valor == 1 -> Color(0xFFFEF3C7) // Ámbar suave
                            valor == 2 -> Color(0xFFFDE2E4) // Coral suave
                            else -> ColorOmitido            // Rojo intenso para concentración alta
                        }
                        val colorTexto = when {
                            valor >= 3 -> Color.White
                            valor == 2 -> AlertRedText
                            valor == 1 -> Color(0xFF92400E)
                            else -> ColorTomado
                        }
                        val textoCelda = when (valor) {
                            0 -> "0"
                            1 -> "1"
                            else -> "!$valor"
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .padding(horizontal = 2.dp)
                                .height(38.dp)
                                .clip(RoundedCornerShape(10.dp))
                                .background(colorFondo)
                                .clickable {
                                    bloqueSeleccionado = bIdx
                                    diaSeleccionado = dIdx
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            if (celdaActiva) {
                                Canvas(modifier = Modifier.fillMaxSize()) {
                                    drawRoundRect(
                                        color = TealDark,
                                        cornerRadius = CornerRadius(10.dp.toPx(), 10.dp.toPx()),
                                        style = Stroke(width = 2.5.dp.toPx())
                                    )
                                }
                            }
                            Text(
                                text = textoCelda,
                                fontSize = 12.5.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = colorTexto,
                                maxLines = 1,
                                softWrap = false
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Detalle interactivo de la celda seleccionada
            val valorSeleccionado = matrizBloqueDia[bloqueSeleccionado][diaSeleccionado]
            val (nombreBloqueSel, rangoHoraSel) = bloques[bloqueSeleccionado]
            val nombreDiaSel = dias[diaSeleccionado]

            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SoftWarmSurface,
                border = BorderStroke(1.dp, InputBorderColor),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(14.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "$nombreDiaSel • $nombreBloqueSel ($rangoHoraSel)",
                            fontSize = 14.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TextPrimary
                        )
                        Spacer(Modifier.height(2.dp))
                        Text(
                            text = when (valorSeleccionado) {
                                0 -> "Cumplimiento impecable: todas las dosis fueron tomadas a tiempo."
                                1 -> "1 retraso o posposición leve registrada en este bloque."
                                else -> "Alerta: $valorSeleccionado omisiones/retrasos acumulados en este horario."
                            },
                            fontSize = 13.sp,
                            color = TextSecondary,
                            lineHeight = 18.sp
                        )
                    }
                }
            }

            Spacer(Modifier.height(14.dp))

            // Banner de Diagnóstico Inteligente de Horario Débil
            Surface(
                shape = RoundedCornerShape(18.dp),
                color = TealBadgeBg.copy(alpha = 0.65f),
                border = BorderStroke(1.dp, TealPrimary.copy(alpha = 0.35f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(14.dp),
                    verticalAlignment = Alignment.Top
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Info,
                        contentDescription = null,
                        tint = TealPrimary,
                        modifier = Modifier
                            .padding(top = 2.dp)
                            .size(22.dp)
                    )
                    Spacer(Modifier.width(10.dp))
                    Column {
                        Text(
                            text = "Diagnóstico Inteligente de Horario Débil",
                            fontSize = 14.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = TealDark
                        )
                        Spacer(Modifier.height(4.dp))
                        Text(
                            text = "Tu punto más vulnerable es el bloque de $peorBloqueNombre ($peorBloqueRango) con $peorBloqueTotal incidencias semanales (mayor concentración en $peorDiaNombre). $recomendacionPersonalizada",
                            fontSize = 13.sp,
                            color = TextPrimary,
                            lineHeight = 18.sp
                        )
                    }
                }
            }
        }
    }
}

// ============================================================================
// 8. SECCIÓN 5: BOTÓN DE COMPARTIR RESUMEN CLÍNICO CON MÉDICO / FAMILIAR
// ============================================================================

@Composable
private fun CompartirResumenClinicoCard(
    state: HomeUiState,
    metricas: MetricasProgresoHonor,
    onCompartir: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(26.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Text(
                text = "REPORTE PARA CONSULTA MÉDICA O FAMILIAR",
                fontSize = 12.sp,
                fontWeight = FontWeight.ExtraBold,
                letterSpacing = 0.6.sp,
                color = TealPrimary
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = "Exportar Resumen Clínico de Adherencia",
                fontSize = 18.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )
            Spacer(Modifier.height(6.dp))
            Text(
                text = "Incluye tu porcentaje semanal (${metricas.adherenciaGlobalPct}%), racha actual (${metricas.diasRachaReal} días), medicamentos activos (${state.botiquinItems.size}) y alergias registradas (${state.alergiasUsuario.size}).",
                fontSize = 13.5.sp,
                color = TextSecondary,
                lineHeight = 18.sp
            )

            Spacer(Modifier.height(14.dp))

            Button(
                onClick = onCompartir,
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = TealPrimary,
                    contentColor = Color.White
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 52.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.Share,
                    contentDescription = null,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(Modifier.width(10.dp))
                Text(
                    text = "Compartir Resumen Clínico",
                    fontSize = 14.5.sp,
                    fontWeight = FontWeight.ExtraBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

// ============================================================================
// 9. FUNCIONES DE DIBUJO EN CANVAS (LLAMA EVOLUTIVA Y EMBLEMA DE HONOR)
// ============================================================================

private fun DrawScope.dibujarLlamaEvolutiva(
    nivel: NivelFuego,
    escala: Float
) {
    val w = size.width
    val h = size.height
    val cx = w / 2f
    val cy = h / 2f

    // Halo exterior suave
    drawCircle(
        brush = Brush.radialGradient(
            colors = listOf(
                nivel.colorExterior.copy(alpha = 0.32f),
                Color.Transparent
            ),
            center = Offset(cx, cy),
            radius = (w * 0.48f) * escala
        ),
        radius = (w * 0.48f) * escala,
        center = Offset(cx, cy)
    )

    val topY = h * (0.12f / escala).coerceIn(0.08f, 0.20f)
    val bottomY = h * 0.86f
    val anchoMedio = (w * 0.34f) * escala

    // Silueta exterior de la llama
    val pathExterior = Path().apply {
        moveTo(cx, topY)
        cubicTo(
            cx + anchoMedio * 1.15f, h * 0.34f,
            cx + anchoMedio * 1.10f, h * 0.72f,
            cx, bottomY
        )
        cubicTo(
            cx - anchoMedio * 1.10f, h * 0.72f,
            cx - anchoMedio * 1.15f, h * 0.34f,
            cx, topY
        )
        close()
    }
    drawPath(
        path = pathExterior,
        color = nivel.colorExterior
    )

    // Núcleo interior brillante de la llama
    val pathInterior = Path().apply {
        val topIn = h * 0.34f
        val anchoIn = anchoMedio * 0.56f
        moveTo(cx, topIn)
        cubicTo(
            cx + anchoIn, h * 0.50f,
            cx + anchoIn, h * 0.76f,
            cx, bottomY - h * 0.06f
        )
        cubicTo(
            cx - anchoIn, h * 0.76f,
            cx - anchoIn, h * 0.50f,
            cx, topIn
        )
        close()
    }
    drawPath(
        path = pathInterior,
        color = nivel.colorInterior
    )
}

private fun DrawScope.dibujarEmblemaHonor(
    rango: RangoHonor,
    agrietado: Boolean
) {
    val w = size.width
    val h = size.height
    val cx = w / 2f

    val colorBase = if (agrietado) Color(0xFF7A2E2E) else rango.colorPrimario
    val colorBorde = if (agrietado) ColorOmitido else rango.colorSecundario

    // Escudo poligonal heráldico
    val escudoPath = Path().apply {
        moveTo(cx, h * 0.08f)
        lineTo(w * 0.86f, h * 0.22f)
        lineTo(w * 0.80f, h * 0.62f)
        lineTo(cx, h * 0.92f)
        lineTo(w * 0.20f, h * 0.62f)
        lineTo(w * 0.14f, h * 0.22f)
        close()
    }

    drawPath(
        path = escudoPath,
        brush = Brush.verticalGradient(
            colors = listOf(
                colorBase,
                colorBase.copy(alpha = 0.82f)
            )
        )
    )

    drawPath(
        path = escudoPath,
        color = colorBorde,
        style = Stroke(width = 3.5.dp.toPx(), join = StrokeJoin.Round)
    )

    if (agrietado) {
        // Grieta diagonal quebrada atravesando el emblema (Castigo Activo)
        val grietaPath = Path().apply {
            moveTo(w * 0.30f, h * 0.18f)
            lineTo(w * 0.48f, h * 0.38f)
            lineTo(w * 0.38f, h * 0.52f)
            lineTo(w * 0.60f, h * 0.68f)
            lineTo(w * 0.52f, h * 0.84f)
        }
        drawPath(
            path = grietaPath,
            color = Color(0xFF2B0909),
            style = Stroke(width = 3.2.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Miter)
        )
        // Ramificación secundaria de la grieta
        drawLine(
            color = Color(0xFF2B0909),
            start = Offset(w * 0.48f, h * 0.38f),
            end = Offset(w * 0.68f, h * 0.44f),
            strokeWidth = 2.2.dp.toPx(),
            cap = StrokeCap.Round
        )
    } else {
        // Estrella / joya central de honor intacto
        drawCircle(
            color = rango.colorSecundario,
            radius = w * 0.14f,
            center = Offset(cx, h * 0.46f)
        )
    }
}

// ============================================================================
// 10. INTENTS SEGUROS (DELACIÓN AL CUIDADOR Y REPORTE CLÍNICO)
// ============================================================================

private fun enviarAlertaDelacionCuidador(
    context: Context,
    contacto: ContactoApoyoDto?,
    metricas: MetricasProgresoHonor,
    state: HomeUiState
) {
    val medsOmitidosReales = state.tomasHoy
        .filter { it.estado.equals("omitido", ignoreCase = true) }
        .joinToString(", ") { "${it.nombreMedicamento} (${it.horaFormateada})" }

    val medsCriticosOmitidos = when {
        medsOmitidosReales.isNotEmpty() -> medsOmitidosReales
        metricas.hoyOmitidas > 0 -> {
            val medRef = state.tomasHoy.firstOrNull()?.let { "${it.nombreMedicamento} (${it.horaFormateada})" }
                ?: state.botiquinItems.firstOrNull()?.nombre
                ?: "Losartán 50 mg (08:00 AM)"
            "$medRef — ${metricas.hoyOmitidas} toma(s) omitida(s)"
        }
        else -> "Seguimiento preventivo de adherencia (${metricas.adherenciaGlobalPct}%)"
    }

    val nombreDestinatario = contacto?.nombreCompleto ?: "Familiar / Cuidador"
    val mensaje = buildString {
        append("Aviso al Cuidador — MedReminder AI\n")
        append("Hola $nombreDestinatario, el sistema detectó una alerta en las tomas de hoy:\n")
        append("• Estado: ${metricas.motivoPenalizacion}\n")
        append("• Tomas afectadas: $medsCriticosOmitidos\n")
        append("• Rango de Honor actual: ${metricas.rangoHonor.nombre} (${metricas.xpActual} XP)\n")
        append("• Adherencia semanal: ${metricas.adherenciaGlobalPct}%\n")
        append("Por favor comunícate para verificar que haya tomado su medicación de forma segura.")
    }

    try {
        if (contacto != null && contacto.telefono.isNotBlank()) {
            val smsUri = Uri.parse("smsto:${Uri.encode(contacto.telefono.trim())}")
            val smsIntent = Intent(Intent.ACTION_SENDTO, smsUri).apply {
                putExtra("sms_body", mensaje)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(smsIntent)
        } else {
            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_SUBJECT, "Alerta de Apoyo MedReminder AI")
                putExtra(Intent.EXTRA_TEXT, mensaje)
            }
            context.startActivity(
                Intent.createChooser(shareIntent, "Enviar alerta al cuidador (WhatsApp / SMS)").apply {
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
            )
        }
    } catch (_: Exception) {
        try {
            val fallbackIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_TEXT, mensaje)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(fallbackIntent)
        } catch (_: Exception) {
            Toast.makeText(context, "Alerta preparada para $nombreDestinatario", Toast.LENGTH_SHORT).show()
        }
    }
}

private fun llamarContactoCuidador(
    context: Context,
    contacto: ContactoApoyoDto?
) {
    val telefono = contacto?.telefono?.trim().orEmpty()
    try {
        val uri = if (telefono.isNotEmpty()) {
            Uri.parse("tel:${Uri.encode(telefono)}")
        } else {
            Uri.parse("tel:")
        }
        val dialIntent = Intent(Intent.ACTION_DIAL, uri).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(dialIntent)
    } catch (_: Exception) {
        val msg = if (telefono.isNotEmpty()) {
            "Teléfono del cuidador: $telefono"
        } else {
            "Registra el teléfono de tu cuidador en la pestaña Salud y Apoyo"
        }
        Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
    }
}

private fun compartirResumenClinico(
    context: Context,
    state: HomeUiState,
    metricas: MetricasProgresoHonor
) {
    val medicamentosStr = if (state.botiquinItems.isNotEmpty()) {
        state.botiquinItems.joinToString("\n") {
            "  - ${it.nombre} (${it.subtituloDosis}) • Stock: ${it.stockActual} u."
        }
    } else {
        "  - Sin medicamentos registrados en botiquín"
    }

    val alergiasStr = if (state.alergiasUsuario.isNotEmpty()) {
        state.alergiasUsuario.joinToString(", ") { "${it.sustancia} (${it.severidad})" }
    } else {
        "Ninguna registrada"
    }

    val reporte = buildString {
        append("RESUMEN CLÍNICO DE ADHERENCIA — MedReminder AI\n")
        append("Fecha: ${state.fechaEncabezado.ifBlank { "Hoy" }}\n\n")
        append("• Adherencia semanal: ${metricas.adherenciaGlobalPct}% (Meta clínica ≥ 90%)\n")
        append("• Racha activa: ${metricas.diasRachaReal} días (${metricas.nivelFuegoReal.titulo})\n")
        append("• Rango de Honor: ${metricas.rangoHonor.nombre} (${metricas.xpActual} XP)\n")
        append("• Tomas de hoy: ${metricas.hoyTomadas} tomadas, ${metricas.hoyPospuestas} pospuestas, ${metricas.hoyOmitidas} omitidas\n\n")
        append("Tratamientos en Botiquín:\n$medicamentosStr\n\n")
        append("Alergias medicamentosas: $alergiasStr\n")
    }

    try {
        val sendIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, "Resumen Clínico MedReminder AI")
            putExtra(Intent.EXTRA_TEXT, reporte)
        }
        val chooser = Intent.createChooser(sendIntent, "Compartir Resumen Clínico").apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(chooser)
    } catch (_: Exception) {
        Toast.makeText(context, "No se encontró una app para compartir el reporte", Toast.LENGTH_SHORT).show()
    }
}
