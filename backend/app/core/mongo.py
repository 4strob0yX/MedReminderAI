from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any
import uuid

from pymongo import DESCENDING, MongoClient

from app.core.config import settings

_mongo_client: MongoClient | None = None
_mongo_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="mongo-event")
_reportes_indexes_ready = False


def get_mongo_client() -> MongoClient:
    """Devuelve una instancia compartida (pooled) de MongoClient (soporte dual local / Atlas)."""
    global _mongo_client
    if _mongo_client is None:
        uri = settings.effective_mongo_url
        kwargs: dict[str, Any] = {
            "serverSelectionTimeoutMS": 1200,
            "connectTimeoutMS": 1200,
            "socketTimeoutMS": 1500,
            "maxPoolSize": 16,
        }
        if uri.startswith("mongodb+srv://"):
            try:
                import certifi

                kwargs["tlsCAFile"] = certifi.where()
            except ImportError:
                pass
        _mongo_client = MongoClient(uri, **kwargs)
    return _mongo_client


def _modo_conexion_mongo() -> str:
    return "atlas" if settings.effective_mongo_url.startswith("mongodb+srv://") else "local"


def verificar_mongo_ping() -> None:
    """Lanza excepción si MongoDB no responde al ping."""
    client = get_mongo_client()
    client.admin.command("ping")


def _insert_mongo_doc(documento: dict[str, Any]) -> None:
    try:
        client = get_mongo_client()
        db = client[settings.mongo_db]
        db["eventos_clinicos"].insert_one(documento)
    except Exception:
        pass


def registrar_evento_mongo(
    evento: str,
    id_usuario: int | None = None,
    detalle: dict[str, Any] | None = None,
) -> bool:
    """Registra de forma asíncrona (no bloqueante, 0ms en el hilo HTTP) y tolerante a fallos
    un evento clínico en la colección `eventos_clinicos` de MongoDB."""
    try:
        documento = {
            "evento": evento,
            "id_usuario": id_usuario,
            "detalle": detalle or {},
            "timestamp": datetime.now(timezone.utc),
        }
        _mongo_executor.submit(_insert_mongo_doc, documento)
        return True
    except Exception:
        return False


def _asegurar_indices_reportes_ia(coleccion: Any) -> None:
    """Crea índices únicos y de ordenamiento para reportes IA (Práctica 15)."""
    global _reportes_indexes_ready
    if _reportes_indexes_ready:
        return
    coleccion.create_index("id_analisis", unique=True)
    coleccion.create_index([("fecha_registro_utc", DESCENDING)])
    coleccion.create_index("sistema")
    coleccion.create_index("id_usuario")
    _reportes_indexes_ready = True


def guardar_reporte_ia_mongo(
    reporte: dict[str, Any],
    id_usuario: int | None = None,
    etapa: str = "Etapa 6 - Persistencia Integral P15",
) -> dict[str, Any]:
    """
    Persiste un reporte integral de IA (Predicción + K-Means + PCA + Recomendaciones)
    en la colección `reportes_ia_medreminder` de MongoDB (local o Atlas).
    """
    id_analisis = str(uuid.uuid4())
    fecha_utc = datetime.now(timezone.utc).isoformat()
    documento = {
        "id_analisis": id_analisis,
        "sistema": "MedReminderAI",
        "etapa": etapa,
        "id_usuario": id_usuario,
        "fecha_registro_utc": fecha_utc,
        "datos": reporte,
    }
    modo = _modo_conexion_mongo()
    try:
        client = get_mongo_client()
        coleccion = client[settings.mongo_db][settings.mongo_collection_reportes]
        _asegurar_indices_reportes_ia(coleccion)
        coleccion.insert_one(documento)
        return {
            "guardado": True,
            "modo": modo,
            "id_analisis": id_analisis,
            "coleccion": settings.mongo_collection_reportes,
            "fecha_registro_utc": fecha_utc,
        }
    except Exception as exc:
        return {
            "guardado": False,
            "modo": f"{modo}_offline",
            "id_analisis": id_analisis,
            "coleccion": settings.mongo_collection_reportes,
            "fecha_registro_utc": fecha_utc,
            "detalle": type(exc).__name__,
        }


def consultar_historial_reportes_mongo(
    id_usuario: int | None = None,
    limite: int = 10,
) -> dict[str, Any]:
    """Consulta los últimos reportes integrales de IA almacenados en MongoDB (Práctica 15)."""
    modo = _modo_conexion_mongo()
    filtro: dict[str, Any] = {}
    if id_usuario is not None:
        filtro["id_usuario"] = id_usuario

    try:
        client = get_mongo_client()
        coleccion = client[settings.mongo_db][settings.mongo_collection_reportes]
        cursor = (
            coleccion.find(filtro, {"_id": 0})
            .sort("fecha_registro_utc", DESCENDING)
            .limit(max(1, min(limite, 50)))
        )
        registros = list(cursor)
        return {
            "disponible": True,
            "modo": modo,
            "base_datos": settings.mongo_db,
            "coleccion": settings.mongo_collection_reportes,
            "total": len(registros),
            "registros": registros,
        }
    except Exception as exc:
        return {
            "disponible": False,
            "modo": f"{modo}_offline",
            "base_datos": settings.mongo_db,
            "coleccion": settings.mongo_collection_reportes,
            "total": 0,
            "registros": [],
            "detalle": type(exc).__name__,
        }
