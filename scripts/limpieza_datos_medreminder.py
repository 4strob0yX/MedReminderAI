# ============================================================
# FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL - UTVT
# ADAPTACIÓN A PROYECTO FINAL: MedReminder AI
# PRÁCTICA 2: DETECCIÓN DE ERRORES, AUDITORÍA Y LIMPIEZA DE DATOS CLÍNICOS
# ============================================================

"""
OBJETIVO:
Implementar el ciclo completo de aseguramiento de calidad de datos para
el sistema MedReminder AI. 

A diferencia del ejemplo didáctico escolar (estudiantes y calificaciones),
aquí evaluamos pacientes, posología, rangos biológicos y métricas de 
adherencia médica.

FASES IMPLEMENTADAS:
1. Simulación de ingesta de datos con inconsistencias comunes en apps médicas.
2. Diagnóstico de calidad (valores faltantes, duplicados, datos fuera de rango).
3. Aplicación de reglas de validación clínica.
4. Separación y exportación de:
   - Datos limpios: listos para entrenar el modelo de Machine Learning.
   - Datos de auditoría: aislados con el motivo de falla para revisión clínica.
"""

import os
import pandas as pd

# ------------------------------------------------------------
# 1. GENERACIÓN DEL CONJUNTO DE DATOS CLÍNICOS CRUDOS
# ------------------------------------------------------------
# Simulación de telemetría recibida de la app móvil y dispositivos médicos.
# Se incluyen deliberadamente anomalías para probar el pipeline de limpieza.

datos_clinicos_crudos = {
    "id_paciente": [
        "PAC-001", "PAC-002", "PAC-003", "PAC-004", "PAC-002",
        "PAC-005", "PAC-006", "PAC-007", "PAC-008", "PAC-009"
    ],
    "nombre": [
        "Don Ramiro", "Doña Carmen", "Lucía Santos", "Roberto Mora", "Doña Carmen",
        "Don Manuel", "Elena Vega", "Jorge Méndez", "Beatriz Soto", "Carlos Vera"
    ],
    "edad": [
        74, 68, 25, 59, 68,
        155, 31, 82, -4, 47         # 155 (outlier biológico), -4 (edad negativa inválida)
    ],
    "medicamentos_activos": [
        5, 3, 1, 4, 3,
        6, None, 5, 2, 0            # Elena tiene valor nulo; Carlos tiene 0 (inconsistente si está en app)
    ],
    "adherencia_historica_pct": [
        62.5, 96.0, 89.0, 45.0, 96.0,
        38.0, 72.0, 130.0, 85.0, 91.0 # 130.0% (error de cálculo porcentual)
    ],
    "retraso_promedio_min": [
        45.0, 5.0, 12.0, 90.0, 5.0,
        60.0, 20.0, 15.0, -18.0, 8.0  # -18.0 min (retraso negativo ilógico)
    ],
    "tiene_cuidador": [
        1, 1, 0, 0, 1,
        1, 0, 1, 1, 0
    ],
    "riesgo_abandono": [
        1, 0, 0, 1, 0,
        1, 0, 1, 0, 0
    ]
}

df_crudo = pd.DataFrame(datos_clinicos_crudos)

print("=" * 70)
print(" 1. DATASET CLÍNICO CRUDO RECIBIDO (MedReminder AI)")
print("=" * 70)
print(df_crudo.to_string(index=False))


# ------------------------------------------------------------
# 2. DIAGNÓSTICO DE CALIDAD DE DATOS
# ------------------------------------------------------------
print("\n" + "=" * 70)
print(" 2. DIAGNÓSTICO Y DETECCIÓN DE ANOMALÍAS")
print("=" * 70)

# A. Búsqueda de valores faltantes (NaN)
faltantes_por_col = df_crudo.isnull().sum()
total_filas_incompletas = df_crudo.isnull().any(axis=1).sum()
print("\n[A] Valores faltantes por columna:")
print(faltantes_por_col[faltantes_por_col > 0])
print(f"Total de registros incompletos: {total_filas_incompletas}")

# B. Detección de duplicados exactos
duplicados = df_crudo[df_crudo.duplicated(keep=False)]
print("\n[B] Registros duplicados detectados:")
if not duplicados.empty:
    print(duplicados[["id_paciente", "nombre", "edad", "adherencia_historica_pct"]].to_string(index=False))
else:
    print("No se encontraron filas idénticas.")

# C. Detección de rangos biológicos y matemáticos inválidos
edad_invalida = (df_crudo["edad"] < 0) | (df_crudo["edad"] > 115)
adherencia_invalida = (df_crudo["adherencia_historica_pct"] < 0) | (df_crudo["adherencia_historica_pct"] > 100)
retraso_invalido = df_crudo["retraso_promedio_min"] < 0
meds_invalidos = (df_crudo["medicamentos_activos"] < 1)

