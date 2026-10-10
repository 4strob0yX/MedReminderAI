from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, SmallInteger, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Recordatorio(Base):
    """Planificacion teorica de una toma (DDL en db/mysql/init/01_schema.sql).
    hora_programada se guarda siempre en UTC."""

    __tablename__ = "recordatorio"
    __table_args__ = (Index("idx_recordatorio_trat_hora", "id_tratamiento", "hora_programada"),)

    id_recordatorio: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_tratamiento: Mapped[int] = mapped_column(
        ForeignKey("tratamiento.id_tratamiento", ondelete="CASCADE")
    )
    hora_programada: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(
        Enum("pendiente", "tomado", "pospuesto", "omitido", name="estado_recordatorio"),
        server_default="pendiente",
    )
    veces_pospuesto: Mapped[int] = mapped_column(SmallInteger, server_default="0")


class HistorialToma(Base):
    """Log de auditoria: NO es unico por recordatorio."""

    __tablename__ = "historial_toma"

    id_historial: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_recordatorio: Mapped[int] = mapped_column(
        ForeignKey("recordatorio.id_recordatorio", ondelete="CASCADE")
    )
    fecha_accion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    estado_final: Mapped[str] = mapped_column(
        Enum("tomado", "pospuesto", "omitido", name="estado_historial")
    )
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
