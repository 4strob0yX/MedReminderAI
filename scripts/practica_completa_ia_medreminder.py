# ==============================================================================
# UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA (UTVT)
# DIRECCIÓN DE CARRERAS DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN
# MATERIA: FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL
# PROYECTO FINAL: MedReminder AI
#
# PRÁCTICA INTEGRAL (04/11/2026):
# DE REGLAS FIJAS A MACHINE LEARNING - CICLO COMPLETO DE CIENCIA DE DATOS
# Y CLASIFICACIÓN DEL RIESGO DE ABANDONO DE TRATAMIENTOS MÉDICOS
# ==============================================================================

"""
DESCRIPCIÓN GENERAL:
Este programa unifica y adapta el 100% de los temas abordados en las prácticas
del 4 de noviembre, transformando el ejemplo escolar didáctico (estudiantes y 
calificaciones) en el módulo inteligente central de MedReminder AI:

MÓDULOS INCLUIDOS:
  1. ENFOQUE TRADICIONAL: Decisión mediante Reglas Fijas (heurística manual).
  2. INGESTA Y EXPLORACIÓN: Generación del DataFrame con métricas de salud y posología.
  3. CONTROL DE CALIDAD Y AUDITORÍA: Detección de duplicados, nulos y outliers biológicos.
  4. PIPELINE DE LIMPIEZA: Separación estricta en datos aptos y bitácora de auditoría.
  5. FORMULACIÓN DEL MODELO: Matriz de características (X) y Vector objetivo (y).
  6. APRENDIZAJE AUTOMÁTICO: División Train/Test y ajuste de DecisionTreeClassifier.
  7. EVALUACIÓN Y COMPARATIVA: Exactitud, Matriz de Confusión y Reporte de Clasificación.
  8. SIMULACIÓN DE INFERENCIA EN PRODUCCIÓN: Integración con el Módulo de Cuidadores.
  9. PERSISTENCIA: Serialización del modelo entrenado en disco (.joblib).
"""

import os
import random
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Fijar semillas para reproducibilidad científica
np.random.seed(42)
random.seed(42)

# ==============================================================================
# FASE 1: ENFOQUE TRADICIONAL - TOMA DE DECISIONES MEDIANTE REGLAS FIJAS
# ==============================================================================
print("=" * 78)
print(" FASE 1: SISTEMA BASADO EN REGLAS MANUALES (CÓDIGO TRADICIONAL)")
print("=" * 78)

def predecir_riesgo_por_regla_manual(edad, medicamentos_activos, adherencia_pct, retraso_min, tiene_cuidador):
    """
    Regla estática definida manualmente por un programador:
    Si la adherencia es menor al 70% o se retrasa más de 45 minutos sin cuidador,
    lo clasifica en 'Alto Riesgo'.
    """
    if adherencia_pct < 70.0:
        return 1  # 1 = Riesgo de Abandono
    if retraso_min >= 45.0 and tiene_cuidador == 0:
        return 1
    return 0      # 0 = Cumplidor / Adherente

pacientes_ejemplo = [
    {"nombre": "Don Ramiro (Geriátrico)", "edad": 78, "meds": 5, "adh": 72.0, "retraso": 40.0, "cuidador": 0},
    {"nombre": "Lucía (Joven)",           "edad": 22, "meds": 1, "adh": 68.0, "retraso": 10.0, "cuidador": 0},
]

print("Evaluación preliminar con regla fija:")
for p in pacientes_ejemplo:
    pred = predecir_riesgo_por_regla_manual(p["edad"], p["meds"], p["adh"], p["retraso"], p["cuidador"])
    estado = "🔴 Alto Riesgo de Abandono" if pred == 1 else "🟢 Tratamiento Estable"
    print(f" - {p['nombre']}: Adherencia={p['adh']}%, Retraso={p['retraso']}m -> Diagnóstico: {estado}")

print("\n[LIMITACIÓN CLÍNICA IDENTIFICADA]:")
print("Don Ramiro tiene 78 años, toma 5 medicinas simultáneas y no tiene cuidador.")
print("La regla fija dice que está 'Estable' solo porque su adherencia es 72% (>70%).")
print("Un modelo de Machine Learning es necesario para detectar la correlación multivariable.")


