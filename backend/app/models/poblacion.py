from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Poblacion(Base):
    __tablename__ = "poblaciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pais_id: Mapped[int] = mapped_column(ForeignKey("paises.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    anio: Mapped[int] = mapped_column(Integer, nullable=False)

    pais: Mapped["Pais"] = relationship(back_populates="poblaciones")
