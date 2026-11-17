"""
PRÁCTICA 04 - MEDREMINDER AI: ENTRENAMIENTO, VALIDACIÓN Y PRUEBA (60/20/20)
Diagnóstico de Underfitting vs Overfitting + StratifiedKFold exclusivo sobre Train.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier
from _datos_medreminder import FEATURES_CLINICAS, TARGET_CLINICO, cargar_dataset_clinico

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p04"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
SEMILLA = 42

df = cargar_dataset_clinico()
X = df[FEATURES_CLINICAS]
y = df[TARGET_CLINICO].astype(int)

X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.20, random_state=SEMILLA, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=SEMILLA, stratify=y_train_val)

print(f"MedReminder AI P04 -> Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

profundidades = [1, 2, 3, 5, 10, None]
filas = []
modelos = {}
for d in profundidades:
    clf = DecisionTreeClassifier(max_depth=d, random_state=SEMILLA)
    clf.fit(X_train, y_train)
    acc_tr = accuracy_score(y_train, clf.predict(X_train))
    acc_va = accuracy_score(y_val, clf.predict(X_val))
    brecha = acc_tr - acc_va
    diag = "Subajuste" if (acc_tr < 0.80 and acc_va < 0.80) else ("Sobreajuste" if brecha > 0.10 else "Buen ajuste")
    etq = "Sin límite" if d is None else str(d)
    modelos[etq] = clf
    filas.append({
        "max_depth": etq,
        "orden": 12 if d is None else d,
        "acc_train": round(acc_tr, 4),
        "acc_val": round(acc_va, 4),
        "brecha": round(brecha, 4),
        "diagnostico": diag,
    })

df_prof = pd.DataFrame(filas)
print("\n=== DIAGNÓSTICO DE AJUSTE (CLÍNICO) ===")
print(df_prof.drop(columns=["orden"]).to_string(index=False))

mejor_fila = df_prof.sort_values(["acc_val", "brecha"], ascending=[False, True]).iloc[0]
mejor_etq = mejor_fila["max_depth"]
mejor_clf = modelos[mejor_etq]

pred_test = mejor_clf.predict(X_test)
print(f"\nMejor profundidad: {mejor_etq} | Test Acc={accuracy_score(y_test, pred_test):.2%} | F1={f1_score(y_test, pred_test):.2%}")
print(classification_report(y_test, pred_test, zero_division=0))

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)
d_num = None if mejor_etq == "Sin límite" else int(mejor_etq)
cv_scores = cross_val_score(DecisionTreeClassifier(max_depth=d_num, random_state=SEMILLA), X_train, y_train, cv=cv, scoring="accuracy")
print(f"StratifiedKFold (solo Train, 5 folds): {cv_scores.mean():.2%} +/- {cv_scores.std():.2%}")

plt.figure(figsize=(8, 4.5))
plt.plot(df_prof["orden"], df_prof["acc_train"], marker="o", label="Entrenamiento")
plt.plot(df_prof["orden"], df_prof["acc_val"], marker="s", label="Validación")
plt.xticks(df_prof["orden"], df_prof["max_depth"])
plt.title("MedReminder AI P04: Entrenamiento vs Validación")
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p04_entrenamiento_vs_validacion_medreminder.png", dpi=200)
plt.close()

cm = confusion_matrix(y_test, pred_test)
plt.figure(figsize=(5, 4))
plt.imshow(cm, cmap="Blues")
plt.title(f"Matriz de Confusión MedReminder P04 (depth={mejor_etq})")
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, str(cm[i, j]), ha="center", va="center")
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p04_matriz_confusion_medreminder.png", dpi=200)
plt.close()

df_prof.drop(columns=["orden"]).to_csv(RESULTADOS_DIR / "p04_resultados_medreminder.csv", index=False, encoding="utf-8")
print(f"Exportados en: {RESULTADOS_DIR}")
