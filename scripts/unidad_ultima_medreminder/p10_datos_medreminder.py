"""
PRÁCTICA 10 - MEDREMINDER AI (ETAPA 1): PREPARACIÓN DEL DATASET CLÍNICO INTEGRADO
Exporta backend/app/data/dataset_entrenamiento_pacientes.csv a resultados_medreminder/medreminder_datos.csv.
"""

from pathlib import Path
from _datos_medreminder import TARGET_CLINICO, cargar_dataset_clinico

BASE_DIR = Path(__file__).resolve().parent
RUTA_RESULTADOS = BASE_DIR / "resultados_medreminder"
RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)


def main() -> None:
    df = cargar_dataset_clinico()
    print("=== ETAPA 1 MEDREMINDER AI: DATASET CLÍNICO ===")
    print(df.head().to_string(index=False))
    print("\nDistribución de riesgo_abandono:")
    print(df[TARGET_CLINICO].value_counts().sort_index())

    destino = RUTA_RESULTADOS / "medreminder_datos.csv"
    df.to_csv(destino, index=False, encoding="utf-8")
    print(f"\nDataset preparado en: {destino}")


if __name__ == "__main__":
    main()
