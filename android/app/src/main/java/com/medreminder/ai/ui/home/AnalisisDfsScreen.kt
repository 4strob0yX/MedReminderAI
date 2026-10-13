package com.medreminder.ai.ui.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AccountTree
import androidx.compose.material.icons.outlined.BarChart
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Loop
import androidx.compose.material.icons.outlined.Route
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.TextMeasurer
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.medreminder.ai.ui.theme.AlertRedBg
import com.medreminder.ai.ui.theme.AlertRedText
import com.medreminder.ai.ui.theme.CardBackground
import com.medreminder.ai.ui.theme.InputBorderColor
import com.medreminder.ai.ui.theme.ProgressBrown
import com.medreminder.ai.ui.theme.SoftWarmSurface
import com.medreminder.ai.ui.theme.TealBadgeBg
import com.medreminder.ai.ui.theme.TealBadgeText
import com.medreminder.ai.ui.theme.TealDark
import com.medreminder.ai.ui.theme.TealPrimary
import com.medreminder.ai.ui.theme.TealSoftBg
import com.medreminder.ai.ui.theme.TextPrimary
import com.medreminder.ai.ui.theme.TextSecondary
import java.util.ArrayDeque
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sin

// ============================================================================
// 1. MODELOS Y MOTOR DE BÚSQUEDA (DFS / BFS + CICLOS + LÍMITE + BACKTRACKING)
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

object MotorBusquedaDfsBfs {

    // Grafo 1: Integración con MedReminder AI (Ciclo de vida de un recordatorio)
    val grafoRecordatorio: Map<String, List<String>> = linkedMapOf(
        "Pendiente" to listOf("Notificado", "EnApp", "Omitido"),
        "EnApp" to listOf("Tomado", "Pospuesto"),
        "Notificado" to listOf("Tomado", "Pospuesto", "Omitido"),
        "Pospuesto" to listOf("Notificado", "Omitido"), // Pospuesto -> Notificado cierra ciclo
        "Tomado" to emptyList(),
        "Omitido" to emptyList()
    )

    // Grafo 2: Ejemplo de clase con ciclo A -> B -> C -> D -> A
    val grafoClase: Map<String, List<String>> = linkedMapOf(
        "A" to listOf("B", "C"),
        "B" to listOf("C", "F"),
        "C" to listOf("D", "F"),
        "D" to listOf("A", "E"), // D -> A cierra ciclo
        "E" to listOf("F"),
        "F" to emptyList()
    )

    /**
     * 2.1 / 2.2 / 2.4 - DFS Clásico (primera solución encontrada)
     * Usa `visitados = mutableSetOf<String>()` global para no expandir estados repetidos.
     */
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
                camino.removeAt(camino.lastIndex) // Backtracking
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

            camino.removeAt(camino.lastIndex) // Backtracking
            return null
        }

        val ruta = visitar(inicio, 0)
        return ResultadoDfsPrimera(ruta, orden, visitados, ciclos, podados)
    }

    /**
     * 2.2 / 2.3 / 2.4 - DFS con Backtracking para encontrar TODAS las rutas posibles.
     * Evita ciclos comprobando `vecino in caminoActual` (en vez de un set global que
     * bloquearía rutas alternativas válidas). Al retroceder (`camino.removeLast()`),
     * el estado queda libre para otras ramas.
     */
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

            camino.removeAt(camino.lastIndex) // Backtracking
        }

        visitar(inicio, 0)
        return ResultadoDfsTodas(rutas, orden, visitados, ciclos, ramasPodadas)
    }

    /**
     * BFS (Búsqueda en Anchura) para comparar con DFS y garantizar la ruta de menor número de pasos.
     */
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
// 2. PANTALLA PRINCIPAL DE ANÁLISIS (DFS/BFS + GRÁFICAS DE ADHERENCIA)
// ============================================================================

private val ColorTomado = Color(0xFF2A9D8F)
private val ColorPospuesto = Color(0xFFE9C46A)
private val ColorOmitido = Color(0xFFE63946)
private val ColorInicio = Color(0xFF1D4E89)
private val ColorPodado = Color(0xFFF4A261)
private val ColoresRutas = listOf(
    Color(0xFF2A9D8F),
    Color(0xFF1D4E89),
    Color(0xFF8E44AD),
    Color(0xFFD97706)
)

