"""
==============================================================================
COMPARACIÓN INTERACTIVA: BÚSQUEDA HEURÍSTICA vs COSTO UNIFORME (UCS)
==============================================================================
Interfaz Gráfica Minimalista y Moderna con Tkinter (Colores Neutros)
Diseñado con renderizado limpio adaptado para macOS y Linux/Windows.
==============================================================================
"""

import tkinter as tk
import heapq

# ==============================================================================
# 1. MODELOS DE DATOS
# ==============================================================================

GRAFO_UCS = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2), ('G', 8)],
    'D': [('H', 3)],
    'E': [('I', 2)],
    'F': [('J', 3)],
    'G': [],
    'H': [],
    'I': [],
    'J': []
}

ARBOL_HEURISTICA = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': ['I'],
    'F': ['J'],
    'G': [],
    'H': [],
    'I': [],
    'J': []
}

HEURISTICAS = {
    'A': 7, 'B': 6, 'C': 4, 'D': 7, 'E': 5,
    'F': 3, 'G': 6, 'H': 8, 'I': 1, 'J': 0
}

INICIO = 'A'
META = 'J'

# Posiciones matemáticamente centradas y alineadas en el Canvas (540 x 420)
# Nivel 0: A(270)
# Nivel 1: B(150), C(390)
# Nivel 2: D(90), E(210), F(330), G(450)
# Nivel 3: H(90), I(210), J(330)
POSICIONES = {
    'A': (270, 50),
    'B': (150, 140),
    'C': (390, 140),
    'D': (90, 240),
    'E': (210, 240),
    'F': (330, 240),
    'G': (450, 240),
    'H': (90, 340),
    'I': (210, 340),
    'J': (330, 340)
}


# ==============================================================================
# 2. LÓGICA DE ALGORITMOS
# ==============================================================================

def ejecutar_heuristica():
    actual = INICIO
    ruta = [actual]
    visitados = [actual]
    costo_total = 0

    while actual != META:
        hijos = ARBOL_HEURISTICA.get(actual, [])
        if not hijos:
            break
        mejor_hijo = min(hijos, key=lambda n: HEURISTICAS.get(n, 999))
        costo_total += HEURISTICAS.get(mejor_hijo, 0)
        actual = mejor_hijo
        ruta.append(actual)
        visitados.append(actual)

    return {
        'ruta': ruta,
        'visitados': visitados,
        'costo': costo_total,
        'nombre': 'Búsqueda Heurística (h)'
    }


def ejecutar_ucs():
    cola = [(0, INICIO, [INICIO])]
    visitados_set = set()
    orden_explorado = []

    while cola:
        costo, actual, ruta = heapq.heappop(cola)
        if actual not in orden_explorado:
            orden_explorado.append(actual)

        if actual == META:
            return {
                'ruta': ruta,
                'visitados': orden_explorado,
                'costo': costo,
                'nombre': 'Costo Uniforme (UCS)'
            }

        if actual not in visitados_set:
            visitados_set.add(actual)
            for vecino, peso in GRAFO_UCS.get(actual, []):
                if vecino not in visitados_set:
                    heapq.heappush(cola, (costo + peso, vecino, ruta + [vecino]))

    return {'ruta': [], 'visitados': orden_explorado, 'costo': 0, 'nombre': 'UCS'}


# ==============================================================================
# 3. COMPONENTE: BOTÓN PILL PERSONALIZADO (Solución estética para macOS)
# ==============================================================================

