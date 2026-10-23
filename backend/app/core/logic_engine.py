"""
backend/app/core/logic_engine.py - Motor formal de evaluación proposicional.
Implementa las seis reglas axiomáticas del agente MedReminder AI evaluadas con valores de verdad canónicos:
1. Validación de alta y CRUD de fármacos (p ∧ q ∧ r ∧ s).
2. Disparo de alerta de inventario crítico (A ∧ B).
3. Transición de estados y exclusión mutua en tomas de medicamentos (t ⊕ p ⊕ o).
4. Límite determinista de posposiciones de tomas de medicamentos (k=2).
5. Matriz lógica de alergias y contraindicaciones críticas (X ∨ Y).
6. Regla formal del Modo Castigo y pérdida de honor (M ∧ N).
"""

def validar_alta_farmaco(nombre: str, dosis: float, frecuencia: int, stock: int) -> bool:
    """Regla 1: Validación lógica de entrada (CRUD de Medicamentos).
    Fórmula: V_alta = p ∧ q ∧ r ∧ s
    Leyes de De Morgan: ¬V_alta = ¬p ∨ ¬q ∨ ¬r ∨ ¬s
    """
    p = len(nombre.strip()) >= 2
    q = dosis > 0.0
    r = frecuencia in [4, 6, 8, 12, 24]
    s = stock >= 0
    return p and q and r and s


def verificar_inventario_critico(stock_actual: int, stock_minimo: int, tratamiento_activo: bool) -> bool:
    """Regla 2: Disparo de alerta de inventario crítico.
    Fórmula: Alerta_Stock = A ∧ B
    """
    a = stock_actual <= stock_minimo
    b = tratamiento_activo
    return a and b


def validar_exclusion_mutua_tomas_de_medicamentos(tomado: bool, pospuesto: bool, omitido: bool) -> bool:
    """Regla 3: Transición de estados y exclusión mutua en tomas de medicamentos.
    Fórmula: Validez_Estado = (t ⊕ p ⊕ o) ∧ ¬(t ∧ p) ∧ ¬(t ∧ o) ∧ ¬(p ∧ o)
    """
    valores = [bool(tomado), bool(pospuesto), bool(omitido)]
    return valores.count(True) == 1


def permitir_posponer_tomas_de_medicamentos(solicita_posponer: bool, contador_posposiciones: int) -> bool:
    """Regla 4: Regla formal de límite de posposiciones de tomas de medicamentos (k=2).
    Fórmula: Permitir_Posponer = C ∧ D (contador_posposiciones < 2)
    """
    c = bool(solicita_posponer)
    d = contador_posposiciones < 2
    return c and d


def evaluar_bloqueo_seguridad_alergias(alergia_detectada: bool, interaccion_grave: bool) -> bool:
    """Regla 5: Matriz lógica de alergias y contraindicaciones críticas.
    Fórmula: Bloqueo_Seguridad = X ∨ Y
    """
    x = bool(alergia_detectada)
    y = bool(interaccion_grave)
    return x or y


def evaluar_modo_castigo(omisiones_acumuladas: int, escudos_disponibles: int) -> bool:
    """Regla 6: Regla formal del Modo Castigo y pérdida de honor.
    Fórmula: Modo_Castigo = M ∧ N (omisiones_acumuladas >= 2 ∧ escudos_disponibles == 0)
    """
    m = omisiones_acumuladas >= 2
    n = escudos_disponibles == 0
    return m and n
