# ==============================================================================
# UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA (UTVT)
# PROYECTO FINAL: MedReminder AI
# PRÁCTICA 05: COMPARACIÓN DE ALGORITMOS DE MACHINE LEARNING SUPERVISADO
# (DECISION TREE vs. RANDOM FOREST vs. K-NEAREST NEIGHBORS)
# ==============================================================================

"""
OBJETIVO:
Comparar 3 familias de algoritmos supervisados para predecir el Riesgo de 
Abandono de Tratamiento en pacientes de MedReminder AI:
  1. Decision Tree (Árbol de Decisión): Reglas lógicas y transparentes.
  2. Random Forest (Bosque Aleatorio): Ensamble robusto anti-ruido.
  3. K-Nearest Neighbors (KNN): Similitud geométrica con normalización StandardScaler.

INCLUYE LOS 3 EXPERIMENTOS OBLIGATORIOS PEDIDOS POR EL PROFESOR:
  • Experimento A: Variación de 'n_neighbors' en KNN [3, 5, 7, 9, 15].
  • Experimento B: Variación de 'n_estimators' en Random Forest [50, 100, 200, 500].
  • Experimento C: Variación de 'max_depth' en Decision Tree [2, 3, 5, 8, None].
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resultados_p05")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. CARGA DE DATOS CLÍNICOS
# ------------------------------------------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(BASE_DIR), "backend", "app", "data", "dataset_entrenamiento_pacientes.csv")
if not os.path.exists(CSV_PATH):
    CSV_PATH = os.path.join(BASE_DIR, "dataset_entrenamiento_pacientes.csv")

df = pd.read_csv(CSV_PATH)
features = ["edad", "medicamentos_activos", "adherencia_historica_pct", "retraso_promedio_min", "tiene_cuidador"]
X = df[features]
y = df["riesgo_abandono"].astype(int)

# Partición 60% Train / 20% Val / 20% Test
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)

print("=" * 80)
print(" PRÁCTICA 05: TORNEO DE ALGORITMOS SUPERVISADOS (MedReminder AI)")
print("=" * 80)
print(f"Total dataset: {len(df)} pacientes | Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

# ------------------------------------------------------------------------------
# 2. DEFINICIÓN DE LOS 3 MODELOS BASE
# ------------------------------------------------------------------------------
modelos_base = {
    "Decision Tree": DecisionTreeClassifier(max_depth=4, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
    "KNN (k=5)": Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=5))
    ])
}

resultados_base = []

for nombre, modelo in modelos_base.items():
    modelo.fit(X_train, y_train)
    y_pred_val = modelo.predict(X_val)

    acc = accuracy_score(y_val, y_pred_val) * 100
    prec = precision_score(y_val, y_pred_val) * 100
    rec = recall_score(y_val, y_pred_val) * 100
    f1 = f1_score(y_val, y_pred_val) * 100

    resultados_base.append({
        "Algoritmo": nombre,
        "Exactitud_Val (%)": round(acc, 2),
        "Precisión (%)": round(prec, 2),
        "Sensibilidad_Recall (%)": round(rec, 2),
        "F1_Score (%)": round(f1, 2)
    })

df_base = pd.DataFrame(resultados_base)
print("\n" + "=" * 80)
print(" COMPARATIVA DE MODELOS EN CONJUNTO DE VALIDACIÓN (20%)")
print("=" * 80)
print(df_base.to_string(index=False))

# ------------------------------------------------------------------------------
# 3. EJECUCIÓN DE LOS 3 EXPERIMENTOS DE HIPERPARÁMETROS DEL PROFESOR
# ------------------------------------------------------------------------------
print("\n" + "=" * 80)
print(" ACTIVIDADES DE MODIFICACIÓN: EXPERIMENTOS A, B Y C")
print("=" * 80)

registros_experimentos = []

# Experimento A: KNN con n_neighbors en [3, 5, 7, 9, 15]
print("\n[Experimento A]: Modificar n_neighbors en KNN [3, 5, 7, 9, 15]")
for k in [3, 5, 7, 9, 15]:
    pipe = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=k))])
    pipe.fit(X_train, y_train)
    p_val = pipe.predict(X_val)
    f1 = f1_score(y_val, p_val) * 100
    acc = accuracy_score(y_val, p_val) * 100
    print(f" • k={k:2d} -> Exactitud: {acc:5.2f}% | F1: {f1:5.2f}%")
    registros_experimentos.append({"Experimento": "A (KNN)", "Parámetro": f"n_neighbors={k}", "Exactitud_Val": acc, "F1_Score": f1})

# Experimento B: Random Forest con n_estimators en [50, 100, 200, 500]
print("\n[Experimento B]: Modificar n_estimators en Random Forest [50, 100, 200, 500]")
for n_est in [50, 100, 200, 500]:
    rf = RandomForestClassifier(n_estimators=n_est, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    p_val = rf.predict(X_val)
    f1 = f1_score(y_val, p_val) * 100
    acc = accuracy_score(y_val, p_val) * 100
    print(f" • n_estimators={n_est:3d} -> Exactitud: {acc:5.2f}% | F1: {f1:5.2f}%")
    registros_experimentos.append({"Experimento": "B (Random Forest)", "Parámetro": f"n_estimators={n_est}", "Exactitud_Val": acc, "F1_Score": f1})

# Experimento C: Decision Tree con max_depth en [2, 3, 5, 8, None]
print("\n[Experimento C]: Modificar max_depth en Decision Tree [2, 3, 5, 8, None]")
for depth in [2, 3, 5, 8, None]:
    dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt.fit(X_train, y_train)
    p_val = dt.predict(X_val)
    f1 = f1_score(y_val, p_val) * 100
    acc = accuracy_score(y_val, p_val) * 100
    nom = "Sin límite" if depth is None else str(depth)
    print(f" • max_depth={nom:<10} -> Exactitud: {acc:5.2f}% | F1: {f1:5.2f}%")
    registros_experimentos.append({"Experimento": "C (Decision Tree)", "Parámetro": f"max_depth={nom}", "Exactitud_Val": acc, "F1_Score": f1})

df_exp = pd.DataFrame(registros_experimentos)
df_exp.to_csv(os.path.join(OUTPUT_DIR, "p05_experimentos_hiperparametros.csv"), index=False)

# ------------------------------------------------------------------------------
# 4. SELECCIÓN DEL MODELO CAMPEÓN Y REENTRENAMIENTO (TRAIN + VAL)
# ------------------------------------------------------------------------------
# Seleccionamos por F1-Score (balance óptimo entre precisión y sensibilidad en salud)
mejor_base = df_base.sort_values(by="F1_Score (%)", ascending=False).iloc[0]
mejor_nombre = mejor_base["Algoritmo"]

print("\n" + "=" * 80)
print(f" 🏆 ALGORITMO SELECCIONADO: {mejor_nombre} (F1 = {mejor_base['F1_Score (%)']}%)")
print("=" * 80)

# Unir Train + Val para entrenar la versión definitiva
X_train_val = pd.concat([X_train, X_val])
y_train_val = pd.concat([y_train, y_val])

if "Random Forest" in mejor_nombre:
    modelo_campeon = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
elif "KNN" in mejor_nombre:
    modelo_campeon = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=7))])
else:
    modelo_campeon = DecisionTreeClassifier(max_depth=5, random_state=42)

modelo_campeon.fit(X_train_val, y_train_val)

# ------------------------------------------------------------------------------
# 5. EVALUACIÓN FINAL EN DATOS DE PRUEBA (TEST SET)
# ------------------------------------------------------------------------------
y_pred_final = modelo_campeon.predict(X_test)
acc_final = accuracy_score(y_test, y_pred_final) * 100
prec_final = precision_score(y_test, y_pred_final) * 100
rec_final = recall_score(y_test, y_pred_final) * 100
f1_final = f1_score(y_test, y_pred_final) * 100

print("\nEVALUACIÓN DEFINITIVA EN PACIENTES NUNCA ANTES VISTOS (TEST SET - 20%):")
print(f" • Exactitud:    {acc_final:.2f}%")
print(f" • Precisión:    {prec_final:.2f}%")
print(f" • Sensibilidad: {rec_final:.2f}% (Capacidad de detectar a los enfermos/en riesgo)")
print(f" • F1-Score:     {f1_final:.2f}%")

cm = confusion_matrix(y_test, y_pred_final)
print("\nMatriz de Confusión del Campeón:")
print(f"  [VN={cm[0,0]}  FP={cm[0,1]}]")
print(f"  [FN={cm[1,0]}  VP={cm[1,1]}]")

# Validación cruzada 5-Fold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(modelo_campeon, X_train_val, y_train_val, cv=cv, scoring="f1") * 100
print(f"\nValidación Cruzada 5-Fold (F1-Score): {cv_scores.mean():.2f}% ± {cv_scores.std():.2f}%")

# ------------------------------------------------------------------------------
# 6. GENERACIÓN DE GRÁFICA COMPARATIVA DE BARRAS
# ------------------------------------------------------------------------------
plt.figure(figsize=(9, 5))
x_idx = np.arange(len(df_base))
ancho = 0.2

plt.bar(x_idx - 1.5 * ancho, df_base["Exactitud_Val (%)"], width=ancho, label="Exactitud (Accuracy)", color="#1E3A8A")
plt.bar(x_idx - 0.5 * ancho, df_base["Precisión (%)"], width=ancho, label="Precisión", color="#0E8074")
plt.bar(x_idx + 0.5 * ancho, df_base["Sensibilidad_Recall (%)"], width=ancho, label="Recall (Sensibilidad)", color="#F59E0B")
plt.bar(x_idx + 1.5 * ancho, df_base["F1_Score (%)"], width=ancho, label="F1-Score", color="#10B981")

plt.xticks(x_idx, df_base["Algoritmo"], fontweight="bold", fontsize=10)
plt.ylabel("Porcentaje (%)", fontweight="bold")
plt.title("Comparativa de Modelos Supervisados - MedReminder AI", fontweight="bold", fontsize=12)
plt.ylim(40, 105)
plt.grid(axis="y", linestyle=":", alpha=0.6)
plt.legend(loc="lower right", fontsize=8.5)
plt.tight_layout()

bar_path = os.path.join(OUTPUT_DIR, "p05_comparacion_algoritmos_medreminder.png")
plt.savefig(bar_path, dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 7. GRÁFICA DE MATRIZ DE CONFUSIÓN
# ------------------------------------------------------------------------------
plt.figure(figsize=(5.5, 4.5))
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Greens)
plt.title(f"Matriz de Confusión - {mejor_nombre}", fontweight="bold", fontsize=11)
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ["Estable (0)", "Riesgo (1)"])
plt.yticks(tick_marks, ["Estable (0)", "Riesgo (1)"])

thresh = cm.max() / 2.0
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], "d"),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black",
                 fontweight="bold")

plt.ylabel("Etiqueta Real", fontweight="bold")
plt.xlabel("Predicción del Modelo", fontweight="bold")
plt.tight_layout()

cm_path = os.path.join(OUTPUT_DIR, "p05_matriz_confusion_medreminder.png")
plt.savefig(cm_path, dpi=300)
plt.close()

# Guardar tabla comparativa en CSV
df_base.to_csv(os.path.join(OUTPUT_DIR, "p05_resultados_comparacion.csv"), index=False)

print(f"\n[OK] Gráficas y tablas guardadas exitosamente:")
print(f" ✓ Gráfica de Métricas: {bar_path}")
print(f" ✓ Matriz de Confusión: {cm_path}")
print(f" ✓ CSV de Comparación:  {os.path.join(OUTPUT_DIR, 'p05_resultados_comparacion.csv')}")
print(f" ✓ CSV de Experimentos: {os.path.join(OUTPUT_DIR, 'p05_experimentos_hiperparametros.csv')}")
print("=" * 80)
