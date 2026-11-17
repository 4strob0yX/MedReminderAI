"""
PRÁCTICA 2 - PARTE C (MEDREMINDER AI): DETECCIÓN DE ERRORES EN TELEMETRÍA CLÍNICA
"""

import pandas as pd

datos_con_errores = {
    "id_paciente": ["PAC-01", "PAC-02", "PAC-03", "PAC-02", "PAC-04", "PAC-05"],
    "edad": [72, 45, 165, 45, None, "setenta"],
    "adherencia_historica_pct": [68.5, 92.0, 135.0, 92.0, 74.0, 81.0],
    "retraso_promedio_min": [42.0, 8.0, 15.0, 8.0, -25.0, None],
}

df = pd.DataFrame(datos_con_errores)
print("=== TELEMETRÍA CRUDA CON ERRORES ===")
print(df)

print("\n=== 1. VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())

print("\n=== 2. FILAS DUPLICADAS ===")
print(df[df.duplicated()])

edad_num = pd.to_numeric(df["edad"], errors="coerce")
print("\n=== 3. EDADES NO NUMÉRICAS O FUERA DE RANGO [0, 120] ===")
print(df[edad_num.isna() | (edad_num < 0) | (edad_num > 120)])

print("\n=== 4. ADHERENCIA FUERA DE [0, 100] ===")
print(df[(df["adherencia_historica_pct"] < 0) | (df["adherencia_historica_pct"] > 100)])

print("\n=== 5. RETRASOS NEGATIVOS O NULOS ===")
print(df[df["retraso_promedio_min"].isna() | (df["retraso_promedio_min"] < 0)])
