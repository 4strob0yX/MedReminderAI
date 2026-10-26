from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routers import (
    ai,
    alergias,
    auth,
    contactos,
    health,
    medicamentos,
    recordatorios,
    tratamientos,
)
from app.db.session import engine

COLUMNAS_MEDICAMENTO_MIGRACION: list[tuple[str, str]] = [
    ("stock_inicial", "INT NOT NULL DEFAULT 30"),
    ("forma_farmaceutica", "VARCHAR(40) NOT NULL DEFAULT 'comprimidos'"),
    ("color_pastilla", "VARCHAR(40) NOT NULL DEFAULT 'blanco'"),
    ("instrucciones_toma", "VARCHAR(255) NULL"),
    ("proposito", "VARCHAR(120) NULL"),
]


def asegurar_esquema_mysql() -> None:
    """Garantiza que las nuevas columnas de `medicamento` existan aunque el volumen
    de MySQL haya sido inicializado previamente con una versión anterior del DDL."""
    try:
        with engine.begin() as conn:
            filas = conn.execute(
                text(
                    "SELECT LOWER(column_name) FROM information_schema.columns "
                    "WHERE table_schema = DATABASE() AND table_name = 'medicamento'"
                )
            ).all()
            existentes = {fila[0] for fila in filas}
            if not existentes:
                return
            for col_name, col_ddl in COLUMNAS_MEDICAMENTO_MIGRACION:
                if col_name.lower() not in existentes:
                    conn.execute(
                        text(f"ALTER TABLE medicamento ADD COLUMN {col_name} {col_ddl}")
                    )
                    if col_name == "stock_inicial":
                        conn.execute(
                            text(
                                "UPDATE medicamento SET stock_inicial = GREATEST(cantidad_stock, 30)"
                            )
                        )
    except Exception:
        # No bloquear el arranque si la BD aún no está lista en entorno de test aislado
        pass


@asynccontextmanager
async def lifespan(_app: FastAPI):
    asegurar_esquema_mysql()
    yield


app = FastAPI(title="MedReminder AI API", lifespan=lifespan)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(medicamentos.router)
app.include_router(tratamientos.router)
app.include_router(recordatorios.router)
app.include_router(alergias.router)
app.include_router(contactos.router)
app.include_router(ai.router)
