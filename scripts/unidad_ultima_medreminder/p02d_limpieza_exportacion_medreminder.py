"""
PRÁCTICA 2 - PARTE D (MEDREMINDER AI): LIMPIEZA, AUDITORÍA CLÍNICA Y EXPORTACIÓN
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados_p02"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

datos_crudos = {
    "id_paciente": ["PAC-01", "PAC-02", "PAC-03", "PAC-02", "PAC-04", "PAC-05"],
    "edad": [72, 45, 165, 45, None, "setenta"],
    "adherencia_historica_pct": [68.5, 92.0, 135.0, 92.0, 74.0, 81.0],
    "retraso_promedio_min": [42.0, 8.0, 15.0, 8.0, -25.0, None],
}

df = pd.DataFrame(datos_crudos).drop_duplicates().copy()
df["edad_num"] = pd.to_numeric(df["edad"], errors="coerce")


def diagnosticar(fila: pd.Series) -> str:
    motivos = []
    if pd.isna(fila["edad_num"]) or not (0 <= fila["edad_num"] <= 120):
        motivos.append("edad_invalida_o_faltante")
    if pd.isna(fila["adherencia_historica_pct"]) or not (0 <= fila["adherencia_historica_pct"] <= 100):
        motivos.append("adherencia_fuera_de_rango")
    if pd.isna(fila["retraso_promedio_min"]) or fila["retraso_promedio_min"] < 0:
        motivos.append("retraso_negativo_o_faltante")
    return "; ".join(motivos)


df["motivo_revision"] = df.apply(diagnosticar, axis=1)
valido = df["motivo_revision"] == ""

df_validos = df.loc[valido, ["id_paciente", "edad_num", "adherencia_historica_pct", "retraso_promedio_min"]].rename(
    columns={"edad_num": "edad"}
)
df_auditoria = df.loc[~valido, ["id_paciente", "edad", "adherencia_historica_pct", "retraso_promedio_min", "motivo_revision"]]

print("=== REGISTROS CLÍNICOS VÁLIDOS ===")
print(df_validos.to_string(index=False))
print("\n=== BITÁCORA DE AUDITORÍA ===")
print(df_auditoria.to_string(index=False))

df_validos.to_csv(RESULTADOS_DIR / "pacientes_limpios.csv", index=False, encoding="utf-8")
df_auditoria.to_csv(RESULTADOS_DIR / "pacientes_auditoria.csv", index=False, encoding="utf-8")
