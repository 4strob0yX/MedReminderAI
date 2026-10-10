from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Medicamento(Base):
    """Mapeo de la tabla `medicamento` (DDL en db/mysql/init/01_schema.sql)."""

    __tablename__ = "medicamento"

    id_medicamento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))
    nombre: Mapped[str] = mapped_column(String(255))
    dosis: Mapped[str] = mapped_column(String(100))
    cantidad_stock: Mapped[int] = mapped_column(default=0)
