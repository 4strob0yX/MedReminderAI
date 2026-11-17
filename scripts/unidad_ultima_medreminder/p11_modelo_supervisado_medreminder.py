"""
PRÁCTICA 11 - MEDREMINDER AI (ETAPA 2): MODELO SUPERVISADO Y PERSISTENCIA JOBLIB
Compara Decision Tree, Random Forest y KNN; guarda modelos/modelo_supervisado_medreminder.joblib.
"""

from pathlib import Path
import joblib
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
from _datos_medreminder import FEATURES_CLINICAS, TARGET_CLINICO

BASE_DIR = Path(__file__).resolve().parent
RUTA_RESULTADOS = BASE_DIR / "resultados_medreminder"
RUTA_MODELOS = RUTA_RESULTADOS / "modelos"
RUTA_MODELOS.mkdir(parents=True, exist_ok=True)
ARCHIVO_DATOS = RUTA_RESULTADOS / "medreminder_datos.csv"
SEMILLA = 42


def main() -> None:
    if not ARCHIVO_DATOS.exists():
        raise FileNotFoundError(f"Falta {ARCHIVO_DATOS}. Ejecuta primero p10_datos_medreminder.py")

    df = pd.read_csv(ARCHIVO_DATOS)
    X = df[FEATURES_CLINICAS]
    y = df[TARGET_CLINICO].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=SEMILLA, stratify=y)

    candidatos = {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=SEMILLA),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=5, random_state=SEMILLA),
        "KNN": Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=5))]),
    }

    filas, entrenados = [], {}
    for nom, clf in candidatos.items():
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)
        entrenados[nom] = clf
        filas.append({
            "algoritmo": nom,
            "accuracy": round(accuracy_score(y_test, pred), 4),
            "precision": round(precision_score(y_test, pred, zero_division=0), 4),
            "recall": round(recall_score(y_test, pred, zero_division=0), 4),
            "f1_score": round(f1_score(y_test, pred, zero_division=0), 4),
        })

    tabla = pd.DataFrame(filas).sort_values("f1_score", ascending=False)
    print("=== ETAPA 2 MEDREMINDER AI: MODELOS SUPERVISADOS ===")
    print(tabla.to_string(index=False))
    tabla.to_csv(RUTA_RESULTADOS / "comparacion_supervisados_medreminder.csv", index=False, encoding="utf-8")

    ganador = tabla.iloc[0]["algoritmo"]
    modelo_ganador = entrenados[ganador]

    paquete = {
        "modelo": modelo_ganador,
        "nombre_modelo": ganador,
        "caracteristicas": FEATURES_CLINICAS,
        "variable_objetivo": TARGET_CLINICO,
        "semilla": SEMILLA,
    }
    ruta_modelo = RUTA_MODELOS / "modelo_supervisado_medreminder.joblib"
    joblib.dump(paquete, ruta_modelo)
    print(f"\nModelo ganador ({ganador}) guardado en: {ruta_modelo}")

    ax = tabla.set_index("algoritmo")[["accuracy", "precision", "recall", "f1_score"]].plot(kind="bar", figsize=(7, 4.5))
    ax.set_ylim(0, 1.05)
    ax.set_title("Modelos Supervisados - MedReminder AI (P11)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(RUTA_RESULTADOS / "comparacion_supervisados_medreminder.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