# ==============================================================================
# FASE 2: INGESTA, EXPLORACIÓN Y DETECCIÓN DE PROBLEMAS DE CALIDAD (PANDAS)
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 2: CONSTRUCCIÓN DEL DATASET CLÍNICO Y DETECCIÓN DE ANOMALÍAS")
print("=" * 78)

# Generación controlada de 80 pacientes para entrenamiento y pruebas
n_pacientes = 80
edades = np.random.randint(18, 90, size=n_pacientes)
meds = np.random.randint(1, 8, size=n_pacientes)
adherencia = np.random.uniform(40.0, 99.0, size=n_pacientes)
retrasos = np.random.uniform(2.0, 95.0, size=n_pacientes)
cuidador = np.random.choice([0, 1], size=n_pacientes, p=[0.45, 0.55])

# Definición del riesgo real basado en interacciones clínicas complejas
riesgo_real = []
for i in range(n_pacientes):
    puntos_riesgo = 0
    if edades[i] >= 65: puntos_riesgo += 2
    if meds[i] >= 4:    puntos_riesgo += 2
    if adherencia[i] < 75.0: puntos_riesgo += 3
    if retrasos[i] > 35.0:   puntos_riesgo += 2
    if cuidador[i] == 1:     puntos_riesgo -= 2
    riesgo_real.append(1 if puntos_riesgo >= 4 else 0)

df_clinico = pd.DataFrame({
    "id_paciente": [f"PAC-{i+1001}" for i in range(n_pacientes)],
    "edad": edades,
    "medicamentos_activos": meds,
    "adherencia_historica_pct": np.round(adherencia, 1),
    "retraso_promedio_min": np.round(retrasos, 1),
    "tiene_cuidador": cuidador,
    "riesgo_abandono": riesgo_real
})

# Inyección deliberada de errores comunes en recolección de telemetría médica
df_clinico.loc[2, "edad"] = 165                 # Error: edad fuera de rango biológico
df_clinico.loc[7, "adherencia_historica_pct"] = 135.0  # Error: porcentaje > 100%
df_clinico.loc[12, "retraso_promedio_min"] = -25.0    # Error: tiempo negativo
df_clinico.loc[18, "medicamentos_activos"] = np.nan   # Error: dato nulo
# Inyección de fila duplicada
fila_duplicada = df_clinico.iloc[[0]].copy()
df_clinico = pd.concat([df_clinico, fila_duplicada], ignore_index=True)

print(f"Dimensiones del dataset crudo: {df_clinico.shape[0]} filas, {df_clinico.shape[1]} columnas")
print("\nPrimeros registros con anomalías:")
print(df_clinico.head(6).to_string(index=False))

# Diagnóstico de Calidad
print("\n[AUDITORÍA DE INTEGRIDAD]:")
print(f"• Valores nulos detectados: {df_clinico.isnull().sum().sum()}")
print(f"• Filas duplicadas encontradas: {df_clinico.duplicated().sum()}")
outliers_edad = ((df_clinico["edad"] < 0) | (df_clinico["edad"] > 115)).sum()
outliers_adh = ((df_clinico["adherencia_historica_pct"] < 0) | (df_clinico["adherencia_historica_pct"] > 100)).sum()
outliers_ret = (df_clinico["retraso_promedio_min"] < 0).sum()
print(f"• Inconsistencias clínicas: {outliers_edad} edad inválida, {outliers_adh} adherencia inválida, {outliers_ret} retraso negativo")


# ==============================================================================
# FASE 3: PIPELINE DE LIMPIEZA Y AUDITORÍA MÉDICA
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 3: PIPELINE DE LIMPIEZA Y GENERACIÓN DE BITÁCORA")
print("=" * 78)

# 1. Eliminación de duplicados
df_sin_duplicados = df_clinico.drop_duplicates().copy()

# 2. Vector booleano de validez clínica
cols_req = ["edad", "medicamentos_activos", "adherencia_historica_pct", "retraso_promedio_min"]
valido_completitud = df_sin_duplicados[cols_req].notna().all(axis=1)
valido_edad = df_sin_duplicados["edad"].between(0, 115)
valido_adh = df_sin_duplicados["adherencia_historica_pct"].between(0.0, 100.0)
valido_ret = df_sin_duplicados["retraso_promedio_min"] >= 0.0
valido_meds = df_sin_duplicados["medicamentos_activos"] >= 1

condicion_valida = valido_completitud & valido_edad & valido_adh & valido_ret & valido_meds

