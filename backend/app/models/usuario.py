from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Usuario(Base):
    """Mapeo de la tabla `usuario` (el DDL vive en db/mysql/init/01_schema.sql)."""

    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(255))
    correo: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    fecha_registro: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
