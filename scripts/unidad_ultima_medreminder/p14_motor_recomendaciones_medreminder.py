"""
PRÁCTICA 14 - MEDREMINDER AI (ETAPA 5): MOTOR CLÍNICO INTEGRAL DE RECOMENDACIONES
Integra modelo supervisado + K-Means + PCA y genera resultados_medreminder/reporte_paciente_medreminder.csv.
"""

import argparse
import sys
from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RUTA_RESULTADOS = BASE_DIR / "resultados_medreminder"
RUTA_MODELOS = RUTA_RESULTADOS / "modelos"

ARCHIVO_SUP = RUTA_MODELOS / "modelo_supervisado_medreminder.joblib"
ARCHIVO_KM = RUTA_MODELOS / "modelo_kmeans_medreminder.joblib"
ARCHIVO_PCA = RUTA_MODELOS / "modelo_pca_medreminder.joblib"


def generar_recomendaciones_clinicas(pac: pd.Series, riesgo: int, perfil: str) -> list[str]:
    recs = []
    if pac["edad"] >= 65:
        recs.append("Paciente geriátrico: activar lector de voz TTS y texto grande en MedReminder AI.")
    if pac["medicamentos_activos"] >= 4:
        recs.append("Polifarmacia activa: consolidar ventanas horarias y validar interacciones en botiquín.")
    if pac["adherencia_historica_pct"] < 75:
        recs.append("Adherencia menor al 75%: reforzar alarmas nativas y activar seguimiento diario.")
    else:
        recs.append("Adherencia aceptable: mantener esquema actual de recordatorios y racha de honor.")
    if pac["retraso_promedio_min"] > 30:
        recs.append("Retraso elevado en tomas: revisar horarios críticos y limitar posposiciones.")
    if pac["tiene_cuidador"] == 0:
        recs.append("Sin cuidador vinculado: sugerir vinculación familiar mediante código de 24h.")
    if riesgo == 1:
        recs.append("Predicción supervisada de RIESGO DE ABANDONO: disparar alerta preventiva al cuidador.")
    recs.append(f"Perfil K-Means asignado: {perfil}.")
    return recs


def main() -> None:
    parser = argparse.ArgumentParser(description="Motor de recomendaciones clínicas MedReminder AI (P14)")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--edad", type=float)
    parser.add_argument("--medicamentos", type=float)
    parser.add_argument("--adherencia", type=float)
    parser.add_argument("--retraso", type=float)
    parser.add_argument("--cuidador", type=int)
    args = parser.parse_args()

    for r in [ARCHIVO_SUP, ARCHIVO_KM, ARCHIVO_PCA]:
        if not r.exists():
            raise FileNotFoundError(f"Falta modelo requerido: {r}. Ejecuta p10 -> p13.")

    sup = joblib.load(ARCHIVO_SUP)
    km = joblib.load(ARCHIVO_KM)
    pca = joblib.load(ARCHIVO_PCA)

    if args.demo:
        vals = (76, 5, 64.0, 48.0, 0)
    elif all(v is not None for v in [args.edad, args.medicamentos, args.adherencia, args.retraso, args.cuidador]):
        vals = (args.edad, args.medicamentos, args.adherencia, args.retraso, args.cuidador)
    elif sys.stdin.isatty():
        vals = (
            float(input("Edad del paciente: ")),
            float(input("Medicamentos activos: ")),
            float(input("Adherencia histórica (%): ")),
            float(input("Retraso promedio (min): ")),
            int(input("¿Tiene cuidador? (1=Sí, 0=No): ")),
        )
    else:
        vals = (76, 5, 64.0, 48.0, 0)

    pac_df = pd.DataFrame([{
        "edad": vals[0],
        "medicamentos_activos": vals[1],
        "adherencia_historica_pct": vals[2],
        "retraso_promedio_min": vals[3],
        "tiene_cuidador": vals[4],
    }])

    pred = int(sup["modelo"].predict(pac_df)[0])
    probs = sup["modelo"].predict_proba(pac_df)[0]

    X_km = km["escalador"].transform(pac_df[km["caracteristicas"]])
    cluster_id = int(km["modelo"].predict(X_km)[0])
    perfil_nom = km["mapa_perfiles"].get(cluster_id, f"Cluster {cluster_id}")

    X_pca = pca["escalador"].transform(pac_df[pca["caracteristicas"]])
    coords_pca = pca["modelo_pca"].transform(X_pca)[0]

    recs = generar_recomendaciones_clinicas(pac_df.iloc[0], pred, perfil_nom)
    reporte = {
        "edad": int(vals[0]),
        "medicamentos_activos": int(vals[1]),
        "adherencia_historica_pct": float(vals[2]),
        "retraso_promedio_min": float(vals[3]),
        "tiene_cuidador": int(vals[4]),
        "riesgo_abandono": pred,
        "probabilidad_abandono_pct": round(float(probs[1]) * 100, 2),
        "cluster": cluster_id,
        "perfil": perfil_nom,
        "PC1": round(float(coords_pca[0]), 4),
        "PC2": round(float(coords_pca[1]), 4),
        "recomendaciones": " | ".join(recs),
    }

    destino = RUTA_RESULTADOS / "reporte_paciente_medreminder.csv"
    pd.DataFrame([reporte]).to_csv(destino, index=False, encoding="utf-8")

    print("=== REPORTE INTEGRAL CLÍNICO MEDREMINDER AI (P14) ===")
    for k, v in reporte.items():
        if k != "recomendaciones":
            print(f"  {k}: {v}")
    print("\nRecomendaciones clínicas:")
    for i, r in enumerate(recs, 1):
        print(f"  {i}. {r}")
    print(f"\nExportado en: {destino}")


if __name__ == "__main__":
    main()
