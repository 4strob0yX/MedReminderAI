from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from app.core.config import settings

_mongo_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    """Devuelve una instancia compartida (pooled) de MongoClient."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(
            settings.mongo_url,
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000,
            socketTimeoutMS=2000,
        )
    return _mongo_client


def verificar_mongo_ping() -> None:
    """Lanza excepción si MongoDB no responde al ping."""
    client = get_mongo_client()
    client.admin.command("ping")


def registrar_evento_mongo(
    evento: str,
    id_usuario: int | None = None,
    detalle: dict[str, Any] | None = None,
) -> bool:
    """Registra de forma no bloqueante y tolerante a fallos un evento clínico
    en la colección `eventos_clinicos` de MongoDB (`medicamento_creado`,
    `toma_confirmada`, `toma_pospuesta`, `toma_omitida`, `castigo_activado`,
    `alerta_alergia`, etc.). Nunca propaga errores a la petición HTTP."""
    try:
        client = get_mongo_client()
        db = client[settings.mongo_db]
        documento = {
            "evento": evento,
            "id_usuario": id_usuario,
            "detalle": detalle or {},
            "timestamp": datetime.now(timezone.utc),
        }
        db["eventos_clinicos"].insert_one(documento)
        return True
    except Exception:
        return False
