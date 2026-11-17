import os

os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "3306")
os.environ.setdefault("MYSQL_DATABASE", "medreminder")
os.environ.setdefault("MYSQL_USER", "med_user")
os.environ.setdefault("MYSQL_PASSWORD", "med_pass")
os.environ.setdefault("JWT_SECRET", "clave_secreta_de_pruebas_con_mas_de_32_caracteres")

from app.core.config import Settings
from app.services.ml_analytics_service import (
    ejecutar_optimizacion_hiperparametros_p06,
    evaluar_perfil_integral_paciente,
    obtener_resumen_segmentacion_pca,
)


def test_config_dual_mongo_uri():
    local_cfg = Settings(
        mysql_host="localhost",
        mysql_port=3306,
        mysql_database="db",
        mysql_user="u",
        mysql_password="p",
        jwt_secret="x" * 32,
        mongo_url="mongodb://localhost:27017/?authSource=admin",
    )
    assert local_cfg.effective_mongo_url.startswith("mongodb://localhost:27017")

    atlas_cfg = Settings(
        mysql_host="localhost",
        mysql_port=3306,
        mysql_database="db",
        mysql_user="u",
        mysql_password="p",
        jwt_secret="x" * 32,
        mongo_cluster="cluster0.example.mongodb.net",
        mongo_user="admin_user",
        mongo_password="pass@word",
    )
    assert atlas_cfg.effective_mongo_url.startswith("mongodb+srv://admin_user:pass%40word@cluster0.example.mongodb.net")


def test_optimizacion_hiperparametros_p06():
    res = ejecutar_optimizacion_hiperparametros_p06()
    assert res["algoritmo_ganador"] in ("decision_tree", "random_forest", "knn")
    assert len(res["comparativa_metodos"]) == 3
    assert res["metricas_prueba"]["f1_score_pct"] > 50.0


def test_segmentacion_kmeans_y_pca():
    res = obtener_resumen_segmentacion_pca()
    assert res["total_pacientes_cohorte"] == 150
    assert len(res["perfiles_kmeans"]) == 3
    assert len(res["evaluacion_k"]) == 4
    assert res["estabilidad_ari"]["ari_promedio"] >= 0.0
    assert len(res["puntos_proyectados"]) == 150
    assert "PC1" in res["pca_varianza_explicada_pct"]
    assert "PC2" in res["pca_varianza_explicada_pct"]


def test_evaluar_perfil_integral_p10_p15():
    res = evaluar_perfil_integral_paciente(
        edad=78,
        medicamentos_activos=5,
        adherencia_historica_pct=62.0,
        retraso_promedio_min=45.0,
        tiene_cuidador=0,
        algoritmo="random_forest",
        persistir_mongo=False,
    )
    assert res["prediccion"]["riesgo_abandono"] is True
    assert res["perfil_kmeans"] in ("Requiere acompañamiento", "Cumplimiento moderado", "Adherencia óptima")
    assert isinstance(res["pc1"], float) and isinstance(res["pc2"], float)
    assert len(res["recomendaciones_motor"]) == 6
    assert res["persistencia_mongo"]["modo"] == "omitido"
