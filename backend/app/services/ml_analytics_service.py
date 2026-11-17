"""
Servicios analíticos de IA Clínica para MedReminder AI (Prácticas 06 a 15):
  - P06: Optimización de hiperparámetros (GridSearchCV vs RandomizedSearchCV)
  - P07/P08/P12: Segmentación no supervisada K-Means, escaladores, ARI y detección de atípicos P95
  - P09/P13: Reducción de dimensionalidad PCA (varianza explicada, cargas y proyección 2D)
  - P10/P14: Motor integral de recomendaciones clínicas
  - P15: Persistencia estructurada en MongoDB (local o Atlas)
"""

import time
from typing import Any

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    adjusted_rand_score,
    f1_score,
    mean_squared_error,
    precision_score,
    recall_score,
    silhouette_score,
)
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from app.core.mongo import guardar_reporte_ia_mongo
from app.services.ml_risk_service import _cargar_o_generar_dataset, predecir_adherencia_ml

_CACHE_OPT_P06: dict[str, Any] | None = None
_CACHE_CLUSTER_PCA: dict[str, Any] | None = None


def ejecutar_optimizacion_hiperparametros_p06() -> dict[str, Any]:
    """
    Práctica 06: Ejecuta GridSearchCV y RandomizedSearchCV con StratifiedKFold(5)
    sobre Decision Tree, Random Forest y KNN en el dataset clínico de MedReminder AI.
    """
    global _CACHE_OPT_P06
    if _CACHE_OPT_P06 is not None:
        return _CACHE_OPT_P06

    X, y, _features, _ = _cargar_o_generar_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    config_grid = {
        "decision_tree": (
            "Decision Tree",
            DecisionTreeClassifier(random_state=42),
            {"max_depth": [3, 5, 8, None], "min_samples_split": [2, 5, 10], "criterion": ["gini", "entropy"]},
        ),
        "random_forest": (
            "Random Forest",
            RandomForestClassifier(random_state=42),
            {"n_estimators": [50, 100, 150], "max_depth": [3, 5, 8, None], "min_samples_split": [2, 5]},
        ),
        "knn": (
            "K-Nearest Neighbors",
            Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier())]),
            {"knn__n_neighbors": [3, 5, 7, 9], "knn__weights": ["uniform", "distance"], "knn__metric": ["euclidean", "manhattan"]},
        ),
    }

    config_rand = {
        "decision_tree": {
            "max_depth": [2, 3, 4, 5, 6, 8, None],
            "min_samples_split": [2, 4, 6, 10],
            "min_samples_leaf": [1, 2, 4],
            "criterion": ["gini", "entropy"],
        },
        "random_forest": {
            "n_estimators": [40, 60, 100, 140, 200],
            "max_depth": [3, 4, 5, 7, None],
            "min_samples_split": [2, 4, 8],
            "min_samples_leaf": [1, 2, 4],
        },
        "knn": {
            "knn__n_neighbors": [3, 5, 7, 9, 11, 13],
            "knn__weights": ["uniform", "distance"],
            "knn__metric": ["euclidean", "manhattan"],
        },
    }

    comparativa = []
    mejores_estimadores: dict[str, Any] = {}
    mejor_clave = "random_forest"
    mejor_f1_cv = -1.0
    mejores_params_ganador: dict[str, Any] = {}

    for clave, (nombre, estimador, grid_params) in config_grid.items():
        t0 = time.perf_counter()
        gs = GridSearchCV(estimador, param_grid=grid_params, scoring="f1", cv=cv, n_jobs=1)
        gs.fit(X_train, y_train)
        t_grid = round(time.perf_counter() - t0, 3)

        t1 = time.perf_counter()
        rs = RandomizedSearchCV(
            estimador,
            param_distributions=config_rand[clave],
            n_iter=10,
            scoring="f1",
            cv=cv,
            random_state=42,
            n_jobs=1,
        )
        rs.fit(X_train, y_train)
        t_rand = round(time.perf_counter() - t1, 3)

        mejores_estimadores[clave] = gs.best_estimator_
        f1_grid_pct = round(float(gs.best_score_) * 100, 2)
        f1_rand_pct = round(float(rs.best_score_) * 100, 2)

        if float(gs.best_score_) > mejor_f1_cv:
            mejor_f1_cv = float(gs.best_score_)
            mejor_clave = clave
            mejores_params_ganador = {k: str(v) for k, v in gs.best_params_.items()}

        comparativa.append({
            "clave": clave,
            "algoritmo": nombre,
            "grid_f1_cv_pct": f1_grid_pct,
            "grid_tiempo_seg": t_grid,
            "grid_params": {k: str(v) for k, v in gs.best_params_.items()},
            "random_f1_cv_pct": f1_rand_pct,
            "random_tiempo_seg": t_rand,
            "random_params": {k: str(v) for k, v in rs.best_params_.items()},
        })

    modelo_ganador = mejores_estimadores[mejor_clave]
    y_pred_test = modelo_ganador.predict(X_test)

    _CACHE_OPT_P06 = {
        "algoritmo_ganador": mejor_clave,
        "algoritmo_ganador_nombre": next(c["algoritmo"] for c in comparativa if c["clave"] == mejor_clave),
        "hiperparametros_optimos": mejores_params_ganador,
        "f1_cv_ganador_pct": round(mejor_f1_cv * 100, 2),
        "metricas_prueba": {
            "accuracy_pct": round(float(accuracy_score(y_test, y_pred_test)) * 100, 2),
            "precision_pct": round(float(precision_score(y_test, y_pred_test, zero_division=0)) * 100, 2),
            "recall_pct": round(float(recall_score(y_test, y_pred_test, zero_division=0)) * 100, 2),
            "f1_score_pct": round(float(f1_score(y_test, y_pred_test, zero_division=0)) * 100, 2),
        },
        "comparativa_metodos": comparativa,
        "estrategia_cv": "StratifiedKFold (n_splits=5, shuffle=True, random_state=42)",
    }
    return _CACHE_OPT_P06


