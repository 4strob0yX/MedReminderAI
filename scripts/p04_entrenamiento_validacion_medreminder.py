# ==============================================================================
# UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA (UTVT)
# PROYECTO FINAL: MedReminder AI
# PRÁCTICA 04: ENTRENAMIENTO, VALIDACIÓN Y PRUEBA (DIAGNÓSTICO DE OVERFITTING)
# ==============================================================================

"""
CASO CLÍNICO: MedReminder AI
Objetivo: Diagnosticar el ajuste del modelo de clasificación (Underfitting vs Overfitting)
para predecir el Riesgo de Abandono de Tratamiento Médico en pacientes.

División Metodológica:
  • 60% Entrenamiento (Aprender patrones clínicos)
  • 20% Validación    (Calibrar la profundidad del árbol 'max_depth' sin sesgo)
  • 20% Prueba        (Evaluación final simulando pacientes nuevos en la App)
"""

import os
import matplotlib
matplotlib.use("Agg")  # Generar gráficos sin requerir servidor X11 interactivo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

# Directorios de salida
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resultados_p04")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. CARGA DEL DATASET CLÍNICO (MedReminder AI)
# ------------------------------------------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(BASE_DIR), "backend", "app", "data", "dataset_entrenamiento_pacientes.csv")
if not os.path.exists(CSV_PATH):
    CSV_PATH = os.path.join(BASE_DIR, "dataset_entrenamiento_pacientes.csv")

df = pd.read_csv(CSV_PATH)

features = ["edad", "medicamentos_activos", "adherencia_historica_pct", "retraso_promedio_min", "tiene_cuidador"]
target = "riesgo_abandono"

X = df[features]
y = df[target].astype(int)

print("=" * 75)
print(" PRÁCTICA 04: EVALUACIÓN Y DETECCIÓN DE OVERFITTING (MedReminder AI)")
print("=" * 75)
print(f"Total pacientes analizados: {len(df)}")
print(f"Variables clínicas: {features}")
print(f"Balance objetivo: {dict(y.value_counts())} (0: Adherente, 1: En Riesgo)")

# ------------------------------------------------------------------------------
# 2. PARTICIÓN TRIPLE: 60% TRAIN / 20% VALIDACIÓN / 20% PRUEBA
# ------------------------------------------------------------------------------
# Paso 1: Separar 20% para Prueba final
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Paso 2: Del 80% restante, tomar 25% para validación (0.80 * 0.25 = 20% del total)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

print(f"\nParticiones:")
print(f" • Entrenamiento (60%): {len(X_train)} pacientes")
print(f" • Validación    (20%): {len(X_val)} pacientes")
print(f" • Prueba        (20%): {len(X_test)} pacientes")

# ------------------------------------------------------------------------------
# 3. EXPERIMENTACIÓN CON PROFUNDIDADES DEL ÁRBOL (max_depth)
# ------------------------------------------------------------------------------
profundidades = [1, 2, 3, 4, 5, 8, 10, None]
resultados = []

for prof in profundidades:
    clf = DecisionTreeClassifier(max_depth=prof, random_state=42)
    clf.fit(X_train, y_train)

    acc_train = accuracy_score(y_train, clf.predict(X_train)) * 100
    acc_val = accuracy_score(y_val, clf.predict(X_val)) * 100
    diferencia = acc_train - acc_val

    # Diagnóstico de sesgo/varianza
    if prof == 1:
        diagnostico = "Subajuste (Underfitting) - Modelo demasiado simple"
    elif acc_train > 98.0 and diferencia > 15.0:
        diagnostico = "Sobreajuste (Overfitting) - Memoriza ruido"
    elif diferencia <= 10.0 and acc_val >= 70.0:
        diagnostico = "Ajuste Óptimo (Buen Balance)"
    else:
        diagnostico = "Ajuste Intermedio"

    nombre_prof = "Sin límite" if prof is None else str(prof)
    resultados.append({
        "profundidad": nombre_prof,
        "exactitud_train": round(acc_train, 2),
        "exactitud_val": round(acc_val, 2),
        "diferencia": round(diferencia, 2),
        "diagnostico": diagnostico
    })

df_res = pd.DataFrame(resultados)
print("\n" + "=" * 75)
print(" TABLA DE EVALUACIÓN DE PROFUNDIDADES (TRAIN VS VALIDACIÓN)")
print("=" * 75)
print(df_res.to_string(index=False))

# Guardar CSV comparativo
csv_comparacion = os.path.join(OUTPUT_DIR, "p04_comparacion_profundidades.csv")
df_res.to_csv(csv_comparacion, index=False)

# ------------------------------------------------------------------------------
# 4. SELECCIÓN DEL MODELO ÓPTIMO BASADO EN VALIDACIÓN
# ------------------------------------------------------------------------------
# Buscamos la profundidad numérica con mayor exactitud en validación y menor brecha
mejor_fila = df_res.sort_values(by=["exactitud_val", "diferencia"], ascending=[False, True]).iloc[0]
mejor_prof_str = mejor_fila["profundidad"]
mejor_prof = None if mejor_prof_str == "Sin límite" else int(mejor_prof_str)

