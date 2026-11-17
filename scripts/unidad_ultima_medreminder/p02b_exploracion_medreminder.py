"""
PRÁCTICA 2 - PARTE B (MEDREMINDER AI): EXPLORACIÓN DEL DATASET CLÍNICO
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CSV = BASE_DIR / "resultados_p02" / "pacientes_medreminder.csv"

if not ARCHIVO_CSV.exists():
    raise FileNotFoundError(f"No se encontró {ARCHIVO_CSV}. Ejecuta primero p02a_creacion_dataset_medreminder.py")

df = pd.read_csv(ARCHIVO_CSV)

print("=== PRIMEROS REGISTROS ===")
print(df.head())
print("\n=== ÚLTIMOS REGISTROS ===")
print(df.tail())
print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)
print("\n=== INFORMACIÓN GENERAL ===")
df.info()
print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
print(df.describe().round(2))
print("\n=== ADHERENCIA POR PACIENTE ===")
print(df[["id_paciente", "adherencia_historica_pct", "retraso_promedio_min"]].to_string(index=False))
print("\nPromedio adherencia:", round(df["adherencia_historica_pct"].mean(), 2), "%")
print("Correlación adherencia vs retraso:", round(df["adherencia_historica_pct"].corr(df["retraso_promedio_min"]), 3))
