from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routers import (
    ai,
    alergias,
    auth,
    contactos,
    cuidador,
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

            # Migración automática de columnas nuevas en `usuario` (`fecha_nacimiento`, `rol`)
            filas_usr = conn.execute(
                text(
                    "SELECT LOWER(column_name) FROM information_schema.columns "
                    "WHERE table_schema = DATABASE() AND table_name = 'usuario'"
                )
            ).all()
            existentes_usr = {fila[0] for fila in filas_usr}
            if existentes_usr:
                if "fecha_nacimiento" not in existentes_usr:
                    conn.execute(
                        text("ALTER TABLE usuario ADD COLUMN fecha_nacimiento DATE NULL")
                    )
                    conn.execute(
                        text(
                            "UPDATE usuario SET fecha_nacimiento = '1957-05-14' "
                            "WHERE fecha_nacimiento IS NULL"
                        )
                    )
                if "rol" not in existentes_usr:
                    conn.execute(
                        text(
                            "ALTER TABLE usuario ADD COLUMN rol VARCHAR(30) NOT NULL DEFAULT 'paciente'"
                        )
                    )

            # Tabla persistente de alertas para la Vista del Cuidador
            conn.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS alerta_cuidador ("
                    "id_alerta INT AUTO_INCREMENT PRIMARY KEY, "
                    "id_usuario INT NOT NULL, "
                    "tipo_alerta VARCHAR(40) NOT NULL DEFAULT 'advertencia_normal', "
                    "accion_origen VARCHAR(40) NOT NULL DEFAULT 'posponer', "
                    "nombre_medicamento VARCHAR(160) NOT NULL, "
                    "dosis VARCHAR(80) NOT NULL DEFAULT '', "
                    "es_critico BOOLEAN NOT NULL DEFAULT FALSE, "
                    "mensaje VARCHAR(500) NOT NULL, "
                    "nombre_cuidador VARCHAR(160) NOT NULL DEFAULT 'Cuidador Principal', "
                    "telefono_cuidador VARCHAR(60) NOT NULL DEFAULT '', "
                    "atendida BOOLEAN NOT NULL DEFAULT FALSE, "
                    "fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "
                    "INDEX idx_alerta_usuario (id_usuario)"
                    ")"
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
app.include_router(cuidador.router)
app.include_router(ai.router)
