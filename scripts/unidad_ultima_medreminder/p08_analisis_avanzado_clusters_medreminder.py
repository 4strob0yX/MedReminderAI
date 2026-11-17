"""
PRÁCTICA 08 - MEDREMINDER AI: ANÁLISIS AVANZADO DE CLÚSTERES DE PACIENTES
Incluye las 7 Actividades resueltas:
  1. K = 2, 3, 4
  2. n_init = 5, 20, 50
  3. Nueva variable 'tomas_puntuales_pct'
  4. PERCENTIL_ATIPICOS = 90, 95, 97.5
  5. StandardScaler vs MinMaxScaler
  6. Estabilidad ARI entre semillas
  7. Pacientes similares en frontera de clústeres
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from _datos_medreminder import FEATURES_CLINICAS, generar_cohorte_segmentacion

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p08"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
SEMILLA = 42

df = generar_cohorte_segmentacion(SEMILLA, incluir_tomas_puntuales=False)
X = df[FEATURES_CLINICAS]
sc_std = StandardScaler()
X_std = sc_std.fit_transform(X)
sc_mm = MinMaxScaler()
X_mm = sc_mm.fit_transform(X)

# Inicializaciones k-means++ vs random
init_rows = []
for method in ["k-means++", "random"]:
    for s in [10, 20, 30, 42, 99]:
        km = KMeans(n_clusters=3, init=method, n_init=1, random_state=s)
        lbl = km.fit_predict(X_std)
        init_rows.append({"inicializacion": method, "semilla": s, "inercia": round(km.inertia_, 3), "silhouette": round(silhouette_score(X_std, lbl), 4)})
pd.DataFrame(init_rows).to_csv(RESULTADOS_DIR / "p08_inicializaciones_medreminder.csv", index=False, encoding="utf-8")

# Escaladores
km_std = KMeans(n_clusters=3, init="k-means++", n_init=20, random_state=SEMILLA)
lbl_std = km_std.fit_predict(X_std)
km_mm = KMeans(n_clusters=3, init="k-means++", n_init=20, random_state=SEMILLA)
lbl_mm = km_mm.fit_predict(X_mm)

df_esc = pd.DataFrame([
    {"escalador": "StandardScaler", "inercia": round(km_std.inertia_, 3), "silhouette": round(silhouette_score(X_std, lbl_std), 4)},
    {"escalador": "MinMaxScaler", "inercia": round(km_mm.inertia_, 3), "silhouette": round(silhouette_score(X_mm, lbl_mm), 4)},
])
df_esc.to_csv(RESULTADOS_DIR / "p08_comparacion_escaladores_medreminder.csv", index=False, encoding="utf-8")

# Estabilidad ARI
semillas = [7, 21, 42, 77, 101]
etq_sem = {s: KMeans(n_clusters=3, init="k-means++", n_init=20, random_state=s).fit_predict(X_std) for s in semillas}
ari_rows = [{"s1": s1, "s2": s2, "ari": round(adjusted_rand_score(etq_sem[s1], etq_sem[s2]), 6)} for i, s1 in enumerate(semillas) for s2 in semillas[i + 1:]]
df_ari = pd.DataFrame(ari_rows)
df_ari.to_csv(RESULTADOS_DIR / "p08_estabilidad_ari_medreminder.csv", index=False, encoding="utf-8")

# Reporte integral y atípicos P95
cent_orig = pd.DataFrame(sc_std.inverse_transform(km_std.cluster_centers_), columns=FEATURES_CLINICAS)
orden = cent_orig["adherencia_historica_pct"].sort_values().index.tolist()
mapa_perfiles = {orden[0]: "Requiere acompañamiento", orden[1]: "Cumplimiento moderado", orden[2]: "Adherencia óptima"}
distancias = np.linalg.norm(X_std - km_std.cluster_centers_[lbl_std], axis=1)
umbral_95 = float(np.percentile(distancias, 95))

reporte = df.copy()
reporte["cluster"] = lbl_std
reporte["perfil"] = reporte["cluster"].map(mapa_perfiles)
reporte["distancia_centroide"] = np.round(distancias, 4)
reporte["posible_atipico"] = reporte["distancia_centroide"] > umbral_95

reporte.to_csv(RESULTADOS_DIR / "p08_reporte_integral_medreminder.csv", index=False, encoding="utf-8")
cent_orig.to_csv(RESULTADOS_DIR / "p08_centroides_medreminder.csv", index=False, encoding="utf-8")
reporte.groupby("perfil")[FEATURES_CLINICAS].mean().round(2).to_csv(RESULTADOS_DIR / "p08_perfiles_medreminder.csv", encoding="utf-8")
reporte[reporte["posible_atipico"]].to_csv(RESULTADOS_DIR / "p08_posibles_atipicos_medreminder.csv", index=False, encoding="utf-8")

# 7 Actividades
print("=== P08 MEDREMINDER AI: ACTIVIDAD 1 (K=2,3,4) ===")
for k in [2, 3, 4]:
    lk = KMeans(n_clusters=k, n_init=20, random_state=SEMILLA).fit_predict(X_std)
    print(f"  K={k} -> Silhouette={silhouette_score(X_std, lk):.4f}")

print("\n=== ACTIVIDAD 2 (n_init=5,20,50) ===")
for ni in [5, 20, 50]:
    km_ni = KMeans(n_clusters=3, n_init=ni, random_state=SEMILLA).fit(X_std)
    print(f"  n_init={ni} -> inercia={km_ni.inertia_:.3f}")

df_5v = generar_cohorte_segmentacion(SEMILLA, incluir_tomas_puntuales=True)
X5_s = StandardScaler().fit_transform(df_5v[FEATURES_CLINICAS + ["tomas_puntuales_pct"]])
l5 = KMeans(n_clusters=3, n_init=20, random_state=SEMILLA).fit_predict(X5_s)
print(f"\n=== ACTIVIDAD 3 (+tomas_puntuales_pct) ===\n  Silhouette 5 vars={silhouette_score(X5_s, l5):.4f}")

print("\n=== ACTIVIDAD 4 (PERCENTIL ATÍPICOS = 90, 95, 97.5) ===")
act4 = []
for p in [90, 95, 97.5]:
    u = float(np.percentile(distancias, p))
    act4.append({"percentil": p, "umbral": round(u, 4), "atipicos": int((distancias > u).sum())})
print(pd.DataFrame(act4).to_string(index=False))

print(f"\n=== ACTIVIDAD 5 y 6 ===\nARI StandardScaler vs MinMaxScaler: {adjusted_rand_score(lbl_std, lbl_mm):.4f}")
print(f"ARI promedio entre semillas: {df_ari['ari'].mean():.4f}")

dist_mat = cdist(X_std, X_std)
dist_mat[lbl_std[:, None] == lbl_std[None, :]] = np.inf
i_min, j_min = np.unravel_index(np.argmin(dist_mat), dist_mat.shape)
print("\n=== ACTIVIDAD 7: PACIENTES FRONTERIZOS SIMILARES EN DISTINTOS CLÚSTERES ===")
print(reporte.iloc[[i_min, j_min]][["id_paciente"] + FEATURES_CLINICAS + ["perfil", "distancia_centroide"]].to_string(index=False))

plt.figure(figsize=(8, 4.5))
plt.hist(distancias, bins=25, color="#0D9488", alpha=0.8)
plt.axvline(umbral_95, color="red", linestyle="--", label=f"P95 = {umbral_95:.2f}")
plt.title("Distancias al centroide - Pacientes MedReminder AI")
plt.xlabel("Distancia estandarizada")
plt.legend()
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p08_distancias_atipicos_medreminder.png", dpi=200)
plt.close()
print(f"Exportados en: {RESULTADOS_DIR}")
