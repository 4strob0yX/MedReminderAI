"""
PRÁCTICA 1 (PARTE A) - MEDREMINDER AI:
BÚSQUEDA DE RUTAS CLÍNICAS MEDIANTE BFS vs. APRENDIZAJE AUTOMÁTICO
"""

from collections import deque

flujo_clinico_medreminder = {
    "Toma_Programada": ["Recordatorio_Notificado", "Botiquin_Bajo"],
    "Recordatorio_Notificado": ["Toma_Confirmada", "Toma_Pospuesta"],
    "Toma_Pospuesta": ["Segundo_Recordatorio", "Toma_Omitida"],
    "Segundo_Recordatorio": ["Toma_Confirmada", "Toma_Omitida"],
    "Toma_Omitida": ["Alerta_Cuidador", "Modo_Castigo_Honor"],
    "Alerta_Cuidador": ["Llamada_Contacto_Apoyo"],
    "Botiquin_Bajo": ["Alerta_Reabastecimiento"],
    "Toma_Confirmada": [],
    "Modo_Castigo_Honor": [],
    "Llamada_Contacto_Apoyo": [],
    "Alerta_Reabastecimiento": [],
}


def buscar_ruta_clinica(grafo: dict[str, list[str]], inicio: str, objetivo: str) -> list[str] | None:
    """Encuentra el camino mínimo de escalamiento clínico con BFS."""
    if inicio not in grafo or objetivo not in grafo:
        return None
    cola = deque([[inicio]])
    visitados = {inicio}

    while cola:
        ruta = cola.popleft()
        actual = ruta[-1]
        if actual == objetivo:
            return ruta
        for vecino in grafo[actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(ruta + [vecino])
    return None


def main() -> None:
    print("=== BÚSQUEDA BFS EN FLUJO CLÍNICO MEDREMINDER AI ===")
    consultas = [
        ("Toma_Programada", "Llamada_Contacto_Apoyo"),
        ("Toma_Programada", "Alerta_Reabastecimiento"),
        ("Toma_Confirmada", "Alerta_Cuidador"),
    ]
    for inicio, fin in consultas:
        ruta = buscar_ruta_clinica(flujo_clinico_medreminder, inicio, fin)
        print(f"\nFlujo: {inicio} -> {fin}")
        if ruta:
            print("  Ruta mínima:", " -> ".join(ruta))
            print("  Transiciones:", len(ruta) - 1)
        else:
            print("  Sin transición posible en el grafo dirigido.")

    print("\n=== DIFERENCIA DE ENFOQUES EN MEDREMINDER AI ===")
    print("- BFS / Reglas deterministas (logic_engine.py): ideales para transiciones")
    print("  exactas (ej. límite k=2 posposiciones, alertas de stock, bloqueos por alergia).")
    print("- Machine Learning (ml_risk_service.py): necesario para predecir riesgo de abandono")
    print("  a partir de patrones históricos con múltiples variables clínicas correlacionadas.")


if __name__ == "__main__":
    main()
