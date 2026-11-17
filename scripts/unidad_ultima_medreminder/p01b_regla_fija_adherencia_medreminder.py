"""
PRÁCTICA 1 (PARTE B) - MEDREMINDER AI:
CLASIFICACIÓN DE RIESGO DE ABANDONO MEDIANTE REGLA FIJA vs. ML
"""

pacientes_demo = [
    {"nombre": "Don Ramiro (78 años, 5 fármacos, sin cuidador)", "edad": 78, "meds": 5, "adherencia": 74.0, "retraso": 40.0, "cuidador": 0},
    {"nombre": "Sra. Elena (68 años, 3 fármacos, con cuidador)", "edad": 68, "meds": 3, "adherencia": 91.0, "retraso": 10.0, "cuidador": 1},
    {"nombre": "Carlos (35 años, 1 fármaco)", "edad": 35, "meds": 1, "adherencia": 68.0, "retraso": 15.0, "cuidador": 0},
]


def predecir_abandono_regla_fija(adherencia_pct: float) -> str:
    """Regla manual simplificada: evalúa únicamente un umbral fijo de adherencia."""
    if adherencia_pct < 75.0:
        return "Riesgo de abandono (Requiere apoyo)"
    return "Adherencia estable"


def main() -> None:
    print("=== CLASIFICACIÓN POR REGLA FIJA (MEDREMINDER AI) ===")
    for p in pacientes_demo:
        diag = predecir_abandono_regla_fija(p["adherencia"])
        print(f"- {p['nombre']} | Adherencia={p['adherencia']}% -> {diag}")

    print("\n=== CASO NUEVO ===")
    print("Adherencia=74.5%, Edad=81, Polifarmacia=6 ->", predecir_abandono_regla_fija(74.5))
    print("\nLimitación clínica: una regla fija con umbral único ignora polifarmacia,")
    print("edad geriátrica, retrasos acumulados y presencia de cuidador.")


if __name__ == "__main__":
    main()
