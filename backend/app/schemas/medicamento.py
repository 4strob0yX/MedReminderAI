from pydantic import BaseModel, Field, field_validator, model_validator


class MedicamentoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    principio_activo: str | None = Field(default=None, max_length=255)
    dosis: str = Field(min_length=1, max_length=100)
    cantidad_stock: int = Field(default=0, ge=0)
    stock_inicial: int | None = Field(default=None, ge=0)
    forma_farmaceutica: str = Field(default="comprimidos", max_length=40)
    color_pastilla: str = Field(default="blanco", max_length=40)
    instrucciones_toma: str | None = Field(default=None, max_length=255)
    proposito: str | None = Field(default=None, max_length=120)
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

    @model_validator(mode="after")
    def _default_stock_inicial(self):
        if self.stock_inicial is None or self.stock_inicial <= 0:
            self.stock_inicial = max(self.cantidad_stock, 30)
        return self


class MedicamentoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=255)
    principio_activo: str | None = Field(default=None, max_length=255)
    dosis: str | None = Field(default=None, min_length=1, max_length=100)
    cantidad_stock: int | None = Field(default=None, ge=0)
    stock_inicial: int | None = Field(default=None, ge=0)
    forma_farmaceutica: str | None = Field(default=None, max_length=40)
    color_pastilla: str | None = Field(default=None, max_length=40)
    instrucciones_toma: str | None = Field(default=None, max_length=255)
    proposito: str | None = Field(default=None, max_length=120)
    permite_posponer: bool | None = None
    es_critico: bool | None = None
    contraindicaciones: str | None = None

    @field_validator("nombre", "dosis")
    @classmethod
    def _strip_optional(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v:
            raise ValueError("El campo no puede estar vacio")
        return v


class MedicamentoStockUpdate(BaseModel):
    cantidad_stock: int | None = Field(default=None, ge=0)
    stock_actual: int | None = Field(default=None, ge=0)
    stock_inicial: int | None = Field(default=None, ge=0)
    cantidad_agregar: int | None = Field(default=None, ge=1)


class MedicamentoOut(BaseModel):
    id_medicamento: int
    nombre: str
    principio_activo: str | None = None
    dosis: str
    cantidad_stock: int
    stock_inicial: int = 30
    forma_farmaceutica: str = "comprimidos"
    color_pastilla: str = "blanco"
    instrucciones_toma: str | None = None
    proposito: str | None = None
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
    forma_sugerida: str = "comprimidos"
    color_sugerido: str = "blanco"
    instrucciones_sugeridas: str = "Tomar con un vaso lleno de agua"
    proposito: str = "Tratamiento médico"
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
    tiene_interaccion: bool = False
    alerta_interaccion: str | None = None
    medicamento_conflicto: str | None = None
    interacciones: list[str] = Field(default_factory=list)