print("\n[C] Inconsistencias de rango detectadas:")
print(f"- Edades biológicamente incoherentes (<0 o >115): {edad_invalida.sum()} paciente(s)")
print(f"- Porcentaje de adherencia fuera de [0, 100]%: {adherencia_invalida.sum()} paciente(s)")
print(f"- Minutos de retraso negativos (< 0): {retraso_invalido.sum()} paciente(s)")
print(f"- Medicamentos prescritos inválidos (< 1): {meds_invalidos.sum()} paciente(s)")


# ------------------------------------------------------------
# 3. PROCESO DE LIMPIEZA Y VALIDACIÓN CLÍNICA
# ------------------------------------------------------------
print("\n" + "=" * 70)
print(" 3. EJECUCIÓN DE REGLAS DE LIMPIEZA")
print("=" * 70)

# Paso 1: Eliminar filas completamente duplicadas (reintentos de red de la app)
df_dedup = df_crudo.drop_duplicates().copy()

# Paso 2: Crear vector de reglas de integridad clínica
columnas_obligatorias = [
    "id_paciente", "edad", "medicamentos_activos", 
    "adherencia_historica_pct", "retraso_promedio_min"
]

valido_completitud = df_dedup[columnas_obligatorias].notna().all(axis=1)
valido_edad = df_dedup["edad"].between(0, 115)
valido_adherencia = df_dedup["adherencia_historica_pct"].between(0.0, 100.0)
valido_retraso = df_dedup["retraso_promedio_min"] >= 0.0
valido_meds = df_dedup["medicamentos_activos"] >= 1

# Condición compuesta de validez
registro_valido = (
    valido_completitud
    & valido_edad
    & valido_adherencia
    & valido_retraso
    & valido_meds
)

# Paso 3: Separación estricta de registros
df_limpios = df_dedup.loc[registro_valido].copy()
df_revision = df_dedup.loc[~registro_valido].copy()

# Documentar en el dataset de auditoría la razón del descarte
def identificar_motivo_falla(fila):
    motivos = []
    if fila[columnas_obligatorias].isnull().any():
        motivos.append("Campos requeridos faltantes")
    if not (0 <= fila["edad"] <= 115):
        motivos.append(f"Edad fuera de rango ({fila['edad']})")
    if not (0.0 <= fila["adherencia_historica_pct"] <= 100.0):
        motivos.append(f"Adherencia fuera de rango ({fila['adherencia_historica_pct']}%)")
    if fila["retraso_promedio_min"] < 0:
        motivos.append(f"Retraso promedio negativo ({fila['retraso_promedio_min']} min)")
    if fila["medicamentos_activos"] < 1:
        motivos.append(f"Medicamentos prescritos inválidos ({fila['medicamentos_activos']})")
    return " | ".join(motivos)

if not df_revision.empty:
    df_revision["motivo_auditoria"] = df_revision.apply(identificar_motivo_falla, axis=1)

print(f"\nTotal registros analizados:  {len(df_dedup)}")
print(f"Registros validados (aptos):  {len(df_limpios)}  (Serán usados por la IA)")
print(f"Registros rechazados:         {len(df_revision)}  (Enviados a revisión de soporte)")


# ------------------------------------------------------------
# 4. EXPORTACIÓN DE RESULTADOS
# ------------------------------------------------------------
output_dir = os.path.dirname(os.path.abspath(__file__))
path_limpios = os.path.join(output_dir, "pacientes_adherencia_limpio.csv")
path_revision = os.path.join(output_dir, "pacientes_auditoria_errores.csv")

df_limpios.to_csv(path_limpios, index=False, encoding="utf-8")
df_revision.to_csv(path_revision, index=False, encoding="utf-8")

print("\n" + "=" * 70)
print(" 4. ARCHIVOS GENERADOS")
print("=" * 70)
print(f"[OK] Dataset limpio guardado en:     {path_limpios}")
print(f"[OK] Bitácora de errores guardada en: {path_revision}")

print("\n=== MUESTRA DE REGISTROS LIMPIOS (LISTOS PARA ENTRENAMIENTO) ===")
print(df_limpios[["id_paciente", "nombre", "edad", "medicamentos_activos", "adherencia_historica_pct", "riesgo_abandono"]].to_string(index=False))

print("\n=== REGISTROS AUDITADOS CON MOTIVO DE EXCLUSIÓN ===")
print(df_revision[["id_paciente", "nombre", "motivo_auditoria"]].to_string(index=False))
print("\n" + "=" * 70)
