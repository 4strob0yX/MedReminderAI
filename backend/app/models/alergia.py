from datetime import datetime
from typing import Literal

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AlergiaUsuario(Base):
    """Mapeo de la tabla `alergia_usuario`."""

    __tablename__ = "alergia_usuario"
    __table_args__ = (Index("idx_alergia_usuario", "id_usuario"),)

    id_alergia: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    sustancia: Mapped[str] = mapped_column(String(255))
    severidad: Mapped[str] = mapped_column(
        Enum("leve", "moderada", "grave", name="severidad_alergia"),
        default="grave",
    )
    reaccion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
