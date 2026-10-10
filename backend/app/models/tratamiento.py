from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Tratamiento(Base):
    """Mapeo de la tabla `tratamiento`. No tiene id_usuario propio: la propiedad
    se resuelve siempre via JOIN con `medicamento.id_usuario`."""

    __tablename__ = "tratamiento"

    id_tratamiento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_medicamento: Mapped[int] = mapped_column(
        ForeignKey("medicamento.id_medicamento", ondelete="CASCADE")
    )
    frecuencia_horas: Mapped[int]
    fecha_inicio: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    fecha_fin: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    estado: Mapped[str] = mapped_column(
        Enum("activo", "inactivo", name="estado_tratamiento"), server_default="activo"
    )