print(f"\n[MODELO GANADOR]: Profundidad óptima = {mejor_prof_str} "
      f"(Validación = {mejor_fila['exactitud_val']}%, Brecha = {mejor_fila['diferencia']}%)")

# ------------------------------------------------------------------------------
# 5. REENTRENAMIENTO (TRAIN + VAL) Y EVALUACIÓN FINAL EN TEST SET
# ------------------------------------------------------------------------------
# Como enseñó el profesor: una vez elegido el hiperparámetro, reentrenamos con Train + Val
X_train_val = pd.concat([X_train, X_val])
y_train_val = pd.concat([y_train, y_val])

modelo_final = DecisionTreeClassifier(max_depth=mejor_prof, random_state=42)
modelo_final.fit(X_train_val, y_train_val)

y_pred_test = modelo_final.predict(X_test)
acc_test = accuracy_score(y_test, y_pred_test) * 100
prec_test = precision_score(y_test, y_pred_test) * 100
rec_test = recall_score(y_test, y_pred_test) * 100
f1_test = f1_score(y_test, y_pred_test) * 100

print("\n" + "=" * 75)
print(" RESULTADOS EN EL CONJUNTO DE PRUEBA INDEPENDIENTE (TEST SET - 20%)")
print("=" * 75)
print(f"Exactitud (Accuracy):  {acc_test:.2f}%")
print(f"Precisión (Precision): {prec_test:.2f}%")
print(f"Sensibilidad (Recall): {rec_test:.2f}%  <- Crítica en salud para no omitir alertas")
print(f"Puntuación F1:         {f1_test:.2f}%")

cm = confusion_matrix(y_test, y_pred_test)
print("\nMatriz de Confusión en Prueba:")
print(f"  [VN={cm[0,0]}  FP={cm[0,1]}]")
print(f"  [FN={cm[1,0]}  VP={cm[1,1]}]")

# ------------------------------------------------------------------------------
# 6. VALIDACIÓN CRUZADA ESTRATIFICADA (5 FOLDS)
# ------------------------------------------------------------------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(modelo_final, X_train_val, y_train_val, cv=cv, scoring="accuracy") * 100

print(f"\nValidación Cruzada (5-Fold Stratified):")
print(f"Folds individuales: {[round(s, 2) for s in cv_scores]}%")
print(f"Promedio:           {cv_scores.mean():.2f}% ± {cv_scores.std():.2f}%")

# ------------------------------------------------------------------------------
# 7. GENERACIÓN DE GRÁFICA DE CURVA DE APRENDIZAJE (TRAIN VS VALIDACIÓN)
# ------------------------------------------------------------------------------
profs_num = [1, 2, 3, 4, 5, 8, 10, 12]
acc_tr_plot = []
acc_val_plot = []

for p in profs_num:
    m = DecisionTreeClassifier(max_depth=p, random_state=42)
    m.fit(X_train, y_train)
    acc_tr_plot.append(accuracy_score(y_train, m.predict(X_train)) * 100)
    acc_val_plot.append(accuracy_score(y_val, m.predict(X_val)) * 100)

plt.figure(figsize=(9, 5.5))
plt.plot(profs_num, acc_tr_plot, marker="o", color="#1E3A8A", linewidth=2.2, label="Entrenamiento (Train)")
plt.plot(profs_num, acc_val_plot, marker="s", color="#0E8074", linewidth=2.2, linestyle="--", label="Validación (Val)")

# Zona de overfitting
plt.axvspan(6, 12, alpha=0.15, color="#EF4444", label="Zona de Sobreajuste (Overfitting)")
plt.axvline(x=mejor_prof if mejor_prof is not None else 4, color="#10B981", linestyle=":", linewidth=2, label=f"Mejor Modelo (depth={mejor_prof})")

plt.title("Práctica 04: Curva de Complejidad y Sobreajuste - MedReminder AI", fontsize=12, fontweight="bold", pad=12)
plt.xlabel("Profundidad Máxima del Árbol (max_depth)", fontsize=10, fontweight="bold")
plt.ylabel("Exactitud (Accuracy %)", fontsize=10, fontweight="bold")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="lower right", fontsize=9)
plt.tight_layout()

curva_path = os.path.join(OUTPUT_DIR, "p04_curva_sobreajuste_medreminder.png")
plt.savefig(curva_path, dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 8. GRÁFICA DE MATRIZ DE CONFUSIÓN
# ------------------------------------------------------------------------------
plt.figure(figsize=(5.5, 4.5))
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.title(f"Matriz de Confusión - Decision Tree (depth={mejor_prof})", fontsize=10, fontweight="bold")
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

cm_path = os.path.join(OUTPUT_DIR, "p04_matriz_confusion_medreminder.png")
plt.savefig(cm_path, dpi=300)
plt.close()

print(f"\n[OK] Gráficas generadas exitosamente:")
print(f" ✓ Curva de aprendizaje: {curva_path}")
print(f" ✓ Matriz de confusión: {cm_path}")
print("=" * 75)