@Composable
fun AnalisisDfsScreenContent(state: HomeUiState) {
    var modoGrafo by remember { mutableStateOf(GrafoModo.MEDREMINDER) }
    var limiteProfundidad by remember { mutableIntStateOf(4) }
    var rutaSeleccionadaIdx by remember(modoGrafo, limiteProfundidad) { mutableIntStateOf(0) }

    val grafo = if (modoGrafo == GrafoModo.MEDREMINDER) {
        MotorBusquedaDfsBfs.grafoRecordatorio
    } else {
        MotorBusquedaDfsBfs.grafoClase
    }
    val inicio = if (modoGrafo == GrafoModo.MEDREMINDER) "Pendiente" else "A"
    val meta = if (modoGrafo == GrafoModo.MEDREMINDER) "Tomado" else "F"

    val dfsPrimera = remember(modoGrafo, limiteProfundidad) {
        MotorBusquedaDfsBfs.dfsPrimeraRuta(grafo, inicio, meta, limiteProfundidad)
    }
    val dfsTodas = remember(modoGrafo, limiteProfundidad) {
        MotorBusquedaDfsBfs.dfsTodasLasRutas(grafo, inicio, meta, limiteProfundidad)
    }
    val bfsRes = remember(modoGrafo, limiteProfundidad) {
        MotorBusquedaDfsBfs.bfsRutaMasCorta(grafo, inicio, meta, limiteProfundidad)
    }
    val comparativaLimites = remember(modoGrafo) {
        (1..5).map { lim ->
            val r = MotorBusquedaDfsBfs.dfsTodasLasRutas(grafo, inicio, meta, lim)
            Triple(lim, r.rutas.size, r.ordenExploracion.size)
        }
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(horizontal = 20.dp, vertical = 18.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        // 1. Encabezado y Selector de Grafo
        item {
            EncabezadoModoCard(
                modoActual = modoGrafo,
                onSelectModo = { modoGrafo = it }
            )
        }

        // 2. Control Interactivo de Límite de Profundidad (2.4)
        item {
            ControlLimiteProfundidadCard(
                limite = limiteProfundidad,
                rutasEncontradas = dfsTodas.rutas.size,
                nodosExplorados = dfsTodas.ordenExploracion.size,
                podasCount = dfsTodas.ramasPodadas.size,
                onSelectLimite = { limiteProfundidad = it }
            )
        }

        // 3. Grafo Visual Interactivo con Orden #n, Ciclos y Rutas
        item {
            GrafoVisualCard(
                modo = modoGrafo,
                grafo = grafo,
                inicio = inicio,
                meta = meta,
                dfsPrimera = dfsPrimera,
                dfsTodas = dfsTodas,
                rutaActivaIdx = rutaSeleccionadaIdx,
                onSelectRutaIdx = { rutaSeleccionadaIdx = it }
            )
        }

        // 4. Tarjeta de Resultados: Orden de Exploración vs Ruta Encontrada, Ciclos y BFS
        item {
            ResultadosExploracionCard(
                dfsPrimera = dfsPrimera,
                dfsTodas = dfsTodas,
                bfsRes = bfsRes
            )
        }

        // 5. Tabla y Gráfica Comparativa por Límite de Profundidad (2.4)
        item {
            ComparativaLimitesCard(comparativa = comparativaLimites, limiteActual = limiteProfundidad)
        }

        // 6. Gráfica 1 Mejorada: Adherencia Semanal y Tomas de Hoy en Vivo
        item {
            Grafica1AdherenciaCard(state = state)
        }

        // 7. Gráfica 3 Mejorada: Paletas Profesionales (Secuencial Mapa de Calor + Semáforo por Medicamento)
        item {
            Grafica3PaletasCard(state = state)
        }
    }
}

// ============================================================================
// 3. COMPONENTES DE INTERFAZ Y VISUALIZACIÓN
// ============================================================================

@Composable
private fun EncabezadoModoCard(
    modoActual: GrafoModo,
    onSelectModo: (GrafoModo) -> Unit
) {
    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    shape = CircleShape,
                    color = TealBadgeBg,
                    modifier = Modifier.size(40.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Outlined.AccountTree,
                            contentDescription = null,
                            tint = TealPrimary,
                            modifier = Modifier.size(22.dp)
                        )
                    }
                }
                Spacer(Modifier.width(12.dp))
                Column {
                    Text(
                        text = "BÚSQUEDA CIEGA DFS / BFS Y VISUALIZACIÓN",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.ExtraBold,
                        letterSpacing = 0.7.sp,
                        color = TealPrimary
                    )
                    Text(
                        text = "Exploración de Estados y Adherencia",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                GrafoModo.entries.forEach { modo ->
                    val selected = modo == modoActual
                    val labelCorto = if (modo == GrafoModo.MEDREMINDER) "Proyecto MedReminder" else "Grafo de Clase (A→F)"
                    Surface(
                        shape = RoundedCornerShape(14.dp),
                        color = if (selected) TealPrimary else SoftWarmSurface,
                        modifier = Modifier
                            .weight(1f)
                            .heightIn(min = 48.dp)
                            .clip(RoundedCornerShape(14.dp))
                            .clickable { onSelectModo(modo) }
                    ) {
                        Box(
                            contentAlignment = Alignment.Center,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 10.dp)
                        ) {
                            Text(
                                text = labelCorto,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (selected) Color.White else TextPrimary,
                                textAlign = TextAlign.Center
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(10.dp))
            Text(
                text = modoActual.subtitulo,
                fontSize = 13.sp,
                color = TextSecondary
            )
        }
    }
}

@Composable
private fun ControlLimiteProfundidadCard(
    limite: Int,
    rutasEncontradas: Int,
    nodosExplorados: Int,
    podasCount: Int,
    onSelectLimite: (Int) -> Unit
) {
    Surface(
        shape = RoundedCornerShape(22.dp),
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
                Column {
                    Text(
                        text = "2.4 LÍMITE DE PROFUNDIDAD",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TealPrimary,
                        letterSpacing = 0.7.sp
                    )
                    Text(
                        text = "Nivel máximo permitido: $limite",
                        fontSize = 17.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = TextPrimary
                    )
                }
                Surface(
                    shape = RoundedCornerShape(50),
                    color = TealBadgeBg
                ) {
                    Text(
                        text = "$rutasEncontradas rutas",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = TealBadgeText,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                    )
                }
            }

            Spacer(Modifier.height(12.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                (1..5).forEach { nivel ->
                    val activo = nivel == limite
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = if (activo) TealPrimary else SoftWarmSurface,
                        modifier = Modifier
                            .weight(1f)
                            .height(48.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .clickable { onSelectLimite(nivel) }
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Text(
                                text = "Niv. $nivel",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (activo) Color.White else TextPrimary
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(12.dp))
            Text(
                text = "Con límite $limite: se revisaron $nodosExplorados estados y se podaron $podasCount ramas al alcanzar el tope (en MedReminder equivale al límite de posposiciones antes de marcar Omitido).",
                fontSize = 12.5.sp,
                color = TextSecondary,
                lineHeight = 17.sp
            )
        }
    }
}

@Composable
private fun GrafoVisualCard(
    modo: GrafoModo,
    grafo: Map<String, List<String>>,
    inicio: String,
    meta: String,
    dfsPrimera: ResultadoDfsPrimera,
    dfsTodas: ResultadoDfsTodas,
    rutaActivaIdx: Int,
    onSelectRutaIdx: (Int) -> Unit
) {
    val textMeasurer = rememberTextMeasurer()
    val rutaResaltada = dfsTodas.rutas.getOrNull(rutaActivaIdx) ?: dfsPrimera.ruta.orEmpty()

    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Text(
                text = "GRAFO DE ESTADOS (#n = orden de exploración DFS)",
                fontSize = 11.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TealPrimary,
                letterSpacing = 0.7.sp
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = if (modo == GrafoModo.MEDREMINDER) {
                    "Ciclo de vida de un recordatorio"
                } else {
                    "Espacio de estados con ciclo cerrado D → A"
                },
                fontSize = 17.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )

            Spacer(Modifier.height(12.dp))

            // Lienzo del grafo
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = SoftWarmSurface,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(250.dp)
            ) {
                Canvas(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(14.dp)
                ) {
                    val posiciones: Map<String, Offset> = if (modo == GrafoModo.MEDREMINDER) {
                        mapOf(
                            "Pendiente" to Offset(size.width * 0.12f, size.height * 0.50f),
                            "EnApp" to Offset(size.width * 0.42f, size.height * 0.18f),
                            "Notificado" to Offset(size.width * 0.42f, size.height * 0.82f),
                            "Pospuesto" to Offset(size.width * 0.66f, size.height * 0.50f),
                            "Tomado" to Offset(size.width * 0.90f, size.height * 0.22f),
                            "Omitido" to Offset(size.width * 0.90f, size.height * 0.82f)
                        )
                    } else {
                        mapOf(
                            "A" to Offset(size.width * 0.14f, size.height * 0.24f),
                            "B" to Offset(size.width * 0.48f, size.height * 0.24f),
                            "C" to Offset(size.width * 0.48f, size.height * 0.78f),
                            "D" to Offset(size.width * 0.14f, size.height * 0.78f),
                            "F" to Offset(size.width * 0.86f, size.height * 0.34f),
                            "E" to Offset(size.width * 0.86f, size.height * 0.82f)
                        )
                    }

                    val radio = 24.dp.toPx()
                    val aristasRuta = rutaResaltada.zipWithNext().toSet()
                    val aristasCiclo = dfsTodas.ciclosEvitados.toSet()

                    // 1. Dibujar aristas base
                    grafo.forEach { (u, vecinos) ->
                        val p1 = posiciones[u] ?: return@forEach
                        vecinos.forEach { v ->
                            val p2 = posiciones[v] ?: return@forEach
                            val esCiclo = (u to v) in aristasCiclo
                            val esRuta = (u to v) in aristasRuta
                            if (!esCiclo && !esRuta) {
                                dibujarFlecha(p1, p2, radio, Color(0xFFB5BDC4), 2.dp.toPx(), false)
                            }
                        }
                    }

                    // 2. Dibujar aristas de ciclo detectado y evitado (rojo punteado)
                    aristasCiclo.forEach { (u, v) ->
                        val p1 = posiciones[u] ?: return@forEach
                        val p2 = posiciones[v] ?: return@forEach
                        dibujarFlecha(p1, p2, radio, ColorOmitido, 3.dp.toPx(), true)
                    }

                    // 3. Dibujar aristas de la ruta seleccionada
                    val colorRuta = ColoresRutas[rutaActivaIdx % ColoresRutas.size]
                    aristasRuta.forEach { (u, v) ->
                        val p1 = posiciones[u] ?: return@forEach
                        val p2 = posiciones[v] ?: return@forEach
                        dibujarFlecha(p1, p2, radio, colorRuta, 4.dp.toPx(), false)
                    }

                    // 4. Orden #n de exploración en la primera visita
                    val ordenMap = linkedMapOf<String, Int>()
                    dfsPrimera.ordenExploracion.forEach { n ->
                        if (n !in ordenMap) ordenMap[n] = ordenMap.size + 1
                    }
                    val nodosPodados = dfsTodas.ramasPodadas.mapNotNull { it.lastOrNull() }.toSet()

                    // 5. Dibujar nodos
                    posiciones.forEach { (nodo, centro) ->
                        val fill = when {
                            nodo == inicio -> ColorInicio
                            nodo == meta -> ColorTomado
                            nodo in nodosPodados -> ColorPodado
                            nodo in rutaResaltada -> TealPrimary
                            else -> Color.White
                        }
                        val txtColor = if (fill == Color.White || fill == ColorPodado) TextPrimary else Color.White

                        drawCircle(color = fill, radius = radio, center = centro)
                        drawCircle(
                            color = TealDark,
                            radius = radio,
                            center = centro,
                            style = Stroke(width = 2.dp.toPx())
                        )

                        dibujarTextoCentrado(
                            textMeasurer = textMeasurer,
                            texto = nodo,
                            centro = centro,
                            color = txtColor,
                            fontSizeSp = if (nodo.length > 6) 9.5f else 12f
                        )

                        ordenMap[nodo]?.let { num ->
                            val badgeCenter = Offset(centro.x, centro.y - radio - 10.dp.toPx())
                            dibujarTextoCentrado(
                                textMeasurer = textMeasurer,
                                texto = "#$num",
                                centro = badgeCenter,
                                color = TealDark,
                                fontSizeSp = 10f
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // Leyenda compacta
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                LeyendaDot("Inicio", ColorInicio)
                LeyendaDot("Objetivo", ColorTomado)
                LeyendaDot("Podado", ColorPodado)
                LeyendaDot("Ciclo evitado", ColorOmitido)
            }

            // Selector de rutas encontradas (2.3)
            if (dfsTodas.rutas.isNotEmpty()) {
                Spacer(Modifier.height(14.dp))
                Text(
                    text = "2.3 TODAS LAS RUTAS ENCONTRADAS (toca para resaltar):",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = TealPrimary
                )
                Spacer(Modifier.height(8.dp))
                dfsTodas.rutas.forEachIndexed { idx, ruta ->
                    val activa = idx == rutaActivaIdx
                    val col = ColoresRutas[idx % ColoresRutas.size]
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = if (activa) col.copy(alpha = 0.14f) else SoftWarmSurface,
                        border = BorderStroke(1.dp, if (activa) col else InputBorderColor),
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 3.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .clickable { onSelectRutaIdx(idx) }
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 9.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Route,
                                contentDescription = null,
                                tint = col,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(
                                text = "Ruta ${idx + 1}: ${ruta.joinToString(" → ")}",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = TextPrimary,
                                modifier = Modifier.weight(1f)
                            )
                            Text(
                                text = "${ruta.size - 1} pasos",
                                fontSize = 11.5.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = TextSecondary
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ResultadosExploracionCard(
    dfsPrimera: ResultadoDfsPrimera,
    dfsTodas: ResultadoDfsTodas,
    bfsRes: ResultadoBfs
) {
    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text(
                text = "2.1 ORDEN DE EXPLORACIÓN ≠ RUTA ENCONTRADA",
                fontSize = 11.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TealPrimary,
                letterSpacing = 0.7.sp
            )

            BloqueMetrica(
                titulo = "Orden de exploración (DFS 1ª solución)",
                valor = dfsPrimera.ordenExploracion.joinToString(" → "),
                nota = "Todos los nodos que el algoritmo revisó antes de llegar a la meta."
            )

            BloqueMetrica(
                titulo = "Ruta encontrada (DFS 1ª solución)",
                valor = dfsPrimera.ruta?.joinToString(" → ") ?: "Sin solución dentro del límite",
                nota = "Camino final tras aplicar backtracking en las ramas sin salida."
            )

            BloqueMetrica(
                titulo = "Nodos visitados (visitados = set())",
                valor = dfsTodas.visitados.joinToString(", "),
                nota = "Total de estados únicos alcanzados: ${dfsTodas.visitados.size}."
            )

            HorizontalDivider(color = InputBorderColor)

            // 2.2 Control de ciclos
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Outlined.Loop,
                    contentDescription = null,
                    tint = ColorOmitido,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(Modifier.width(6.dp))
                Text(
                    text = "2.2 DETECCIÓN Y EVASIÓN DE CICLOS INFINITOS",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = ColorOmitido
                )
            }

            val ciclosStr = dfsTodas.ciclosEvitados
                .map { "${it.first} → ${it.second}" }
                .distinct()
                .ifEmpty { listOf("Ningún ciclo alcanzado con este límite") }
                .joinToString("  •  ")

            Surface(
                shape = RoundedCornerShape(12.dp),
                color = AlertRedBg,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(
                        text = "Ciclos bloqueados: $ciclosStr",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Bold,
                        color = AlertRedText
                    )
                    Spacer(Modifier.height(3.dp))
                    Text(
                        text = "Mecanismo: antes de expandir un vecino se verifica si ya pertenece al camino/conjunto visitado; así se evita el bucle infinito.",
                        fontSize = 12.sp,
                        color = TextPrimary,
                        lineHeight = 16.sp
                    )
                }
            }

            HorizontalDivider(color = InputBorderColor)

            BloqueMetrica(
                titulo = "Comparación con BFS (Búsqueda en Anchura)",
                valor = "Exploración: ${bfsRes.ordenExploracion.joinToString(" → ")}\nRuta óptima: ${bfsRes.rutaMasCorta?.joinToString(" → ") ?: "N/A"}",
                nota = "BFS explora por niveles usando una cola FIFO y garantiza la ruta de menor número de pasos."
            )
        }
    }
}

@Composable
private fun ComparativaLimitesCard(
    comparativa: List<Triple<Int, Int, Int>>,
    limiteActual: Int
) {
    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Text(
                text = "PRUEBA CON DIFERENTES LÍMITES DE PROFUNDIDAD",
                fontSize = 11.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TealPrimary,
                letterSpacing = 0.7.sp
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = "Cómo cambia la búsqueda al variar el límite",
                fontSize = 17.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )
            Spacer(Modifier.height(12.dp))

            val maxExpl = comparativa.maxOfOrNull { it.third }?.coerceAtLeast(1) ?: 1

            comparativa.forEach { (lim, rutas, explorados) ->
                val activo = lim == limiteActual
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 5.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Límite $lim",
                        fontSize = 13.sp,
                        fontWeight = if (activo) FontWeight.ExtraBold else FontWeight.SemiBold,
                        color = if (activo) TealPrimary else TextPrimary,
                        modifier = Modifier.width(68.dp)
                    )
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth((explorados.toFloat() / maxExpl).coerceIn(0.08f, 1f))
                                    .height(10.dp)
                                    .clip(RoundedCornerShape(50))
                                    .background(if (activo) TealPrimary else ColorInicio.copy(alpha = 0.65f))
                            )
                        }
                        Spacer(Modifier.height(3.dp))
                        Text(
                            text = "$rutas rutas encontradas • $explorados estados explorados",
                            fontSize = 11.5.sp,
                            color = TextSecondary
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun Grafica1AdherenciaCard(state: HomeUiState) {
    // Semanas históricas + semana actual alimentada en vivo si hay datos hoy
    val semanas = listOf("S1", "S2", "S3", "S4", "S5", "S6", "S7", "Hoy")
    val hoyTotal = state.tomasHoy.size
    val hoyTomadas = state.tomasHoy.count { it.estado == "tomado" }
    val hoyPosp = state.tomasHoy.count { it.estado == "pendiente" && it.vecesPospuesto > 0 }
    val hoyOmit = state.tomasHoy.count { it.estado == "omitido" }

    val tomadas = listOf(38, 41, 37, 33, 40, 43, 45, if (hoyTotal > 0) hoyTomadas else 46)
    val pospuestas = listOf(4, 3, 5, 6, 4, 2, 2, if (hoyTotal > 0) hoyPosp else 1)
    val omitidas = listOf(3, 1, 5, 8, 2, 0, 0, if (hoyTotal > 0) hoyOmit else 0)

    val porcentajes = semanas.indices.map { i ->
        val tot = (tomadas[i] + pospuestas[i] + omitidas[i]).coerceAtLeast(1)
        ((tomadas[i].toFloat() / tot) * 100f).toInt()
    }

    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Outlined.BarChart,
                    contentDescription = null,
                    tint = TealPrimary,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    text = "1. GRÁFICA 1 MEJORADA: ADHERENCIA AL TRATAMIENTO",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = TealPrimary,
                    letterSpacing = 0.6.sp
                )
            }
            Spacer(Modifier.height(4.dp))
            Text(
                text = "Composición de Tomas y Meta Clínica (90%)",
                fontSize = 17.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )
            Text(
                text = "Paleta semántica coherente: Tomado (verde) • Pospuesto (ámbar) • Omitido (rojo)",
                fontSize = 12.sp,
                color = TextSecondary
            )

            Spacer(Modifier.height(14.dp))

            // Barras apiladas + % de adherencia
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(150.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.Bottom
            ) {
                semanas.indices.forEach { i ->
                    val tot = (tomadas[i] + pospuestas[i] + omitidas[i]).coerceAtLeast(1).toFloat()
                    val pct = porcentajes[i]
                    val esPeor = i == 3 // S4 semana crítica

                    Column(
                        modifier = Modifier.weight(1f),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Bottom
                    ) {
                        Text(
                            text = "$pct%",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (esPeor) ColorOmitido else TealDark
                        )
                        Spacer(Modifier.height(4.dp))
                        Column(
                            modifier = Modifier
                                .width(22.dp)
                                .height(104.dp)
                                .clip(RoundedCornerShape(6.dp))
                                .background(SoftWarmSurface)
                        ) {
                            if (omitidas[i] > 0) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .weight(omitidas[i] / tot)
                                        .background(ColorOmitido)
                                )
                            }
                            if (pospuestas[i] > 0) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .weight(pospuestas[i] / tot)
                                        .background(ColorPospuesto)
                                )
                            }
                            if (tomadas[i] > 0) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .weight((tomadas[i] / tot).coerceAtLeast(0.05f))
                                        .background(ColorTomado)
                                )
                            }
                        }
                        Spacer(Modifier.height(5.dp))
                        Text(
                            text = semanas[i],
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (esPeor) ColorOmitido else TextPrimary
                        )
                    }
                }
            }

            Spacer(Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                LeyendaDot("Tomado", ColorTomado)
                LeyendaDot("Pospuesto", ColorPospuesto)
                LeyendaDot("Omitido", ColorOmitido)
                LeyendaDot("Meta ≥ 90%", ColorInicio)
            }
        }
    }
}

