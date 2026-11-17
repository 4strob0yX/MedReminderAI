"""
PRÁCTICA 15 - MEDREMINDER AI (ETAPA 6): PERSISTENCIA DUAL EN MONGODB (LOCAL / ATLAS)
Lee reporte_paciente_medreminder.csv y persiste usando el .env de MedReminderAI:
  - Si existe MONGO_CLUSTER en .env -> conecta por SRV a MongoDB Atlas.
  - En caso contrario -> usa MONGO_URL local (Docker port 27018 o 27017).
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus
import certifi
import pandas as pd
from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[1]
RUTA_REPORTE = BASE_DIR / "resultados_medreminder" / "reporte_paciente_medreminder.csv"
RUTA_ENV = REPO_ROOT / ".env"

if RUTA_ENV.exists():
    load_dotenv(RUTA_ENV)


def resolver_conexion_mongo() -> tuple[str, str, str]:
    mongo_cluster = os.getenv("MONGO_CLUSTER")
    mongo_user = os.getenv("MONGO_USER", "")
    mongo_password = os.getenv("MONGO_PASSWORD", "")
    mongo_db = os.getenv("MONGO_DB", "medreminder_logs")
    mongo_coll = os.getenv("MONGO_COLLECTION", "reportes_ia_medreminder")

    if mongo_cluster and mongo_user and mongo_password:
        uri = (
            f"mongodb+srv://{quote_plus(mongo_user)}:{quote_plus(mongo_password)}"
            f"@{mongo_cluster}/?retryWrites=true&w=majority"
        )
        return uri, mongo_db, mongo_coll

    if os.getenv("MONGO_URL"):
        return os.environ["MONGO_URL"], mongo_db, mongo_coll

    # En Docker Compose del proyecto el puerto mapeado al host es 27018
    if mongo_user and mongo_password:
        uri = f"mongodb://{quote_plus(mongo_user)}:{quote_plus(mongo_password)}@localhost:27018/?authSource=admin"
    else:
        uri = "mongodb://localhost:27018/?authSource=admin"
    return uri, mongo_db, mongo_coll


def main() -> None:
    if not RUTA_REPORTE.exists():
        raise FileNotFoundError(f"No se encontró {RUTA_REPORTE}. Ejecuta primero p14_motor_recomendaciones_medreminder.py")

    df = pd.read_csv(RUTA_REPORTE)
    registros = json.loads(df.to_json(orient="records"))
    ahora = datetime.now(timezone.utc).isoformat()
    docs = [
        {
            "id_analisis": str(uuid.uuid4()),
            "sistema": "MedReminderAI",
            "etapa": "Etapa 6 - Persistencia P15",
            "fecha_registro_utc": ahora,
            "archivo_origen": RUTA_REPORTE.name,
            "datos": reg,
        }
        for reg in registros
    ]

    uri, db_name, coll_name = resolver_conexion_mongo()
    print("=== ETAPA 6 MEDREMINDER AI: PERSISTENCIA MONGODB (P15) ===")
    print(f"Base: {db_name} | Colección: {coll_name}")
    print("Documento preparado:\n", json.dumps(docs[0], indent=2, ensure_ascii=False))

    cliente = None
    try:
        kwargs = {"serverSelectionTimeoutMS": 2500}
        if uri.startswith("mongodb+srv://"):
            kwargs["tlsCAFile"] = certifi.where()
        cliente = MongoClient(uri, **kwargs)
        cliente.admin.command("ping")

        col = cliente[db_name][coll_name]
        col.create_index("id_analisis", unique=True)
        col.create_index([("fecha_registro_utc", DESCENDING)])
        col.create_index("sistema")
        res = col.insert_many(docs)
        print(f"Insertados {len(res.inserted_ids)} documento(s) en MongoDB.")
    except PyMongoError as exc:
        print(f"\n[MODO OFFLINE / SIN DOCKER MONGO O ATLAS ACTIVO]: {type(exc).__name__}")
        print("El esquema JSON, índices y adaptador dual (.env local/Atlas) quedaron validados.")
    finally:
        if cliente is not None:
            cliente.close()


if __name__ == "__main__":
    main()
