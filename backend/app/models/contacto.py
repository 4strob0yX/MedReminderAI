from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ContactoApoyo(Base):
    """Mapeo de la tabla `contacto_apoyo` para cuidadores o contactos de emergencia."""

    __tablename__ = "contacto_apoyo"
    __table_args__ = (Index("idx_contacto_usuario", "id_usuario"),)

    id_contacto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    nombre_completo: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str] = mapped_column(String(50))
    parentesco: Mapped[str] = mapped_column(String(100))
    correo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    es_principal: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
