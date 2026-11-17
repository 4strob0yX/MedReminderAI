"""
PRÁCTICA 12 - MEDREMINDER AI (ETAPA 3): SEGMENTACIÓN CLÍNICA K-MEANS
Evalúa K=2..6 y guarda modelos/modelo_kmeans_medreminder.joblib.
"""

from pathlib import Path
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from _datos_medreminder import FEATURES_CLINICAS

BASE_DIR = Path(__file__).resolve().parent
RUTA_RESULTADOS = BASE_DIR / "resultados_medreminder"
RUTA_MODELOS = RUTA_RESULTADOS / "modelos"
RUTA_MODELOS.mkdir(parents=True, exist_ok=True)
ARCHIVO_DATOS = RUTA_RESULTADOS / "medreminder_datos.csv"
SEMILLA = 42


def main() -> None:
    if not ARCHIVO_DATOS.exists():
        raise FileNotFoundError(f"Falta {ARCHIVO_DATOS}. Ejecuta primero p10_datos_medreminder.py")

    datos = pd.read_csv(ARCHIVO_DATOS)
    X = datos[FEATURES_CLINICAS]
    escalador = StandardScaler()
    X_scaled = escalador.fit_transform(X)

    eval_rows = []
    for k in range(2, 7):
        km = KMeans(n_clusters=k, n_init=20, random_state=SEMILLA)
        etq = km.fit_predict(X_scaled)
        eval_rows.append({"k": k, "inercia": round(km.inertia_, 2), "silhouette": round(silhouette_score(X_scaled, etq), 4)})
    df_eval = pd.DataFrame(eval_rows)
    print("=== ETAPA 3 MEDREMINDER AI: EVALUACIÓN K (2..6) ===")
    print(df_eval.to_string(index=False))

    k_optimo = 3  # 3 perfiles clínicos canónicos de MedReminder AI
    modelo = KMeans(n_clusters=k_optimo, n_init=20, random_state=SEMILLA)
    clusters = modelo.fit_predict(X_scaled)

    cent_orig = pd.DataFrame(escalador.inverse_transform(modelo.cluster_centers_), columns=FEATURES_CLINICAS)
    orden = cent_orig["adherencia_historica_pct"].sort_values().index.tolist()
    nombres = ["Requiere acompañamiento", "Cumplimiento moderado", "Adherencia óptima"]
    mapa_perfiles = {cid: nombres[pos] for pos, cid in enumerate(orden)}

    seg = datos.copy()
    seg["cluster"] = clusters
    seg["perfil"] = seg["cluster"].map(mapa_perfiles)
    resumen = seg.groupby("perfil")[FEATURES_CLINICAS].mean().round(2)
    print("\nResumen de perfiles clínicos:\n", resumen)

    seg.to_csv(RUTA_RESULTADOS / "pacientes_segmentados.csv", index=False, encoding="utf-8")
    resumen.to_csv(RUTA_RESULTADOS / "resumen_perfiles_medreminder.csv", encoding="utf-8")
    df_eval.to_csv(RUTA_RESULTADOS / "evaluacion_k_medreminder.csv", index=False, encoding="utf-8")

    ruta_km = RUTA_MODELOS / "modelo_kmeans_medreminder.joblib"
    joblib.dump({
        "modelo": modelo,
        "escalador": escalador,
        "caracteristicas": FEATURES_CLINICAS,
        "mapa_perfiles": mapa_perfiles,
        "numero_clusters": k_optimo,
        "semilla": SEMILLA,
    }, ruta_km)
    print(f"Modelo K-Means guardado en: {ruta_km}")

    plt.figure(figsize=(7, 5))
    for cid, nom in mapa_perfiles.items():
        sub = seg[seg["cluster"] == cid]
        plt.scatter(sub["adherencia_historica_pct"], sub["retraso_promedio_min"], label=nom, alpha=0.75)
    plt.xlabel("Adherencia histórica (%)")
    plt.ylabel("Retraso promedio (min)")
    plt.title("Clústeres Clínicos MedReminder AI (P12)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RUTA_RESULTADOS / "segmentacion_kmeans_medreminder.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