# 3. Separación de DataFrames
df_limpio = df_sin_duplicados.loc[condicion_valida].copy()
df_auditoria = df_sin_duplicados.loc[~condicion_valida].copy()

# Explicación de rechazo para auditoría médica
def diagnosticar_rechazo(row):
    causas = []
    if row[cols_req].isnull().any(): causas.append("Dato nulo")
    if not (0 <= row["edad"] <= 115): causas.append(f"Edad fuera de rango ({row['edad']})")
    if not (0 <= row["adherencia_historica_pct"] <= 100): causas.append(f"Adherencia anormal ({row['adherencia_historica_pct']}%)")
    if row["retraso_promedio_min"] < 0: causas.append("Retraso negativo")
    if row["medicamentos_activos"] < 1: causas.append("Sin medicinas prescritas")
    return " | ".join(causas)

df_auditoria["motivo_rechazo"] = df_auditoria.apply(diagnosticar_rechazo, axis=1)

# Exportación a archivos CSV
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_limpio_path = os.path.join(base_dir, "pacientes_adherencia_limpio.csv")
csv_auditoria_path = os.path.join(base_dir, "pacientes_auditoria_errores.csv")
df_limpio.to_csv(csv_limpio_path, index=False, encoding="utf-8")
df_auditoria.to_csv(csv_auditoria_path, index=False, encoding="utf-8")

print(f"✓ Registros limpios listos para IA: {len(df_limpio)} -> {csv_limpio_path}")
print(f"✓ Registros aislados para revisión: {len(df_auditoria)} -> {csv_auditoria_path}")
print("\nDetalle de registros rechazados en auditoría:")
print(df_auditoria[["id_paciente", "motivo_rechazo"]].to_string(index=False))


# ==============================================================================
# FASE 4: DEFINICIÓN DE VARIABLES (X, y) Y DIVISIÓN TRAIN / TEST
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 4: PREPARACIÓN DE CARACTERÍSTICAS (X) Y OBJETIVO (y)")
print("=" * 78)

# Características predictoras (Features)
features = ["edad", "medicamentos_activos", "adherencia_historica_pct", "retraso_promedio_min", "tiene_cuidador"]
X = df_limpio[features]

# Variable dependiente objetivo (Target)
y = df_limpio["riesgo_abandono"].astype(int)

# División estratificada (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Variables de entrada (X): {features}")
print(f"Variable objetivo (y):    riesgo_abandono [0 = Estable, 1 = Riesgo]")
print(f"Conjunto de Entrenamiento: {len(X_train)} pacientes")
print(f"Conjunto de Evaluación:    {len(X_test)} pacientes")
print(f"Balance de clases (Entrenamiento): {np.bincount(y_train)} (0: Estable, 1: Riesgo)")


# ==============================================================================
# FASE 5: ENTRENAMIENTO DEL MODELO DE MACHINE LEARNING
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 5: ENTRENAMIENTO DEL ÁRBOL DE DECISIÓN (DecisionTreeClassifier)")
print("=" * 78)

# Entrenar árbol de decisión con profundidad acotada para evitar sobreajuste (overfitting)
modelo_arbol = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo_arbol.fit(X_train, y_train)

print("¡Modelo entrenado exitosamente con Scikit-Learn!")
print("\nEstructura de decisión aprendida por el modelo:")
print(export_text(modelo_arbol, feature_names=features))

print("Importancia relativa de las características según el árbol:")
for feat, imp in zip(features, modelo_arbol.feature_importances_):
    barra = "█" * int(imp * 30)
    print(f" • {feat:<25}: {imp:.3f} | {barra}")


# ==============================================================================
# FASE 6: EVALUACIÓN EXPERIMENTAL (REGLAS FIJAS VS MACHINE LEARNING)
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 6: COMPARATIVA DE RENDIMIENTO EN EL CONJUNTO DE PRUEBA")
print("=" * 78)

# 1. Predicciones con el modelo de Machine Learning
y_pred_ml = modelo_arbol.predict(X_test)

# 2. Predicciones con el sistema de reglas fijas manuales
y_pred_reglas = [
    predecir_riesgo_por_regla_manual(row["edad"], row["medicamentos_activos"], 
                                     row["adherencia_historica_pct"], 
                                     row["retraso_promedio_min"], row["tiene_cuidador"])
    for _, row in X_test.iterrows()
]

