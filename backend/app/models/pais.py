from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Pais(Base):
    __tablename__ = "paises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    codigo_iso: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    continente_id: Mapped[int | None] = mapped_column(ForeignKey("continentes.id"), nullable=True)
    continente: Mapped["Continente"] = relationship(back_populates="paises")
    poblaciones: Mapped[list["Poblacion"]] = relationship(back_populates="pais", cascade="all, delete-orphan")
