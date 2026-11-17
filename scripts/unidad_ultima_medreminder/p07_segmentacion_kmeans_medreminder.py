"""
PRÁCTICA 07 - MEDREMINDER AI: SEGMENTACIÓN DE PACIENTES MEDIANTE K-MEANS
Incluye las 4 Actividades resueltas en el dominio clínico:
  1. K = 2, 3, 4, 5
  2. Nueva variable clínica 'tomas_puntuales_pct'
  3. Sin escalar vs StandardScaler
  4. Impacto de pacientes atípicos (outliers) en centroides
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler
from _datos_medreminder import FEATURES_CLINICAS, generar_cohorte_segmentacion

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p07"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
SEMILLA = 42

df = generar_cohorte_segmentacion(SEMILLA, incluir_tomas_puntuales=False)
X = df[FEATURES_CLINICAS]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Codo y Silhouette K=2..6
inercias, sils = [], []
ks = list(range(2, 7))
for k in ks:
    km = KMeans(n_clusters=k, n_init=20, random_state=SEMILLA)
    lbl = km.fit_predict(X_scaled)
    inercias.append(round(km.inertia_, 2))
    sils.append(round(silhouette_score(X_scaled, lbl), 4))

km3 = KMeans(n_clusters=3, n_init=20, random_state=SEMILLA)
df["cluster"] = km3.fit_predict(X_scaled)
cent_orig = pd.DataFrame(scaler.inverse_transform(km3.cluster_centers_), columns=FEATURES_CLINICAS)
orden = cent_orig["adherencia_historica_pct"].sort_values().index.tolist()
nombres_perfil = {orden[0]: "Requiere acompañamiento", orden[1]: "Cumplimiento moderado", orden[2]: "Adherencia óptima"}
df["perfil"] = df["cluster"].map(nombres_perfil)
perfiles = df.groupby("perfil")[FEATURES_CLINICAS].mean().round(2)

print("=== PERFILES CLÍNICOS K=3 (MEDREMINDER AI) ===")
print(perfiles)

# Actividad 1: K = 2, 3, 4, 5
act1 = []
for k in [2, 3, 4, 5]:
    km_k = KMeans(n_clusters=k, n_init=20, random_state=SEMILLA)
    lbl_k = km_k.fit_predict(X_scaled)
    act1.append({"k": k, "inercia": round(km_k.inertia_, 2), "silhouette": round(silhouette_score(X_scaled, lbl_k), 4)})
print("\n=== ACTIVIDAD 1 (K=2..5) ===")
print(pd.DataFrame(act1).to_string(index=False))

# Actividad 2: Nueva variable 'tomas_puntuales_pct'
vars_act2 = FEATURES_CLINICAS + ["tomas_puntuales_pct"]
df_act2 = generar_cohorte_segmentacion(SEMILLA, incluir_tomas_puntuales=True)
sc2 = StandardScaler()
X2_s = sc2.fit_transform(df_act2[vars_act2])
km_act2 = KMeans(n_clusters=3, n_init=20, random_state=SEMILLA)
df_act2["cluster"] = km_act2.fit_predict(X2_s)
print(f"\n=== ACTIVIDAD 2 (+tomas_puntuales_pct) ===\nSilhouette 5 vars: {silhouette_score(X2_s, df_act2['cluster']):.4f}")

# Actividad 3: Sin escalar vs StandardScaler
lbl_raw = KMeans(n_clusters=3, n_init=20, random_state=SEMILLA).fit_predict(X)
print("\n=== ACTIVIDAD 3 (SIN ESCALAR vs STANDARDSCALER) ===")
print(f"Silhouette sin escalar: {silhouette_score(X, lbl_raw):.4f} | Con StandardScaler: {sils[1]:.4f}")
print(f"ARI estructural: {adjusted_rand_score(df['cluster'], lbl_raw):.4f}")

# Actividad 4: Outliers clínicos
outliers = pd.DataFrame([
    {"edad": 95, "medicamentos_activos": 12, "adherencia_historica_pct": 10.0, "retraso_promedio_min": 180.0, "tiene_cuidador": 0},
    {"edad": 18, "medicamentos_activos": 10, "adherencia_historica_pct": 15.0, "retraso_promedio_min": 175.0, "tiene_cuidador": 0},
    {"edad": 92, "medicamentos_activos": 1, "adherencia_historica_pct": 100.0, "retraso_promedio_min": 0.0, "tiene_cuidador": 1},
])
df_out = pd.concat([X, outliers], ignore_index=True)
sc_out = StandardScaler()
km_out = KMeans(n_clusters=3, n_init=20, random_state=SEMILLA).fit(sc_out.fit_transform(df_out))
cent_out = pd.DataFrame(sc_out.inverse_transform(km_out.cluster_centers_), columns=FEATURES_CLINICAS)
drift = np.linalg.norm(
    cent_orig.sort_values("adherencia_historica_pct").values - cent_out.sort_values("adherencia_historica_pct").values,
    axis=1,
).round(3)
print("\n=== ACTIVIDAD 4 (DESPLAZAMIENTO DE CENTROIDES POR OUTLIERS) ===")
print("Desplazamientos por perfil:", drift.tolist())

# Exportar
df.to_csv(RESULTADOS_DIR / "p07_pacientes_segmentados_medreminder.csv", index=False, encoding="utf-8")
perfiles.to_csv(RESULTADOS_DIR / "p07_perfiles_medreminder.csv", encoding="utf-8")
df_act2.to_csv(RESULTADOS_DIR / "p07_actividad2_tomas_puntuales_medreminder.csv", index=False, encoding="utf-8")
pd.DataFrame(act1).to_csv(RESULTADOS_DIR / "p07_actividades_resumen_medreminder.csv", index=False, encoding="utf-8")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(ks, inercias, marker="o")
axes[0].set_title("Método del Codo (MedReminder AI)")
axes[0].grid(True, alpha=0.3)
axes[1].plot(ks, sils, marker="s", color="teal")
axes[1].set_title("Silhouette Score (MedReminder AI)")
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p07_codo_y_silhouette_medreminder.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 5))
for cid, nom in nombres_perfil.items():
    sub = df[df["cluster"] == cid]
    plt.scatter(sub["adherencia_historica_pct"], sub["retraso_promedio_min"], label=nom, alpha=0.75)
plt.scatter(cent_orig["adherencia_historica_pct"], cent_orig["retraso_promedio_min"], c="black", marker="X", s=160, label="Centroides")
plt.xlabel("Adherencia histórica (%)")
plt.ylabel("Retraso promedio (min)")
plt.title("Segmentación K-Means Pacientes MedReminder AI")
plt.legend()
plt.tight_layout()
plt.savefig(RESULTADOS_DIR / "p07_segmentacion_medreminder.png", dpi=200)
plt.close()
print(f"Exportados en: {RESULTADOS_DIR}")
