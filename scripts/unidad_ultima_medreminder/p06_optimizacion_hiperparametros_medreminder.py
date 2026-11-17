"""
PRÁCTICA 06 - MEDREMINDER AI: OPTIMIZACIÓN DE HIPERPARÁMETROS
GridSearchCV vs RandomizedSearchCV con StratifiedKFold para Decision Tree, Random Forest y KNN
sobre el dataset clínico oficial de MedReminder AI.
"""

import time
from pathlib import Path
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from _datos_medreminder import FEATURES_CLINICAS, TARGET_CLINICO, cargar_dataset_clinico

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p06"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
SEMILLA = 42

df = cargar_dataset_clinico()
X = df[FEATURES_CLINICAS]
y = df[TARGET_CLINICO].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=SEMILLA, stratify=y)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)

modelos_grid = {
    "Decision Tree": (
        DecisionTreeClassifier(random_state=SEMILLA),
        {"max_depth": [3, 5, 8, None], "min_samples_split": [2, 5, 10], "min_samples_leaf": [1, 2, 4], "criterion": ["gini", "entropy"]},
    ),
    "Random Forest": (
        RandomForestClassifier(random_state=SEMILLA),
        {"n_estimators": [50, 100, 200], "max_depth": [3, 5, 8, None], "min_samples_split": [2, 5, 10]},
    ),
    "KNN": (
        Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier())]),
        {"knn__n_neighbors": [3, 5, 7, 9, 11], "knn__weights": ["uniform", "distance"], "knn__metric": ["euclidean", "manhattan"]},
    ),
}

modelos_random = {
    "Decision Tree": (
        DecisionTreeClassifier(random_state=SEMILLA),
        {"max_depth": [2, 3, 4, 5, 6, 8, None], "min_samples_split": [2, 4, 6, 10, 15], "min_samples_leaf": [1, 2, 3, 5], "criterion": ["gini", "entropy"]},
    ),
    "Random Forest": (
        RandomForestClassifier(random_state=SEMILLA),
        {"n_estimators": [50, 80, 100, 150, 200, 300], "max_depth": [3, 5, 7, 10, None], "min_samples_split": [2, 5, 8, 12], "min_samples_leaf": [1, 2, 4]},
    ),
    "KNN": (
        Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier())]),
        {"knn__n_neighbors": [3, 5, 7, 9, 11, 15], "knn__weights": ["uniform", "distance"], "knn__metric": ["euclidean", "manhattan"]},
    ),
}

grid_rows, mejores_grid = [], {}
for nombre, (est, grid) in modelos_grid.items():
    t0 = time.perf_counter()
    gs = GridSearchCV(est, param_grid=grid, scoring="f1", cv=cv, n_jobs=-1)
    gs.fit(X_train, y_train)
    dur = time.perf_counter() - t0
    mejores_grid[nombre] = gs.best_estimator_
    grid_rows.append({"algoritmo": nombre, "f1_cv": round(gs.best_score_, 4), "tiempo_seg": round(dur, 3), "hiperparametros": str(gs.best_params_)})

rand_rows, mejores_rand = [], {}
for nombre, (est, dist) in modelos_random.items():
    t0 = time.perf_counter()
    rs = RandomizedSearchCV(est, param_distributions=dist, n_iter=15, scoring="f1", cv=cv, random_state=SEMILLA, n_jobs=-1)
    rs.fit(X_train, y_train)
    dur = time.perf_counter() - t0
    mejores_rand[nombre] = rs.best_estimator_
    rand_rows.append({"algoritmo": nombre, "f1_cv": round(rs.best_score_, 4), "tiempo_seg": round(dur, 3), "hiperparametros": str(rs.best_params_)})

df_grid = pd.DataFrame(grid_rows)
df_rand = pd.DataFrame(rand_rows)
comp = df_grid[["algoritmo", "f1_cv", "tiempo_seg"]].merge(df_rand[["algoritmo", "f1_cv", "tiempo_seg"]], on="algoritmo", suffixes=("_grid", "_random"))

print("=== P06 MEDREMINDER AI: GRIDSEARCHCV ===")
print(df_grid.to_string(index=False))
print("\n=== RANDOMIZEDSEARCHCV ===")
print(df_rand.to_string(index=False))

mejor_nombre = df_grid.sort_values("f1_cv", ascending=False).iloc[0]["algoritmo"]
mejor_modelo = mejores_grid[mejor_nombre]
y_pred = mejor_modelo.predict(X_test)
print(f"\nGanador óptimo ({mejor_nombre}) en Test -> Acc={accuracy_score(y_test, y_pred):.2%} | Precision={precision_score(y_test, y_pred):.2%} | Recall={recall_score(y_test, y_pred):.2%} | F1={f1_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred, zero_division=0))

joblib.dump(mejor_modelo, RESULTADOS_DIR / "modelo_optimizado_p06_medreminder.joblib")
df_grid.to_csv(RESULTADOS_DIR / "p06_resultados_gridsearch_medreminder.csv", index=False, encoding="utf-8")
df_rand.to_csv(RESULTADOS_DIR / "p06_resultados_randomized_medreminder.csv", index=False, encoding="utf-8")
comp.to_csv(RESULTADOS_DIR / "p06_comparacion_metodos_medreminder.csv", index=False, encoding="utf-8")

x_pos = np.arange(len(comp))
plt.figure(figsize=(8, 4.5))
plt.bar(x_pos - 0.18, comp["f1_cv_grid"], width=0.35, label="GridSearchCV")
plt.bar(x_pos + 0.18, comp["f1_cv_random"], width=0.35, label="RandomizedSearchCV")
plt.xticks(x_pos, comp["algoritmo"])
plt.ylim(0, 1.05)
plt.ylabel("F1-score CV")
plt.title("Optimización de Hiperparámetros MedReminder AI (P06)")
plt.legend()
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p06_comparacion_optimizacion_medreminder.png", dpi=200)
plt.close()

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
plt.imshow(cm, cmap="Blues")
plt.title(f"Matriz Confusión P06 ({mejor_nombre})")
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, str(cm[i, j]), ha="center", va="center")
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p06_matriz_confusion_medreminder.png", dpi=200)
plt.close()
print(f"Exportados en: {RESULTADOS_DIR}")
