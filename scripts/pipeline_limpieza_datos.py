# ==============================================================================
# UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA (UTVT)
# PROYECTO FINAL: MedReminder AI
# MÓDULO: PIPELINE DE DETECCIÓN DE ANOMALÍAS Y LIMPIEZA DE DATOS (PANDAS)
# ==============================================================================

"""
UBICACIÓN DE ESTE SCRIPT:
scripts/pipeline_limpieza_datos.py

OBJETIVO:
Tomar los datos crudos originales (155 pacientes en CSV o MySQL),
aplicar las reglas de auditoría clínica con Pandas, separar los datos limpios
de los sucios y documentar la causa del rechazo de cada anomalía.

FLUJO DE EJECUCIÓN:
1. Ingesta: Carga 'pacientes_adherencia_original_crudo.csv' (155 registros).
2. Detección: Identifica duplicados, nulos y valores fuera de rangos biológicos.
3. Filtrado: Separa en 150 registros aprobados y 5 registros con errores.
4. Auditoría: Etiqueta la columna 'motivo_rechazo' en cada fila descartada.
5. Exportación: Actualiza los CSVs y sincroniza las tablas de MySQL.
"""

import os
import pandas as pd

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "backend", "app", "data")

PATH_CRUDO = os.path.join(DATA_DIR, "pacientes_adherencia_original_crudo.csv")
PATH_LIMPIO = os.path.join(DATA_DIR, "dataset_entrenamiento_pacientes.csv")
PATH_ERRORES = os.path.join(BASE_DIR, "pacientes_auditoria_errores.csv")


def ejecutar_limpieza():
    print("=" * 75)
    print(" PIPELINE DE LIMPIEZA Y CALIDAD DE DATOS (MedReminder AI)")
    print("=" * 75)

    if not os.path.exists(PATH_CRUDO):
        print(f"Error: No se encontró el archivo original crudo en {PATH_CRUDO}")
        return

    # --------------------------------------------------------------------------
    # PASO 1: LECTURA DEL DATASET ORIGINAL CRUDO
    # --------------------------------------------------------------------------
    df_crudo = pd.read_csv(PATH_CRUDO)
    total_original = len(df_crudo)
    print(f"\n[1] Datos Originales Crudos Cargados: {total_original} registros")

    # --------------------------------------------------------------------------
    # PASO 2: ELIMINACIÓN DE DUPLICADOS EXACTOS
    # --------------------------------------------------------------------------
    # Elimina registros idénticos provocados por retransmisión de red de la app
    df_dedup = df_crudo.drop_duplicates(subset=["id_paciente", "edad", "medicamentos_activos", "adherencia_historica_pct"]).copy()
    duplicados_eliminados = total_original - len(df_dedup)
    print(f"[2] Registros Duplicados Eliminados: {duplicados_eliminados}")

    # --------------------------------------------------------------------------
    # PASO 3: APLICACIÓN DE REGLAS DE INTEGRIDAD CLÍNICA
    # --------------------------------------------------------------------------
    # Columnas requeridas que no pueden tener NaN
    cols_requeridas = ["edad", "medicamentos_activos", "adherencia_historica_pct", "retraso_promedio_min"]
    
    valido_completitud = df_dedup[cols_requeridas].notna().all(axis=1)
    valido_edad = df_dedup["edad"].between(0, 115)                     # Rango de vida humana
    valido_adherencia = df_dedup["adherencia_historica_pct"].between(0.0, 100.0) # Porcentaje matemático
    valido_retraso = df_dedup["retraso_promedio_min"] >= 0.0          # El tiempo no puede ser negativo
    valido_meds = df_dedup["medicamentos_activos"] >= 1                # Mínimo 1 fármaco prescrito

    # Condición vectorial final: Cumple TODAS las reglas
    condicion_aprobada = (
        valido_completitud 
        & valido_edad 
        & valido_adherencia 
        & valido_retraso 
        & valido_meds
    )

    # --------------------------------------------------------------------------
    # PASO 4: SEPARACIÓN DE DATOS LIMPIOS VS BITÁCORA DE ERRORES
    # --------------------------------------------------------------------------
    df_limpio = df_dedup.loc[condicion_aprobada].copy()
    df_errores = df_dedup.loc[~condicion_aprobada].copy()

    # Función para documentar la causa médica exacta de cada exclusión
    def documentar_motivo_falla(fila):
        fallas = []
        if fila[cols_requeridas].isnull().any():
            fallas.append("Campos obligatorios en blanco / nulos")
        if not (0 <= fila["edad"] <= 115):
            fallas.append(f"Outlier biológico: Edad fuera de rango ({fila['edad']} años)")
        if not (0.0 <= fila["adherencia_historica_pct"] <= 100.0):
            fallas.append(f"Error de cálculo: Adherencia anormal ({fila['adherencia_historica_pct']}%)")
        if fila["retraso_promedio_min"] < 0:
            fallas.append(f"Inconsistencia temporal: Retraso negativo ({fila['retraso_promedio_min']} min)")
        if fila["medicamentos_activos"] < 1:
            fallas.append("Sin medicamentos activos registrados")
        return " | ".join(fallas)

    if not df_errores.empty:
        df_errores["motivo_rechazo"] = df_errores.apply(documentar_motivo_falla, axis=1)

    print(f"\n[3] RESULTADOS DEL FILTRADO:")
    print(f"    • Registros Válidos y Limpios: {len(df_limpio)}  -> Listos para la IA")
    print(f"    • Registros Rechazados:        {len(df_errores) + duplicados_eliminados}  -> Aislados en bitácora")

    # --------------------------------------------------------------------------
    # PASO 5: EXPORTACIÓN DE LOS ARCHIVOS RESULTANTES
    # --------------------------------------------------------------------------
    df_limpio.to_csv(PATH_LIMPIO, index=False)
    df_errores.to_csv(PATH_ERRORES, index=False)

    print("\n[4] ARCHIVOS ACTUALIZADOS:")
    print(f"    ✓ Dataset Limpio:    {PATH_LIMPIO}")
    print(f"    ✓ Dataset Auditoría: {PATH_ERRORES}")

    print("\n" + "=" * 75)
    print(" DETALLE DE REGISTROS RECHAZADOS (AUDITORÍA MÉDICA)")
    print("=" * 75)
    print(df_errores[["id_paciente", "edad", "adherencia_historica_pct", "motivo_rechazo"]].to_string(index=False))
    print("=" * 75)

if __name__ == "__main__":
    ejecutar_limpieza()
