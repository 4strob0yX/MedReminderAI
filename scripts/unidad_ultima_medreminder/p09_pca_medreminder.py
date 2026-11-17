"""
PRÁCTICA 09 - MEDREMINDER AI: REDUCCIÓN DE DIMENSIONALIDAD MEDIANTE PCA
Proyección 2D/3D de las 5 variables clínicas, varianza explicada, cargas y error de reconstrucción.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from _datos_medreminder import FEATURES_CLINICAS, generar_cohorte_segmentacion

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p09"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
SEMILLA = 42

ruta_p08 = BASE_DIR / "resultados_p08" / "p08_reporte_integral_medreminder.csv"
df = pd.read_csv(ruta_p08) if ruta_p08.exists() else generar_cohorte_segmentacion(SEMILLA)

X_scaled = StandardScaler().fit_transform(df[FEATURES_CLINICAS])
if "cluster" not in df.columns:
    df["cluster"] = KMeans(n_clusters=3, n_init=20, random_state=SEMILLA).fit_predict(X_scaled)

pca = PCA(n_components=len(FEATURES_CLINICAS), random_state=SEMILLA)
coords = pca.fit_transform(X_scaled)

var_ind = pca.explained_variance_ratio_
var_acum = np.cumsum(var_ind)
tabla_var = pd.DataFrame({
    "componente": [f"PC{i}" for i in range(1, len(FEATURES_CLINICAS) + 1)],
    "varianza_explicada_pct": np.round(var_ind * 100, 2),
    "varianza_acumulada_pct": np.round(var_acum * 100, 2),
})

cargas = pd.DataFrame(np.round(pca.components_, 4), index=tabla_var["componente"], columns=FEATURES_CLINICAS)
X_recons = coords[:, :2] @ pca.components_[:2, :]
err_mse = mean_squared_error(X_scaled, X_recons)

print("=== PCA MEDREMINDER AI (P09) ===")
print(tabla_var.to_string(index=False))
print("\nCargas de componentes:\n", cargas)
print(f"\nError reconstrucción 2D (MSE): {err_mse:.6f}")

tabla_var.to_csv(RESULTADOS_DIR / "p09_varianza_pca_medreminder.csv", index=False, encoding="utf-8")
cargas.to_csv(RESULTADOS_DIR / "p09_cargas_pca_medreminder.csv", encoding="utf-8")

df_coords = df[["id_paciente", "cluster"]].copy()
df_coords["PC1"] = np.round(coords[:, 0], 4)
df_coords["PC2"] = np.round(coords[:, 1], 4)
df_coords["PC3"] = np.round(coords[:, 2], 4)
df_coords.to_csv(RESULTADOS_DIR / "p09_coordenadas_pca_medreminder.csv", index=False, encoding="utf-8")

plt.figure(figsize=(7, 5))
for cid in sorted(df["cluster"].unique()):
    m = df["cluster"] == cid
    etq = df.loc[m, "perfil"].iloc[0] if "perfil" in df.columns else f"Cluster {cid}"
    plt.scatter(coords[m, 0], coords[m, 1], label=etq, alpha=0.75)
plt.xlabel(f"PC1 ({var_ind[0]*100:.1f}%)")
plt.ylabel(f"PC2 ({var_ind[1]*100:.1f}%)")
plt.title("Proyección PCA 2D - Pacientes MedReminder AI")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p09_pca_2d_medreminder.png", dpi=200)
plt.close()
print(f"Exportados en: {RESULTADOS_DIR}")
