from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Continente(Base):
    __tablename__ = "continentes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    paises: Mapped[list["Pais"]] = relationship(back_populates="continente")
