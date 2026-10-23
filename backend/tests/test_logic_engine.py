"""
backend/tests/test_logic_engine.py - Suite de verificación de tablas de verdad formales.
Audita cada fila de las seis tablas deductivas de la Sección 2.2 del Manual Técnico.
"""

import sys
from pathlib import Path

# Asegurar importación de backend/app
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.core.logic_engine import (
    validar_alta_farmaco,
    verificar_inventario_critico,
    validar_exclusion_mutua_tomas_de_medicamentos,
    permitir_posponer_tomas_de_medicamentos,
    evaluar_bloqueo_seguridad_alergias,
    evaluar_modo_castigo
)

def test_tabla_2_2_crud_farmacos():
    """Tabla 2.2: Validación Lógica de Fármacos (p ∧ q ∧ r ∧ s)."""
    # Fila 1: V V V V -> V
    assert validar_alta_farmaco("Paracetamol", 500.0, 8, 20) is True
    # Fila 2: V V V F -> F (stock negativo)
    assert validar_alta_farmaco("Paracetamol", 500.0, 8, -1) is False
    # Fila 3: V V F V -> F (frecuencia no admisible)
    assert validar_alta_farmaco("Paracetamol", 500.0, 7, 20) is False
    # Fila 4: V F V V -> F (dosis nula o negativa)
    assert validar_alta_farmaco("Paracetamol", 0.0, 8, 20) is False
    # Fila 5: F V V V -> F (nombre vacío)
    assert validar_alta_farmaco(" ", 500.0, 8, 20) is False
    # Fila 6: F F F F -> F (múltiples fallas)
    assert validar_alta_farmaco("", -10.0, 3, -5) is False

def test_tabla_2_3_inventario_critico():
    """Tabla 2.3: Inventario Crítico de Medicamentos (A ∧ B)."""
    # Fila 1: V V -> V
    assert verificar_inventario_critico(stock_actual=3, stock_minimo=5, tratamiento_activo=True) is True
    # Fila 2: V F -> F
    assert verificar_inventario_critico(stock_actual=3, stock_minimo=5, tratamiento_activo=False) is False
    # Fila 3: F V -> F
    assert verificar_inventario_critico(stock_actual=10, stock_minimo=5, tratamiento_activo=True) is False
    # Fila 4: F F -> F
    assert verificar_inventario_critico(stock_actual=10, stock_minimo=5, tratamiento_activo=False) is False

def test_tabla_2_4_exclusion_mutua_tomas_de_medicamentos():
    """Tabla 2.4: Exclusión Mutua en Estados de Tomas de Medicamentos."""
    # Fila 1: V F F -> V (Tomado)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=True, pospuesto=False, omitido=False) is True
    # Fila 2: F V F -> V (Pospuesto)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=False, pospuesto=True, omitido=False) is True
    # Fila 3: F F V -> V (Omitido)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=False, pospuesto=False, omitido=True) is True
    # Fila 4: V V F -> F (Conflicto tomado y pospuesto)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=True, pospuesto=True, omitido=False) is False
    # Fila 5: V F V -> F (Conflicto tomado y omitido)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=True, pospuesto=False, omitido=True) is False
    # Fila 6: F V V -> F (Conflicto pospuesto y omitido)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=False, pospuesto=True, omitido=True) is False
    # Fila 7: V V V -> F (Contradicción total)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=True, pospuesto=True, omitido=True) is False
    # Fila 8: F F F -> F (Sin resolver)
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=False, pospuesto=False, omitido=False) is False

def test_tabla_2_5_limite_posposiciones_k2():
    """Tabla 2.5: Límite Determinista de Posposiciones (k=2)."""
    # Fila 1: V V -> V
    assert permitir_posponer_tomas_de_medicamentos(solicita_posponer=True, contador_posposiciones=1) is True
    # Fila 2: V F -> F (Límite k=2 alcanzado)
    assert permitir_posponer_tomas_de_medicamentos(solicita_posponer=True, contador_posposiciones=2) is False
    # Fila 3: F V -> F
    assert permitir_posponer_tomas_de_medicamentos(solicita_posponer=False, contador_posposiciones=0) is False
    # Fila 4: F F -> F
    assert permitir_posponer_tomas_de_medicamentos(solicita_posponer=False, contador_posposiciones=3) is False

def test_tabla_2_6_alergias_contraindicaciones():
    """Tabla 2.6: Matriz Lógica de Bloqueo por Alergias e Interacciones (X ∨ Y)."""
    # Fila 1: V V -> V
    assert evaluar_bloqueo_seguridad_alergias(alergia_detectada=True, interaccion_grave=True) is True
    # Fila 2: V F -> V
    assert evaluar_bloqueo_seguridad_alergias(alergia_detectada=True, interaccion_grave=False) is True
    # Fila 3: F V -> V
    assert evaluar_bloqueo_seguridad_alergias(alergia_detectada=False, interaccion_grave=True) is True
    # Fila 4: F F -> F
    assert evaluar_bloqueo_seguridad_alergias(alergia_detectada=False, interaccion_grave=False) is False

def test_tabla_2_7_modo_castigo():
    """Tabla 2.7: Activación del Modo Castigo y Pérdida de Honor (M ∧ N)."""
    # Fila 1: V V -> V
    assert evaluar_modo_castigo(omisiones_acumuladas=2, escudos_disponibles=0) is True
    # Fila 2: V F -> F (Escudo disponible protege racha)
    assert evaluar_modo_castigo(omisiones_acumuladas=2, escudos_disponibles=1) is False
    # Fila 3: F V -> F (Menos de 2 omisiones)
    assert evaluar_modo_castigo(omisiones_acumuladas=1, escudos_disponibles=0) is False
    # Fila 4: F F -> F
    assert evaluar_modo_castigo(omisiones_acumuladas=0, escudos_disponibles=2) is False

if __name__ == "__main__":
    test_tabla_2_2_crud_farmacos()
    test_tabla_2_3_inventario_critico()
    test_tabla_2_4_exclusion_mutua_tomas_de_medicamentos()
    test_tabla_2_5_limite_posposiciones_k2()
    test_tabla_2_6_alergias_contraindicaciones()
    test_tabla_2_7_modo_castigo()
    print("✅ Todas las pruebas de las tablas de verdad 2.2 a 2.7 pasaron con 100% de éxito.")
