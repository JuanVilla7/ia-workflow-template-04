from pydantic import BaseModel, ConfigDict, field_validator


class PoblacionBase(BaseModel):
    pais_id: int
    cantidad: int
    anio: int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("cantidad no puede ser negativa")
        return v

    @field_validator("anio")
    @classmethod
    def anio_valid(cls, v: int) -> int:
        if v < 0 or v > 2100:
            raise ValueError("anio no es válido")
        return v


class PoblacionCreate(PoblacionBase):
    pass


class PoblacionUpdate(BaseModel):
    cantidad: int | None = None
    anio: int | None = None

    @field_validator("cantidad")
    @classmethod
    def cantidad_positive(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("cantidad no puede ser negativa")
        return v


class PoblacionRead(PoblacionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
