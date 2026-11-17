"""
PRÁCTICA 03 - MEDREMINDER AI: PRIMER MODELO DE MACHINE LEARNING
Comparación: Regla Fija Clínica vs. DecisionTreeClassifier para Riesgo de Abandono.
"""

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from _datos_medreminder import FEATURES_CLINICAS, TARGET_CLINICO, cargar_dataset_clinico

df = cargar_dataset_clinico()
X = df[FEATURES_CLINICAS]
y = df[TARGET_CLINICO].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)


def predecir_regla_clinica(fila: pd.Series) -> int:
    if fila["adherencia_historica_pct"] < 72.0:
        return 1
    if fila["retraso_promedio_min"] > 35.0 and fila["tiene_cuidador"] == 0:
        return 1
    return 0


modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo.fit(X_train, y_train)

pred_regla = X_test.apply(predecir_regla_clinica, axis=1)
pred_ml = modelo.predict(X_test)

print("=== PRÁCTICA 03 MEDREMINDER AI: REGLA FIJA vs ÁRBOL DE DECISIÓN ===")
print(f"Dataset oficial: {len(df)} pacientes | Train: {len(X_train)} | Test: {len(X_test)}")
print(f"Accuracy Regla Fija: {accuracy_score(y_test, pred_regla):.2%}")
print(f"Accuracy Árbol ML:   {accuracy_score(y_test, pred_ml):.2%}")
print("\nReporte de clasificación Árbol ML:")
print(classification_report(y_test, pred_ml, zero_division=0))
print("Matriz de confusión Árbol ML:\n", confusion_matrix(y_test, pred_ml))
print("\nReglas aprendidas por el Árbol:")
print(export_text(modelo, feature_names=FEATURES_CLINICAS))

paciente_nuevo = pd.DataFrame([{
    "edad": 78,
    "medicamentos_activos": 5,
    "adherencia_historica_pct": 74.0,
    "retraso_promedio_min": 32.0,
    "tiene_cuidador": 0,
}])
print("Prueba Don Ramiro (nuevo caso):")
print("  Regla Fija:", "EN RIESGO" if predecir_regla_clinica(paciente_nuevo.iloc[0]) == 1 else "ESTABLE")
print("  Árbol ML:  ", "EN RIESGO" if int(modelo.predict(paciente_nuevo)[0]) == 1 else "ESTABLE")
