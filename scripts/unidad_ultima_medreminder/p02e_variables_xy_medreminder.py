"""
PRÁCTICA 2 - PARTE E (MEDREMINDER AI): VARIABLES DE ENTRADA (X) Y OBJETIVO (y)
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CSV = BASE_DIR / "resultados_p02" / "pacientes_medreminder.csv"

if not ARCHIVO_CSV.exists():
    raise FileNotFoundError(f"No se encontró {ARCHIVO_CSV}. Ejecuta primero p02a_creacion_dataset_medreminder.py")

df = pd.read_csv(ARCHIVO_CSV)
features = ["edad", "medicamentos_activos", "adherencia_historica_pct", "retraso_promedio_min", "tiene_cuidador"]
X = df[features]
y = df["riesgo_abandono"]

print("=== MATRIZ DE CARACTERÍSTICAS CLÍNICAS X ===")
print(X.head())
print("\n=== VECTOR OBJETIVO y (riesgo_abandono) ===")
print(y.head())
print(f"\nDimensiones X={X.shape} | y={y.shape}")
assert len(X) == len(y), "Desalineación entre X e y"
print("Alineación X/y verificada correctamente.")
