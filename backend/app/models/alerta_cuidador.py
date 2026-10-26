from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AlertaCuidador(Base):
    """Registro persistente de alertas y avisos enviados al cuidador del paciente."""

    __tablename__ = "alerta_cuidador"

    id_alerta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"), index=True)
    tipo_alerta: Mapped[str] = mapped_column(String(40), default="advertencia_normal")
    accion_origen: Mapped[str] = mapped_column(String(40), default="posponer")
    nombre_medicamento: Mapped[str] = mapped_column(String(160))
    dosis: Mapped[str] = mapped_column(String(80), default="")
    es_critico: Mapped[bool] = mapped_column(Boolean, default=False)
    mensaje: Mapped[str] = mapped_column(String(500))
    nombre_cuidador: Mapped[str] = mapped_column(String(160), default="Cuidador Principal")
    telefono_cuidador: Mapped[str] = mapped_column(String(60), default="")
    atendida: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_creacion: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
