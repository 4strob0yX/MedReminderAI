from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class VinculacionCuidador(Base):
    """Vinculación real multi-dispositivo entre un Paciente y un Cuidador."""

    __tablename__ = "vinculacion_cuidador"
    __table_args__ = (
        Index("idx_vinc_paciente", "id_paciente"),
        Index("idx_vinc_cuidador", "id_cuidador"),
    )

    id_vinculacion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_paciente: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    id_cuidador: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id_usuario", ondelete="SET NULL"), nullable=True
    )
    codigo_vinculacion: Mapped[str] = mapped_column(String(16), unique=True)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    parentesco: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expira_en: Mapped[datetime] = mapped_column(DateTime)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        server_default=func.current_timestamp(),
    )
    fecha_vinculacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