class PillButton(tk.Canvas):
    """Botón redondeado minimalista que evita los problemas de renderizado de macOS."""
    def __init__(self, parent, text, command, bg_color="#18181B", fg_color="#FFFFFF", hover_color="#27272A", height=38):
        super().__init__(parent, height=height, bg=parent["bg"], highlightthickness=0, cursor="hand2")
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.current_bg = bg_color
        self.h = height

        self.bind("<Configure>", self._redibujar)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _redibujar(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.h
        r = h // 2

        if w < 10:
            return

        # Dibujar forma redondeada (píldora)
        self.create_oval(2, 2, 2 + h - 4, h - 2, fill=self.current_bg, outline=self.current_bg)
        self.create_oval(w - h + 2, 2, w - 2, h - 2, fill=self.current_bg, outline=self.current_bg)
        self.create_rectangle(r, 2, w - r, h - 2, fill=self.current_bg, outline=self.current_bg)

        # Texto centrado
        self.create_text(
            w / 2, h / 2,
            text=self.text,
            fill=self.fg_color,
            font=("SF Pro Text", 10, "bold")
        )

    def _on_enter(self, e):
        self.current_bg = self.hover_color
        self._redibujar()

    def _on_leave(self, e):
        self.current_bg = self.bg_color
        self._redibujar()

    def _on_click(self, e):
        if self.command:
            self.command()


# ==============================================================================
# 4. INTERFAZ GRÁFICA PRINCIPAL
# ==============================================================================

class ComparadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comparación Heurística vs Costo Uniforme")
        self.geometry("980x670")
        self.minsize(940, 640)

        # Paleta Neutra Minimalista
        self.c_bg = "#F8F9FA"         # Fondo general
        self.c_card = "#FFFFFF"       # Tarjeta
        self.c_border = "#E2E8F0"     # Bordes sutiles
        self.c_text = "#0F172A"       # Texto principal oscuro
        self.c_muted = "#64748B"      # Texto secundario
        self.c_pill = "#F1F5F9"       # Fondo insignias
        self.c_edge = "#E2E8F0"       # Líneas normales
        self.c_active_edge = "#0F172A"# Líneas de la ruta activa

        self.configure(bg=self.c_bg)

        self._crear_interfaz()
        self.dibujar_grafo()

    def _crear_interfaz(self):
        # Header Superior
        header = tk.Frame(self, bg=self.c_bg, padx=32, pady=18)
        header.pack(fill=tk.X)

        lbl_t = tk.Label(
            header,
            text="Comparación: Heurística vs Costo Uniforme (UCS)",
            font=("SF Pro Display", 18, "bold"),
            bg=self.c_bg,
            fg=self.c_text
        )
        lbl_t.pack(anchor="w")

        lbl_sub = tk.Label(
            header,
            text="Análisis comparativo de exploración: criterio voraz f(n)=h(n) vs costo real acumulado f(n)=g(n).",
            font=("SF Pro Text", 10),
            bg=self.c_bg,
            fg=self.c_muted
        )
        lbl_sub.pack(anchor="w", pady=(3, 0))

        # Contenedor Horizontal Principal
        body = tk.Frame(self, bg=self.c_bg, padx=32)
        body.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # COLUMNA IZQUIERDA: CANVAS DEL ÁRBOL
        # -------------------------------------------------------------
        left_card = tk.Frame(body, bg=self.c_card, highlightbackground=self.c_border, highlightthickness=1)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 16), pady=(0, 20))

        card_header = tk.Frame(left_card, bg=self.c_card, padx=18, pady=12)
        card_header.pack(fill=tk.X)

        tk.Label(
            card_header,
            text="ESTRUCTURA DEL ÁRBOL",
            font=("SF Pro Text", 9, "bold"),
            bg=self.c_card,
            fg=self.c_muted
        ).pack(side=tk.LEFT)

        self.lbl_badge = tk.Label(
            card_header,
            text="Listo para simular",
            font=("SF Pro Text", 9),
            bg=self.c_pill,
            fg=self.c_muted,
            padx=10,
            pady=4
        )
        self.lbl_badge.pack(side=tk.RIGHT)

        # Canvas con tamaño proporcional
        self.canvas = tk.Canvas(left_card, bg=self.c_card, highlightthickness=0, width=540, height=420)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        # -------------------------------------------------------------
        # COLUMNA DERECHA: ACCIONES Y MÉTRICAS
        # -------------------------------------------------------------
        right_panel = tk.Frame(body, bg=self.c_bg, width=360)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, pady=(0, 20))
        right_panel.pack_propagate(False)

        # Tarjeta 1: Acciones
        act_card = tk.Frame(right_panel, bg=self.c_card, highlightbackground=self.c_border, highlightthickness=1, padx=18, pady=16)
        act_card.pack(fill=tk.X, pady=(0, 14))

        tk.Label(
            act_card,
            text="ACCIONES",
            font=("SF Pro Text", 9, "bold"),
            bg=self.c_card,
            fg=self.c_muted
        ).pack(anchor="w", pady=(0, 10))

        btn_heur = PillButton(
            act_card,
            text="▶ Búsqueda Heurística (h)",
            command=self.simular_heuristica,
            bg_color="#18181B",
            fg_color="#FFFFFF",
            hover_color="#27272A"
        )
        btn_heur.pack(fill=tk.X, pady=(0, 8))

        btn_ucs = PillButton(
            act_card,
            text="▶ Costo Uniforme (UCS)",
            command=self.simular_ucs,
            bg_color="#334155",
            fg_color="#FFFFFF",
            hover_color="#475569"
        )
        btn_ucs.pack(fill=tk.X, pady=(0, 8))

        btn_ambos = PillButton(
            act_card,
            text="⚖ Comparar Ambos",
            command=self.comparar_ambos,
            bg_color="#F1F5F9",
            fg_color="#0F172A",
            hover_color="#E2E8F0"
        )
        btn_ambos.pack(fill=tk.X, pady=(0, 8))

        btn_reset = PillButton(
            act_card,
            text="↺ Reiniciar",
            command=self.reset,
            bg_color="#FFFFFF",
            fg_color="#64748B",
            hover_color="#F8F9FA",
            height=32
        )
        btn_reset.pack(fill=tk.X)

        # Tarjeta 2: Métricas
        met_card = tk.Frame(right_panel, bg=self.c_card, highlightbackground=self.c_border, highlightthickness=1, padx=18, pady=16)
        met_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            met_card,
            text="MÉTRICAS COMPARATIVAS",
            font=("SF Pro Text", 9, "bold"),
            bg=self.c_card,
            fg=self.c_muted
        ).pack(anchor="w", pady=(0, 10))

        # Bloque Heurística
        self.box_h = tk.Frame(met_card, bg=self.c_pill, padx=12, pady=10)
        self.box_h.pack(fill=tk.X, pady=(0, 8))
        tk.Label(self.box_h, text="Búsqueda Heurística (pheuristica.py)", font=("SF Pro Text", 9, "bold"), bg=self.c_pill, fg=self.c_text).pack(anchor="w")
        self.lbl_h_ruta = tk.Label(self.box_h, text="Ruta: -", font=("SF Pro Text", 9), bg=self.c_pill, fg=self.c_muted)
        self.lbl_h_ruta.pack(anchor="w", pady=(2, 0))
        self.lbl_h_costo = tk.Label(self.box_h, text="Costo h: -  |  Visitados: -", font=("SF Pro Text", 9), bg=self.c_pill, fg=self.c_muted)
        self.lbl_h_costo.pack(anchor="w")

        # Bloque UCS
        self.box_ucs = tk.Frame(met_card, bg=self.c_pill, padx=12, pady=10)
        self.box_ucs.pack(fill=tk.X, pady=(0, 10))
        tk.Label(self.box_ucs, text="Costo Uniforme (ucs.py)", font=("SF Pro Text", 9, "bold"), bg=self.c_pill, fg=self.c_text).pack(anchor="w")
        self.lbl_ucs_ruta = tk.Label(self.box_ucs, text="Ruta: -", font=("SF Pro Text", 9), bg=self.c_pill, fg=self.c_text)
        self.lbl_ucs_ruta.pack(anchor="w", pady=(2, 0))
        self.lbl_ucs_costo = tk.Label(self.box_ucs, text="Costo g: -  |  Visitados: -", font=("SF Pro Text", 9), bg=self.c_pill, fg=self.c_muted)
        self.lbl_ucs_costo.pack(anchor="w")

        # Resumen / Explicación
        self.lbl_concl = tk.Label(
            met_card,
            text="Presiona cualquier botón para simular y ver la comparación de rendimiento en el árbol.",
            font=("SF Pro Text", 9),
            bg=self.c_card,
            fg=self.c_muted,
            wraplength=310,
            justify="left"
        )
        self.lbl_concl.pack(anchor="w", pady=(6, 0))

    # ==========================================================================
    # 5. DIBUJO LIMPIO DEL ÁRBOL
    # ==========================================================================

    def dibujar_grafo(self, ruta_activa=None, nodos_visitados=None):
        self.canvas.delete("all")
        ruta_activa = ruta_activa or []
        nodos_visitados = nodos_visitados or []

        # 1. Dibujar Aristas
        for u, vecinos in GRAFO_UCS.items():
            x1, y1 = POSICIONES[u]
            for v, peso in vecinos:
                x2, y2 = POSICIONES[v]

                # Verificar si pertenece a la ruta activa
                es_activa = False
                if len(ruta_activa) > 1:
                    for i in range(len(ruta_activa) - 1):
                        if ruta_activa[i] == u and ruta_activa[i + 1] == v:
                            es_activa = True
                            break

                color = self.c_active_edge if es_activa else self.c_edge
                ancho = 3.2 if es_activa else 1.6

                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)

                # Costo de la arista c=...
                # Desplazamos un poco para no tapar la línea
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2
                dx = -12 if x2 < x1 else 12

                # Etiqueta de peso pequeña y limpia
                self.canvas.create_text(
                    mx + dx, my,
                    text=f"c={peso}",
                    font=("SF Pro Text", 8),
                    fill=self.c_muted
                )

        # 2. Dibujar Nodos
        r = 18
        for nodo, (x, y) in POSICIONES.items():
            en_ruta = nodo in ruta_activa
            fue_visitado = nodo in nodos_visitados

            if en_ruta:
                fill_color = "#0F172A"       # Negro neutro
                border_color = "#0F172A"
                text_color = "#FFFFFF"
            elif fue_visitado:
                fill_color = "#E2E8F0"       # Gris suave explorado
                border_color = "#94A3B8"
                text_color = "#0F172A"
            else:
                fill_color = "#FFFFFF"       # Blanco normal
                border_color = "#CBD5E1"
                text_color = "#0F172A"

            # Círculo del nodo
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=fill_color,
                outline=border_color,
                width=2
            )

            # Letra del nodo centrada
            self.canvas.create_text(
                x, y,
                text=nodo,
                font=("SF Pro Text", 10, "bold"),
                fill=text_color
            )

            # Heurística h=... debajo con espacio suficiente para no encimarse
            h_val = HEURISTICAS.get(nodo, "-")
            meta_txt = " (META)" if nodo == META else ""
            self.canvas.create_text(
                x, y + r + 11,
                text=f"h={h_val}{meta_txt}",
                font=("SF Pro Text", 8),
                fill=self.c_muted
            )

    # ==========================================================================
    # 6. ACCIONES
    # ==========================================================================

    def simular_heuristica(self):
        res = ejecutar_heuristica()
        self.dibujar_grafo(ruta_activa=res['ruta'], nodos_visitados=res['visitados'])
        self.lbl_badge.config(text="Búsqueda Heurística", fg="#0F172A", bg="#E2E8F0")

        self.lbl_h_ruta.config(text=f"Ruta: {' → '.join(res['ruta'])}")
        self.lbl_h_costo.config(text=f"Costo h: {res['costo']}  |  Visitados: {len(res['visitados'])}")

        self.lbl_concl.config(
            text="La Búsqueda Heurística elige el nodo más prometedor según h(n) en cada paso. Va directo a J explorando solo 4 nodos."
        )

    def simular_ucs(self):
        res = ejecutar_ucs()
        self.dibujar_grafo(ruta_activa=res['ruta'], nodos_visitados=res['visitados'])
        self.lbl_badge.config(text="Costo Uniforme (UCS)", fg="#0F172A", bg="#E2E8F0")

        self.lbl_ucs_ruta.config(text=f"Ruta: {' → '.join(res['ruta'])}")
        self.lbl_ucs_costo.config(text=f"Costo g: {res['costo']}  |  Visitados: {len(res['visitados'])}")

        self.lbl_concl.config(
            text="UCS usa heapq para explorar siempre el camino con menor costo acumulado g(n). Explora más nodos para garantizar el óptimo real."
        )

    def comparar_ambos(self):
        res_h = ejecutar_heuristica()
        res_ucs = ejecutar_ucs()

        self.dibujar_grafo(ruta_activa=res_h['ruta'], nodos_visitados=res_ucs['visitados'])
        self.lbl_badge.config(text="Comparación completa", fg="#0F172A", bg="#E2E8F0")

        self.lbl_h_ruta.config(text=f"Ruta: {' → '.join(res_h['ruta'])}")
        self.lbl_h_costo.config(text=f"Costo h: {res_h['costo']}  |  Visitados: {len(res_h['visitados'])}")

        self.lbl_ucs_ruta.config(text=f"Ruta: {' → '.join(res_ucs['ruta'])}")
        self.lbl_ucs_costo.config(text=f"Costo g: {res_ucs['costo']}  |  Visitados: {len(res_ucs['visitados'])}")

        dif = len(res_ucs['visitados']) - len(res_h['visitados'])
        self.lbl_concl.config(
            text=f"Ambos coinciden en la ruta A → C → F → J. "
                 f"La Heurística necesitó solo {len(res_h['visitados'])} nodos. "
                 f"UCS exploró {dif} nodos adicionales ({len(res_ucs['visitados'])} en total) para verificar ramas de menor costo."
        )

    def reset(self):
        self.dibujar_grafo()
        self.lbl_badge.config(text="Listo para simular", fg=self.c_muted, bg=self.c_pill)
        self.lbl_h_ruta.config(text="Ruta: -")
        self.lbl_h_costo.config(text="Costo h: -  |  Visitados: -")
        self.lbl_ucs_ruta.config(text="Ruta: -")
        self.lbl_ucs_costo.config(text="Costo g: -  |  Visitados: -")
        self.lbl_concl.config(
            text="Presiona cualquier botón para simular y ver la comparación de rendimiento en el árbol."
        )


if __name__ == "__main__":
    app = ComparadorApp()
    app.mainloop()