@Composable
private fun Grafica3PaletasCard(state: HomeUiState) {
    val dias = listOf("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
    val bloques = listOf("08h", "14h", "20h", "22h")
    // Matriz secuencial de omisiones (más oscuro = mayor concentración en fin de semana noche)
    val matrizOmisiones = listOf(
        listOf(1, 0, 0, 1),
        listOf(0, 1, 0, 0),
        listOf(1, 0, 1, 0),
        listOf(0, 1, 0, 1),
        listOf(0, 1, 2, 2),
        listOf(1, 2, 4, 5),
        listOf(0, 1, 3, 4)
    )

    // Lista de medicamentos (usa los del botiquín real del usuario si existen, o los de referencia)
    val medsAdherencia: List<Pair<String, Int>> = if (state.botiquinItems.isNotEmpty()) {
        state.botiquinItems.map { it.nombre to it.porcentajeRestante.coerceIn(55, 98) }
    } else {
        listOf(
            "Metformina" to 94,
            "Atorvastatina" to 91,
            "Losartán" to 86,
            "Vitamina D" to 79,
            "Omeprazol" to 71
        )
    }

    Surface(
        shape = RoundedCornerShape(22.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, InputBorderColor),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Text(
                text = "1. GRÁFICA 3 MEJORADA: TEORÍA DEL COLOR APLICADA",
                fontSize = 11.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TealPrimary,
                letterSpacing = 0.6.sp
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = "Mapa de Calor (Paleta Secuencial) y Semáforo por Medicamento",
                fontSize = 17.sp,
                fontWeight = FontWeight.ExtraBold,
                color = TextPrimary
            )
            Spacer(Modifier.height(12.dp))

            // Subgráfica A: Mapa de calor secuencial (Reds)
            Text(
                text = "A) Paleta Secuencial: Omisiones por Día y Hora (más intenso = más olvidos)",
                fontSize = 12.5.sp,
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
            Spacer(Modifier.height(8.dp))

            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Spacer(Modifier.width(42.dp))
                bloques.forEach { h ->
                    Text(
                        text = h,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextSecondary,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
            Spacer(Modifier.height(4.dp))

            dias.forEachIndexed { r, dia ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 2.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = dia,
                        fontSize = 11.5.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextPrimary,
                        modifier = Modifier.width(42.dp)
                    )
                    matrizOmisiones[r].forEach { valor ->
                        val intensidad = (valor / 5f).coerceIn(0f, 1f)
                        val bg = Color.hsv(
                            hue = 355f,
                            saturation = 0.12f + 0.75f * intensidad,
                            value = 0.98f - 0.25f * intensidad
                        )
                        val txtCol = if (intensidad > 0.55f) Color.White else TextPrimary
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .padding(horizontal = 3.dp)
                                .height(26.dp)
                                .clip(RoundedCornerShape(6.dp))
                                .background(bg),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = valor.toString(),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = txtCol
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(16.dp))
            HorizontalDivider(color = InputBorderColor)
            Spacer(Modifier.height(12.dp))

            // Subgráfica B: Semáforo categórico por medicamento
            Text(
                text = "B) Paleta Categórica con Significado Clínico (Verde ≥90% • Ámbar 80-89% • Rojo <80%)",
                fontSize = 12.5.sp,
                fontWeight = FontWeight.Bold,
                color = TextPrimary
            )
            Spacer(Modifier.height(8.dp))

            medsAdherencia.forEach { (nombre, pct) ->
                val colorBarra = when {
                    pct >= 90 -> ColorTomado
                    pct >= 80 -> ColorPospuesto
                    else -> ColorOmitido
                }
                Column(modifier = Modifier.padding(vertical = 4.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(
                            text = nombre,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Text(
                            text = "$pct%",
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = if (pct < 80) ColorOmitido else TextPrimary
                        )
                    }
                    Spacer(Modifier.height(4.dp))
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(9.dp)
                            .clip(RoundedCornerShape(50))
                            .background(SoftWarmSurface)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth((pct / 100f).coerceIn(0.08f, 1f))
                                .fillMaxHeight()
                                .clip(RoundedCornerShape(50))
                                .background(colorBarra)
                        )
                    }
                }
            }

            Spacer(Modifier.height(10.dp))
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = SoftWarmSurface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Info,
                        contentDescription = null,
                        tint = TealPrimary,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = "Conclusión: las omisiones se concentran los sábados y domingos por la noche (20h–22h).",
                        fontSize = 12.sp,
                        color = TextPrimary,
                        lineHeight = 16.sp
                    )
                }
            }
        }
    }
}

