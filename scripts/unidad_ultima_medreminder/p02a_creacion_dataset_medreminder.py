"""
PRÁCTICA 2 - PARTE A (MEDREMINDER AI): CREACIÓN DEL DATASET CLÍNICO DE PACIENTES
Incluye la Actividad rápida: agregar nuevos pacientes y comprobar el cambio de dimensiones.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p02"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

datos_iniciales = {
    "id_paciente": ["PAC-01", "PAC-02", "PAC-03", "PAC-04", "PAC-05", "PAC-06", "PAC-07", "PAC-08"],
    "edad": [72, 45, 81, 64, 29, 77, 53, 69],
    "medicamentos_activos": [5, 2, 6, 4, 1, 7, 3, 4],
    "adherencia_historica_pct": [68.5, 92.0, 54.0, 78.0, 96.5, 61.0, 84.0, 73.5],
    "retraso_promedio_min": [42.0, 8.0, 65.0, 22.0, 5.0, 55.0, 18.0, 36.0],
    "tiene_cuidador": [0, 1, 0, 1, 0, 1, 1, 0],
    "riesgo_abandono": [1, 0, 1, 0, 0, 1, 0, 1],
}

df_original = pd.DataFrame(datos_iniciales)
print("=== CONJUNTO CLÍNICO ORIGINAL ===")
print(df_original.to_string(index=False))
print(f"Dimensiones originales: {df_original.shape}")

# Actividad rápida: incorporar más pacientes y comprobar cambio de dimensiones
nuevos = pd.DataFrame({
    "id_paciente": ["PAC-09", "PAC-10", "PAC-11", "PAC-12"],
    "edad": [84, 38, 71, 60],
    "medicamentos_activos": [8, 2, 5, 3],
    "adherencia_historica_pct": [49.0, 94.0, 81.5, 69.0],
    "retraso_promedio_min": [78.0, 6.0, 20.0, 44.0],
    "tiene_cuidador": [0, 0, 1, 0],
    "riesgo_abandono": [1, 0, 0, 1],
})

df = pd.concat([df_original, nuevos], ignore_index=True)
print("\n=== CONJUNTO AMPLIADO (ACTIVIDAD RÁPIDA MEDREMINDER AI) ===")
print(f"Nuevas dimensiones: {df.shape} (+{len(nuevos)} pacientes)")

archivo = RESULTADOS_DIR / "pacientes_medreminder.csv"
df.to_csv(archivo, index=False, encoding="utf-8")
print(f"Archivo guardado en: {archivo}")