def inicializar_analitica_no_supervisada() -> dict[str, Any]:
    """
    Prácticas 07, 08, 09, 12 y 13: Entrena K-Means (K=3) + análisis de estabilidad ARI,
    comparativa de inicializaciones y escaladores, detección de atípicos P95 y PCA 2D.
    """
    global _CACHE_CLUSTER_PCA
    if _CACHE_CLUSTER_PCA is not None:
        return _CACHE_CLUSTER_PCA

    X, _y, features, meta_info = _cargar_o_generar_dataset()
    scaler_std = StandardScaler()
    X_std = scaler_std.fit_transform(X)

    scaler_mm = MinMaxScaler()
    X_mm = scaler_mm.fit_transform(X)

    # P07/P12: Barrido K=2..5 (Codo + Silhouette)
    evaluacion_k = []
    for k in range(2, 6):
        km_k = KMeans(n_clusters=k, init="k-means++", n_init=20, random_state=42)
        lbl_k = km_k.fit_predict(X_std)
        evaluacion_k.append({
            "k": k,
            "inercia": round(float(km_k.inertia_), 2),
            "silhouette": round(float(silhouette_score(X_std, lbl_k)), 4),
        })

    # P08: Comparativa k-means++ vs random
    comparativa_init = []
    for method in ["k-means++", "random"]:
        inercias, sils = [], []
        for s in [10, 20, 42]:
            km_i = KMeans(n_clusters=3, init=method, n_init=1, random_state=s)
            li = km_i.fit_predict(X_std)
            inercias.append(float(km_i.inertia_))
            sils.append(float(silhouette_score(X_std, li)))
        comparativa_init.append({
            "metodo": method,
            "inercia_promedio": round(float(np.mean(inercias)), 2),
            "silhouette_promedio": round(float(np.mean(sils)), 4),
        })

    # P08: Comparativa StandardScaler vs MinMaxScaler
    km_std = KMeans(n_clusters=3, init="k-means++", n_init=20, random_state=42)
    lbl_std = km_std.fit_predict(X_std)
    km_mm = KMeans(n_clusters=3, init="k-means++", n_init=20, random_state=42)
    lbl_mm = km_mm.fit_predict(X_mm)

    comparativa_escaladores = [
        {
            "escalador": "StandardScaler",
            "inercia": round(float(km_std.inertia_), 2),
            "silhouette": round(float(silhouette_score(X_std, lbl_std)), 4),
        },
        {
            "escalador": "MinMaxScaler",
            "inercia": round(float(km_mm.inertia_), 2),
            "silhouette": round(float(silhouette_score(X_mm, lbl_mm)), 4),
        },
    ]

    # P08: Estabilidad ARI entre semillas
    semillas = [7, 21, 42, 77]
    lbls_sem = [KMeans(n_clusters=3, init="k-means++", n_init=20, random_state=s).fit_predict(X_std) for s in semillas]
    aris = [
        float(adjusted_rand_score(lbls_sem[i], lbls_sem[j]))
        for i in range(len(semillas))
        for j in range(i + 1, len(semillas))
    ]
    estabilidad_ari = {
        "ari_promedio": round(float(np.mean(aris)), 4),
        "ari_minimo": round(float(np.min(aris)), 4),
        "ari_maximo": round(float(np.max(aris)), 4),
    }

    # Etiquetado descriptivo ordenado por adherencia_historica_pct (índice 2)
    centroides_orig = scaler_std.inverse_transform(km_std.cluster_centers_)
    orden = np.argsort(centroides_orig[:, 2]).tolist()
    nombres_canonicos = ["Requiere acompañamiento", "Cumplimiento moderado", "Adherencia óptima"]
    mapa_perfiles = {int(cid): nombres_canonicos[pos] for pos, cid in enumerate(orden)}

    # P08: Detección de posibles pacientes atípicos (Percentil 95)
    distancias = np.linalg.norm(X_std - km_std.cluster_centers_[lbl_std], axis=1)
    umbral_p95 = float(np.percentile(distancias, 95))
    atipicos_mask = distancias > umbral_p95

    perfiles_resumen = []
    for cid in orden:
        mask = lbl_std == cid
        medios = X[mask].mean(axis=0)
        perfiles_resumen.append({
            "cluster": int(cid),
            "perfil": mapa_perfiles[int(cid)],
            "total_pacientes": int(mask.sum()),
            "edad_promedio": round(float(medios[0]), 1),
            "medicamentos_promedio": round(float(medios[1]), 1),
            "adherencia_promedio_pct": round(float(medios[2]), 1),
            "retraso_promedio_min": round(float(medios[3]), 1),
            "proporcion_cuidador_pct": round(float(medios[4]) * 100, 1),
        })

    # P09 / P13: PCA 2D reutilizando el mismo StandardScaler
    pca = PCA(n_components=2, random_state=42)
    coords_2d = pca.fit_transform(X_std)
    var_ind = pca.explained_variance_ratio_
    var_acum = float(np.sum(var_ind))
    X_recons = coords_2d @ pca.components_
    error_mse = float(mean_squared_error(X_std, X_recons))

    cargas = {
        f"PC{i + 1}": {
            feat: round(float(pca.components_[i, j]), 4)
            for j, feat in enumerate(features)
        }
        for i in range(2)
    }

    puntos_proyectados = [
        {
            "id_paciente": f"PAC-{1001 + i}",
            "pc1": round(float(coords_2d[i, 0]), 3),
            "pc2": round(float(coords_2d[i, 1]), 3),
            "cluster": int(lbl_std[i]),
            "perfil": mapa_perfiles[int(lbl_std[i])],
            "atipico": bool(atipicos_mask[i]),
        }
        for i in range(len(X))
    ]

    _CACHE_CLUSTER_PCA = {
        "scaler": scaler_std,
        "kmeans": km_std,
        "pca": pca,
        "features": features,
        "mapa_perfiles": mapa_perfiles,
        "umbral_p95": umbral_p95,
        "resumen_publico": {
            "total_pacientes_cohorte": int(len(X)),
            "evaluacion_k": evaluacion_k,
            "comparativa_inicializaciones": comparativa_init,
            "comparativa_escaladores": comparativa_escaladores,
            "estabilidad_ari": estabilidad_ari,
            "umbral_atipicos_p95": round(umbral_p95, 4),
            "total_atipicos_detectados": int(atipicos_mask.sum()),
            "perfiles_kmeans": perfiles_resumen,
            "pca_varianza_explicada_pct": {
                "PC1": round(float(var_ind[0]) * 100, 2),
                "PC2": round(float(var_ind[1]) * 100, 2),
                "acumulada": round(var_acum * 100, 2),
            },
            "pca_error_reconstruccion_mse": round(error_mse, 4),
            "pca_cargas": cargas,
            "puntos_proyectados": puntos_proyectados,
        },
    }
    return _CACHE_CLUSTER_PCA


