from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.mongo import verificar_mongo_ping
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    return {"status": "ok"}


@router.get("/db")
def health_db(db: Session = Depends(get_db)):
    """Verifica conectividad con MySQL (vía pool de SQLAlchemy) y MongoDB (cliente compartido)."""
    status_info = {}

    try:
        db.execute(text("SELECT 1"))
        status_info["mysql"] = "ok"
    except Exception as e:
        status_info["mysql"] = f"error: {type(e).__name__}"

    try:
        verificar_mongo_ping()
        status_info["mongo"] = "ok"
    except Exception as e:
        status_info["mongo"] = f"error: {type(e).__name__}"

    if "error" in "".join(status_info.values()):
        raise HTTPException(status_code=503, detail=status_info)
    return status_info
