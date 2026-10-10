from pydantic import BaseModel, Field, field_validator


class MedicamentoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    dosis: str = Field(min_length=1, max_length=100)
    cantidad_stock: int = Field(default=0, ge=0)

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
    dosis: str
    cantidad_stock: int

    model_config = {"from_attributes": True}