def obtener_resumen_segmentacion_pca() -> dict[str, Any]:
    """Devuelve los resultados públicos de K-Means (P07/P08/P12) y PCA (P09/P13)."""
    return inicializar_analitica_no_supervisada()["resumen_publico"]


def _generar_recomendaciones_motor_p14(
    edad: int,
    medicamentos_activos: int,
    adherencia_historica_pct: float,
    retraso_promedio_min: float,
    tiene_cuidador: int,
    riesgo_abandono: bool,
    perfil_kmeans: str,
    es_atipico: bool,
) -> list[str]:
    """Motor clínico de 6 reglas (Práctica 14) adaptado al dominio MedReminder AI."""
    recs = []
    if edad >= 65:
        recs.append("Regla 1 (Edad geriátrica): Activar lector de voz TTS y modo de texto grande.")
    else:
        recs.append("Regla 1 (Edad): Mantener interfaz estándar y recordatorios por horario.")

    if medicamentos_activos >= 4:
        recs.append(f"Regla 2 (Polifarmacia: {medicamentos_activos} fármacos): Agrupar tomas y vigilar interacciones.")
    else:
        recs.append("Regla 2 (Carga farmacológica): Esquema terapéutico manejable.")

    if adherencia_historica_pct < 75.0:
        recs.append(f"Regla 3 (Adherencia {adherencia_historica_pct:.1f}%): Reforzar alarmas críticas diarias.")
    else:
        recs.append(f"Regla 3 (Adherencia {adherencia_historica_pct:.1f}%): Mantener racha de honor y metas.")

    if retraso_promedio_min > 30.0:
        recs.append(f"Regla 4 (Retraso {retraso_promedio_min:.1f} min): Ajustar horarios de notificación anticipada.")
    else:
        recs.append("Regla 4 (Puntualidad): Ventana de respuesta dentro de rango clínico aceptable.")

    if tiene_cuidador == 0 and (riesgo_abandono or edad >= 65):
        recs.append("Regla 5 (Red de apoyo): Vincular a un familiar/cuidador mediante código de 24h.")
    elif tiene_cuidador == 1:
        recs.append("Regla 5 (Red de apoyo): Mantener alertas activas al cuidador vinculado.")
    else:
        recs.append("Regla 5 (Red de apoyo): Opcional agregar contacto de emergencia.")

    aviso_atipico = " (Caso atípico > P95: requiere revisión personalizada)" if es_atipico else ""
    recs.append(f"Regla 6 (Perfil K-Means): Segmento '{perfil_kmeans}'{aviso_atipico}.")
    return recs