// ============================================================================
// 4. UTILIDADES DE DIBUJO EN CANVAS Y BLOQUES DE TEXTO
// ============================================================================

@Composable
private fun BloqueMetrica(titulo: String, valor: String, nota: String) {
    Column {
        Text(
            text = titulo,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            color = TextSecondary
        )
        Spacer(Modifier.height(2.dp))
        Text(
            text = valor,
            fontSize = 14.sp,
            fontWeight = FontWeight.ExtraBold,
            color = TextPrimary,
            lineHeight = 19.sp
        )
        Spacer(Modifier.height(2.dp))
        Text(
            text = nota,
            fontSize = 11.5.sp,
            color = TextSecondary
        )
    }
}

@Composable
private fun LeyendaDot(label: String, color: Color) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Box(
            modifier = Modifier
                .size(10.dp)
                .clip(CircleShape)
                .background(color)
        )
        Spacer(Modifier.width(5.dp))
        Text(
            text = label,
            fontSize = 11.sp,
            fontWeight = FontWeight.SemiBold,
            color = TextSecondary
        )
    }
}

private fun DrawScope.dibujarFlecha(
    desde: Offset,
    hasta: Offset,
    radioNodo: Float,
    color: Color,
    grosor: Float,
    punteada: Boolean
) {
    val dx = hasta.x - desde.x
    val dy = hasta.y - desde.y
    val angulo = atan2(dy, dx)

    val inicio = Offset(
        desde.x + cos(angulo) * radioNodo,
        desde.y + sin(angulo) * radioNodo
    )
    val fin = Offset(
        hasta.x - cos(angulo) * (radioNodo + 4.dp.toPx()),
        hasta.y - sin(angulo) * (radioNodo + 4.dp.toPx())
    )

    drawLine(
        color = color,
        start = inicio,
        end = fin,
        strokeWidth = grosor,
        cap = StrokeCap.Round,
        pathEffect = if (punteada) PathEffect.dashPathEffect(floatArrayOf(12f, 10f), 0f) else null
    )

    val tamPunta = 10.dp.toPx()
    val ang1 = angulo - Math.toRadians(28.0).toFloat()
    val ang2 = angulo + Math.toRadians(28.0).toFloat()
    val p1 = Offset(fin.x - cos(ang1) * tamPunta, fin.y - sin(ang1) * tamPunta)
    val p2 = Offset(fin.x - cos(ang2) * tamPunta, fin.y - sin(ang2) * tamPunta)

    val path = Path().apply {
        moveTo(fin.x, fin.y)
        lineTo(p1.x, p1.y)
        lineTo(p2.x, p2.y)
        close()
    }
    drawPath(path = path, color = color)
}

private fun DrawScope.dibujarTextoCentrado(
    textMeasurer: TextMeasurer,
    texto: String,
    centro: Offset,
    color: Color,
    fontSizeSp: Float
) {
    val layout = textMeasurer.measure(
        text = texto,
        style = TextStyle(
            color = color,
            fontSize = fontSizeSp.sp,
            fontWeight = FontWeight.ExtraBold
        )
    )
    drawText(
        textLayoutResult = layout,
        topLeft = Offset(
            centro.x - layout.size.width / 2f,
            centro.y - layout.size.height / 2f
        )
    )
}
