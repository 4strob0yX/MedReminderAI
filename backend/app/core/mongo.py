from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from app.core.config import settings

_mongo_client: MongoClient | None = None
_mongo_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="mongo-event")


def get_mongo_client() -> MongoClient:
    """Devuelve una instancia compartida (pooled) de MongoClient."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(
            settings.mongo_url,
            serverSelectionTimeoutMS=1200,
            connectTimeoutMS=1200,
            socketTimeoutMS=1500,
            maxPoolSize=16,
        )
    return _mongo_client


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
