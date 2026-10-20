from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Medicamento(Base):
    """Mapeo de la tabla `medicamento` (DDL en db/mysql/init/01_schema.sql)."""

    __tablename__ = "medicamento"

    id_medicamento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    nombre: Mapped[str] = mapped_column(String(255))
    principio_activo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dosis: Mapped[str] = mapped_column(String(100))
    cantidad_stock: Mapped[int] = mapped_column(Integer, default=0)
    stock_inicial: Mapped[int] = mapped_column(Integer, default=30, server_default="30")
    forma_farmaceutica: Mapped[str] = mapped_column(
        String(40), default="comprimidos", server_default="comprimidos"
    )
    color_pastilla: Mapped[str] = mapped_column(
        String(40), default="blanco", server_default="blanco"
    )
    instrucciones_toma: Mapped[str | None] = mapped_column(String(255), nullable=True)
    proposito: Mapped[str | None] = mapped_column(String(120), nullable=True)
    permite_posponer: Mapped[bool] = mapped_column(Boolean, default=True)
    es_critico: Mapped[bool] = mapped_column(Boolean, default=False)
    contraindicaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