# 3. Métricas de exactitud
acc_ml = accuracy_score(y_test, y_pred_ml) * 100.0
acc_reglas = accuracy_score(y_test, y_pred_reglas) * 100.0

# Tabla comparativa paciente por paciente en el conjunto de prueba
df_comparativa = X_test.copy()
df_comparativa["Riesgo_Real"] = y_test.values
df_comparativa["Pred_Reglas"] = y_pred_reglas
df_comparativa["Pred_ML"] = y_pred_ml

print("Muestra de predicciones en el Conjunto de Prueba (Test Set):")
print(df_comparativa[["edad", "medicamentos_activos", "adherencia_historica_pct", "Riesgo_Real", "Pred_Reglas", "Pred_ML"]].head(8).to_string())

print("\n" + "-" * 78)
print(f"📊 EXACTITUD SISTEMA DE REGLAS MANUALES: {acc_reglas:.2f}%")
print(f"🤖 EXACTITUD MODELO DE MACHINE LEARNING: {acc_ml:.2f}%")
print("-" * 78)

print("\nMatriz de Confusión del Modelo de Machine Learning:")
print(confusion_matrix(y_test, y_pred_ml))

print("\nReporte Clínico de Clasificación:")
print(classification_report(y_test, y_pred_ml, target_names=["Tratamiento Estable", "Riesgo de Abandono"]))


# ==============================================================================
# FASE 7: SIMULACIÓN DE INFERENCIA EN PRODUCCIÓN (INTEGRACIÓN CON CUIDADORES)
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 7: INFERENCIA EN VIVO - CASOS CLÍNICOS REALES EN MedReminder AI")
print("=" * 78)

nuevos_pacientes = pd.DataFrame([
    {
        "caso": "Paciente Geriátrico Polimedicado",
        "edad": 76,
        "medicamentos_activos": 6,
        "adherencia_historica_pct": 74.5,
        "retraso_promedio_min": 42.0,
        "tiene_cuidador": 0
    },
    {
        "caso": "Paciente Joven con Tratamiento Simple",
        "edad": 24,
        "medicamentos_activos": 1,
        "adherencia_historica_pct": 92.0,
        "retraso_promedio_min": 8.0,
        "tiene_cuidador": 0
    }
])

X_nuevos = nuevos_pacientes[features]
predicciones_nuevas = modelo_arbol.predict(X_nuevos)
probabilidades = modelo_arbol.predict_proba(X_nuevos)

for i, row in nuevos_pacientes.iterrows():
    riesgo = predicciones_nuevas[i]
    prob_abandono = probabilidades[i][1] * 100.0
    print(f"\n[CASO {i+1}]: {row['caso']}")
    print(f"  Edad: {row['edad']} años | Fármacos: {row['medicamentos_activos']} | Adherencia: {row['adherencia_historica_pct']}% | Retraso: {row['retraso_promedio_min']}m")
    
    if riesgo == 1:
        print(f"  Diagnóstico IA: 🚨 ALTO RIESGO DE ABANDONO ({prob_abandono:.1f}% probabilidad)")
        print(f"  Acción Automatizada: Disparar registrar_alerta_cuidador_db(...) -> Notificación Push urgente.")
    else:
        print(f"  Diagnóstico IA: 🟢 TRATAMIENTO ESTABLE ({100 - prob_abandono:.1f}% probabilidad de adherencia)")
        print(f"  Acción Automatizada: Registrar log en MongoDB (medreminder_logs) -> Sin alerta.")


# ==============================================================================
# FASE 8: PERSISTENCIA DEL MODELO (EXPORTACIÓN JOBLIB)
# ==============================================================================
print("\n" + "=" * 78)
print(" FASE 8: GUARDADO Y SERIALIZACIÓN DEL MODELO PARA EL BACKEND FASTAPI")
print("=" * 78)

modelo_path = os.path.join(base_dir, "modelo_adherencia_medreminder.joblib")
joblib.dump(modelo_arbol, modelo_path)

print(f"✓ Modelo serializado con éxito en: {modelo_path}")
print("✓ El backend de FastAPI puede cargar este archivo instantáneamente con joblib.load(...)")
print("  para responder peticiones REST en menos de 5 milisegundos sin reentrenar.")

print("\n" + "=" * 78)
print(" CONCLUSIÓN DE LA PRÁCTICA: CICLO COMPLETO CONCLUIDO CON ÉXITO")
print("=" * 78)
