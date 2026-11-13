from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class PasswordResetCode(Base):
    """Código temporal de un solo uso para recuperación segura de contraseña."""

    __tablename__ = "password_reset_code"
    __table_args__ = (Index("idx_reset_usuario", "id_usuario"),)

    id_reset: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    codigo_hash: Mapped[str] = mapped_column(String(255))
    expira_en: Mapped[datetime] = mapped_column(DateTime)
    usado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        server_default=func.current_timestamp(),
    )
