import os

import pymysql
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    return {"status": "ok"}


@router.get("/db")
def health_db():
    """Verifica conectividad con MySQL y MongoDB."""
    status = {}

    try:
        conn = pymysql.connect(
            host=os.environ["MYSQL_HOST"],
            port=int(os.environ["MYSQL_PORT"]),
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            connect_timeout=3,
        )
        conn.ping()
        conn.close()
        status["mysql"] = "ok"
    except Exception as e:
        status["mysql"] = f"error: {type(e).__name__}"

    try:
        client = MongoClient(os.environ["MONGO_URL"], serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        client.close()
        status["mongo"] = "ok"
    except Exception as e:
        status["mongo"] = f"error: {type(e).__name__}"

    if "error" in "".join(status.values()):
        raise HTTPException(status_code=503, detail=status)
    return status
