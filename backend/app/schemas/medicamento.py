from pydantic import BaseModel, Field, field_validator


class MedicamentoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    principio_activo: str | None = Field(default=None, max_length=255)
    dosis: str = Field(min_length=1, max_length=100)
    cantidad_stock: int = Field(default=0, ge=0)
    permite_posponer: bool = Field(default=True)
    es_critico: bool = Field(default=False)
    contraindicaciones: str | None = Field(default=None)

    @field_validator("nombre", "dosis")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El campo no puede estar vacio")
        return v


class MedicamentoOut(BaseModel):
    id_medicamento: int
    nombre: str
    principio_activo: str | None = None
    dosis: str
    cantidad_stock: int
    permite_posponer: bool = True
    es_critico: bool = False
    contraindicaciones: str | None = None

    model_config = {"from_attributes": True}


class MedicamentoCatalogoItem(BaseModel):
    nombre: str
    principio_activo: str
    familia: str
    dosis_sugerida: str
    forma_farmaceutica: str
    contraindicaciones: str
    es_critico_defecto: bool = False


class VerificarAlergiasIn(BaseModel):
    nombre: str
    principio_activo: str | None = None


class VerificarAlergiasOut(BaseModel):
    tiene_conflicto: bool
    alerta: str | None = None
    alergia_detectada: str | None = None
    severidad: str | None = None
