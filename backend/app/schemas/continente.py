from pydantic import BaseModel, ConfigDict, field_validator


class ContinenteBase(BaseModel):
    nombre: str
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def nombre_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("nombre no puede estar vacío")
        if len(v) > 50:
            raise ValueError("nombre no puede superar 50 caracteres")
        return v


class ContinenteCreate(ContinenteBase):
    pass


class ContinenteUpdate(BaseModel):
    nombre: str | None = None
    activo: bool | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_not_empty(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("nombre no puede estar vacío")
        if len(v) > 50:
            raise ValueError("nombre no puede superar 50 caracteres")
        return v


class ContinenteRead(ContinenteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
