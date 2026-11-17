"""
PRÁCTICA 05 - MEDREMINDER AI: COMPARACIÓN DE ALGORITMOS + 3 EXPERIMENTOS
Comparativa Decision Tree vs Random Forest vs KNN sobre el dataset clínico oficial
e incluye Experimento A (KNN n_neighbors), Experimento B (RF n_estimators) y Experimento C (DT max_depth).
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from _datos_medreminder import FEATURES_CLINICAS, TARGET_CLINICO, cargar_dataset_clinico

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p05"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
SEMILLA = 42

df = cargar_dataset_clinico()
X = df[FEATURES_CLINICAS]
y = df[TARGET_CLINICO].astype(int)

X_tv, X_test, y_tv, y_test = train_test_split(X, y, test_size=0.20, random_state=SEMILLA, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_tv, y_tv, test_size=0.25, random_state=SEMILLA, stratify=y_tv)

modelos_base = {
    "Decision Tree (depth=5)": DecisionTreeClassifier(max_depth=5, random_state=SEMILLA),
    "Random Forest (n=100)": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=SEMILLA),
    "KNN (k=5 + Scaler)": Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=5))]),
}

base_rows = []
for nombre, clf in modelos_base.items():
    clf.fit(X_train, y_train)
    p_val = clf.predict(X_val)
    base_rows.append({
        "modelo": nombre,
        "acc_val": round(accuracy_score(y_val, p_val), 4),
        "prec_val": round(precision_score(y_val, p_val, zero_division=0), 4),
        "rec_val": round(recall_score(y_val, p_val, zero_division=0), 4),
        "f1_val": round(f1_score(y_val, p_val, zero_division=0), 4),
    })

df_base = pd.DataFrame(base_rows)
print("=== COMPARATIVA BASE MEDREMINDER AI ===")
print(df_base.to_string(index=False))

# 3 Experimentos obligatorios
exp_rows = []
for k in [3, 5, 7, 9, 15]:
    m = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=k))]).fit(X_train, y_train)
    exp_rows.append({
        "experimento": "A_KNN_n_neighbors", "parametro": str(k),
        "val_f1": round(f1_score(y_val, m.predict(X_val)), 4),
        "test_f1": round(f1_score(y_test, m.predict(X_test)), 4),
    })

for n_est in [50, 100, 200, 500]:
    m = RandomForestClassifier(n_estimators=n_est, max_depth=5, random_state=SEMILLA).fit(X_train, y_train)
    exp_rows.append({
        "experimento": "B_RF_n_estimators", "parametro": str(n_est),
        "val_f1": round(f1_score(y_val, m.predict(X_val)), 4),
        "test_f1": round(f1_score(y_test, m.predict(X_test)), 4),
    })

for depth in [2, 3, 5, 8, None]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=SEMILLA).fit(X_train, y_train)
    exp_rows.append({
        "experimento": "C_DT_max_depth", "parametro": "None" if depth is None else str(depth),
        "val_f1": round(f1_score(y_val, m.predict(X_val)), 4),
        "test_f1": round(f1_score(y_test, m.predict(X_test)), 4),
    })

df_exp = pd.DataFrame(exp_rows)
print("\n=== EXPERIMENTOS A, B y C (MEDREMINDER AI) ===")
print(df_exp.to_string(index=False))

df_base.to_csv(RESULTADOS_DIR / "p05_base_medreminder.csv", index=False, encoding="utf-8")
df_exp.to_csv(RESULTADOS_DIR / "p05_experimentos_medreminder.csv", index=False, encoding="utf-8")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (key, title) in zip(axes, [
    ("A_KNN_n_neighbors", "Exp A: KNN n_neighbors"),
    ("B_RF_n_estimators", "Exp B: RF n_estimators"),
    ("C_DT_max_depth", "Exp C: DT max_depth"),
]):
    sub = df_exp[df_exp["experimento"] == key]
    ax.plot(sub["parametro"], sub["val_f1"], marker="o", label="Val F1")
    ax.plot(sub["parametro"], sub["test_f1"], marker="s", linestyle="--", label="Test F1")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p05_experimentos_medreminder.png", dpi=200)
plt.close()
print(f"Exportados en: {RESULTADOS_DIR}")
