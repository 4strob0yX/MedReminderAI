"""
PRÁCTICA 13 - MEDREMINDER AI (ETAPA 4): REDUCCIÓN DE DIMENSIONALIDAD PCA
Reutiliza el escalador de K-Means y guarda modelos/modelo_pca_medreminder.joblib.
"""

from pathlib import Path
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from _datos_medreminder import FEATURES_CLINICAS

BASE_DIR = Path(__file__).resolve().parent
RUTA_RESULTADOS = BASE_DIR / "resultados_medreminder"
RUTA_MODELOS = RUTA_RESULTADOS / "modelos"

ARCHIVO_DATOS = RUTA_RESULTADOS / "medreminder_datos.csv"
ARCHIVO_SEG = RUTA_RESULTADOS / "pacientes_segmentados.csv"
ARCHIVO_KM = RUTA_MODELOS / "modelo_kmeans_medreminder.joblib"


def main() -> None:
    for r in [ARCHIVO_DATOS, ARCHIVO_SEG, ARCHIVO_KM]:
        if not r.exists():
            raise FileNotFoundError(f"Falta archivo previo: {r}. Ejecuta p10 -> p12.")

    datos = pd.read_csv(ARCHIVO_DATOS)
    seg = pd.read_csv(ARCHIVO_SEG)
    paq_km = joblib.load(ARCHIVO_KM)
    escalador = paq_km["escalador"]

    X_scaled = escalador.transform(datos[FEATURES_CLINICAS])
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)

    var_ind = pca.explained_variance_ratio_
    var_acum = np.cumsum(var_ind)
    tabla_var = pd.DataFrame({
        "componente": ["PC1", "PC2"],
        "varianza_explicada_pct": np.round(var_ind * 100, 2),
        "varianza_acumulada_pct": np.round(var_acum * 100, 2),
    })
    cargas = pd.DataFrame(np.round(pca.components_, 4), index=["PC1", "PC2"], columns=FEATURES_CLINICAS)

    print("=== ETAPA 4 MEDREMINDER AI: PCA ===")
    print(tabla_var.to_string(index=False))
    print("\nCargas:\n", cargas)

    out = datos[["id_paciente"]].copy()
    out["cluster"] = seg["cluster"]
    out["perfil"] = seg["perfil"]
    out["PC1"] = np.round(coords[:, 0], 4)
    out["PC2"] = np.round(coords[:, 1], 4)

    tabla_var.to_csv(RUTA_RESULTADOS / "varianza_pca_medreminder.csv", index=False, encoding="utf-8")
    cargas.to_csv(RUTA_RESULTADOS / "cargas_pca_medreminder.csv", encoding="utf-8")
    out.to_csv(RUTA_RESULTADOS / "pacientes_pca_medreminder.csv", index=False, encoding="utf-8")

    plt.figure(figsize=(7, 5))
    for p_nom, sub in out.groupby("perfil"):
        plt.scatter(sub["PC1"], sub["PC2"], label=p_nom, alpha=0.75)
    plt.xlabel(f"PC1 ({var_ind[0]*100:.1f}%)")
    plt.ylabel(f"PC2 ({var_ind[1]*100:.1f}%)")
    plt.title("Mapa PCA 2D de Pacientes - MedReminder AI (P13)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(RUTA_RESULTADOS / "pca_segmentacion_medreminder.png", dpi=200)
    plt.close()

    ruta_pca = RUTA_MODELOS / "modelo_pca_medreminder.joblib"
    joblib.dump({"modelo_pca": pca, "escalador": escalador, "caracteristicas": FEATURES_CLINICAS, "numero_componentes": 2}, ruta_pca)
    print(f"Modelo PCA guardado en: {ruta_pca}")


if __name__ == "__main__":
    main()