def evaluar_perfil_integral_paciente(
    edad: int,
    medicamentos_activos: int,
    adherencia_historica_pct: float,
    retraso_promedio_min: float,
    tiene_cuidador: int,
    algoritmo: str = "random_forest",
    id_usuario: int | None = None,
    nombre_paciente: str = "Paciente",
    persistir_mongo: bool = True,
) -> dict[str, Any]:
    """
    Prácticas 10 a 15 integradas:
      1. Predicción supervisada (P05/P06/P11)
      2. Segmentación K-Means + distancia al centroide + atípico P95 (P07/P08/P12)
      3. Proyección PCA 2D (P09/P13)
      4. Motor de 6 reglas clínicas (P14)
      5. Persistencia dual en MongoDB (P15)
    """
    bundle = inicializar_analitica_no_supervisada()
    pred = predecir_adherencia_ml(
        edad=edad,
        medicamentos_activos=medicamentos_activos,
        adherencia_historica_pct=adherencia_historica_pct,
        retraso_promedio_min=retraso_promedio_min,
        tiene_cuidador=tiene_cuidador,
        algoritmo=algoritmo,
    )

    x_raw = np.array([[edad, medicamentos_activos, adherencia_historica_pct, retraso_promedio_min, tiene_cuidador]], dtype=float)
    x_scaled = bundle["scaler"].transform(x_raw)

    kmeans = bundle["kmeans"]
    cluster_id = int(kmeans.predict(x_scaled)[0])
    perfil_nom = bundle["mapa_perfiles"][cluster_id]
    distancia = float(np.linalg.norm(x_scaled[0] - kmeans.cluster_centers_[cluster_id]))
    es_atipico = bool(distancia > bundle["umbral_p95"])

    coords_pca = bundle["pca"].transform(x_scaled)[0]
    pc1 = round(float(coords_pca[0]), 4)
    pc2 = round(float(coords_pca[1]), 4)

    recs = _generar_recomendaciones_motor_p14(
        edad=edad,
        medicamentos_activos=medicamentos_activos,
        adherencia_historica_pct=adherencia_historica_pct,
        retraso_promedio_min=retraso_promedio_min,
        tiene_cuidador=tiene_cuidador,
        riesgo_abandono=pred["riesgo_abandono"],
        perfil_kmeans=perfil_nom,
        es_atipico=es_atipico,
    )

    datos_reporte = {
        "nombre_paciente": nombre_paciente,
        "edad": edad,
        "medicamentos_activos": medicamentos_activos,
        "adherencia_historica_pct": round(adherencia_historica_pct, 1),
        "retraso_promedio_min": round(retraso_promedio_min, 1),
        "tiene_cuidador": tiene_cuidador,
        "prediccion": pred,
        "cluster_kmeans": cluster_id,
        "perfil_kmeans": perfil_nom,
        "distancia_centroide": round(distancia, 4),
        "umbral_atipico_p95": round(bundle["umbral_p95"], 4),
        "es_atipico": es_atipico,
        "pc1": pc1,
        "pc2": pc2,
        "recomendaciones_motor": recs,
    }

    if persistir_mongo:
        persistencia = guardar_reporte_ia_mongo(datos_reporte, id_usuario=id_usuario)
    else:
        persistencia = {"guardado": False, "modo": "omitido", "id_analisis": "", "coleccion": "", "fecha_registro_utc": ""}

    return {
        "paciente_id": id_usuario or 0,
        "nombre_paciente": nombre_paciente,
        "datos_clinicos_extraidos": {
            "edad": edad,
            "medicamentos_activos": medicamentos_activos,
            "adherencia_historica_pct": round(adherencia_historica_pct, 1),
            "retraso_promedio_min": round(retraso_promedio_min, 1),
            "tiene_cuidador": tiene_cuidador,
        },
        "prediccion": pred,
        "cluster_kmeans": cluster_id,
        "perfil_kmeans": perfil_nom,
        "distancia_centroide": round(distancia, 4),
        "umbral_atipico_p95": round(bundle["umbral_p95"], 4),
        "es_atipico": es_atipico,
        "pc1": pc1,
        "pc2": pc2,
        "recomendaciones_motor": recs,
        "persistencia_mongo": persistencia,
    }
