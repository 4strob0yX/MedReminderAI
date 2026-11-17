"""
Utilidad compartida para cargar el dataset clínico oficial de MedReminder AI
(backend/app/data/dataset_entrenamiento_pacientes.csv) o generar una cohorte
clínica reproducible con perfiles de adherencia para prácticas no supervisadas.
"""

from pathlib import Path
import numpy as np
import pandas as pd

FEATURES_CLINICAS = [
    "edad",
    "medicamentos_activos",
    "adherencia_historica_pct",
    "retraso_promedio_min",
    "tiene_cuidador",
]

TARGET_CLINICO = "riesgo_abandono"


def obtener_ruta_dataset_oficial() -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    ruta_backend = repo_root / "backend" / "app" / "data" / "dataset_entrenamiento_pacientes.csv"
    if ruta_backend.exists():
        return ruta_backend
    ruta_scripts = repo_root / "scripts" / "dataset_entrenamiento_pacientes.csv"
    if ruta_scripts.exists():
        return ruta_scripts
    raise FileNotFoundError("No se encontró dataset_entrenamiento_pacientes.csv en backend/app/data ni scripts/.")


def cargar_dataset_clinico() -> pd.DataFrame:
    return pd.read_csv(obtener_ruta_dataset_oficial())


def generar_cohorte_segmentacion(
    semilla: int = 42,
    incluir_tomas_puntuales: bool = False,
) -> pd.DataFrame:
    """
    Genera 450 pacientes clínicos simulados en 3 perfiles naturales de adherencia
    (Óptima, Moderada y Crítica) para K-Means, análisis de clústeres y PCA.
    """
    rng = np.random.default_rng(semilla)

    # Perfil 1 (160): Adherencia Óptima (adultos jóvenes/medios, pocos fármacos, alta adherencia, poco retraso)
    optimo = np.column_stack([
        rng.normal(42, 10, 160),
        rng.normal(2.0, 0.8, 160),
        rng.normal(93, 4, 160),
        rng.normal(9, 5, 160),
        rng.choice([0, 1], 160, p=[0.35, 0.65]),
    ])
    # Perfil 2 (155): Cumplimiento Moderado (posposición ocasional, polifarmacia media)
    moderado = np.column_stack([
        rng.normal(60, 9, 155),
        rng.normal(4.0, 1.0, 155),
        rng.normal(76, 6, 155),
        rng.normal(32, 9, 155),
        rng.choice([0, 1], 155, p=[0.45, 0.55]),
    ])
    # Perfil 3 (135): Riesgo Crítico / Requiere Acompañamiento (geriátrico, alta polifarmacia, baja adherencia, retrasos)
    critico = np.column_stack([
        rng.normal(76, 7, 135),
        rng.normal(6.5, 1.2, 135),
        rng.normal(52, 8, 135),
        rng.normal(72, 14, 135),
        rng.choice([0, 1], 135, p=[0.70, 0.30]),
    ])

    datos = np.vstack([optimo, moderado, critico])
    cols = list(FEATURES_CLINICAS)

    if incluir_tomas_puntuales:
        tp = np.concatenate([
            rng.normal(94, 4, 160),
            rng.normal(71, 8, 155),
            rng.normal(42, 11, 135),
        ])
        datos = np.column_stack([datos, tp])
        cols.append("tomas_puntuales_pct")

    rng.shuffle(datos)
    df = pd.DataFrame(datos, columns=cols)
    df["edad"] = df["edad"].clip(18, 95).round(0).astype(int)
    df["medicamentos_activos"] = df["medicamentos_activos"].clip(1, 10).round(0).astype(int)
    df["adherencia_historica_pct"] = df["adherencia_historica_pct"].clip(25, 100).round(1)
    df["retraso_promedio_min"] = df["retraso_promedio_min"].clip(0, 120).round(1)
    df["tiene_cuidador"] = df["tiene_cuidador"].round(0).astype(int)
    if incluir_tomas_puntuales:
        df["tomas_puntuales_pct"] = df["tomas_puntuales_pct"].clip(10, 100).round(1)
    df.insert(0, "id_paciente", [f"PAC-{i:04d}" for i in range(1, len(df) + 1)])
    return df
