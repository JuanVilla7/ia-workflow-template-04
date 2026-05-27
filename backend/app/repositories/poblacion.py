from sqlalchemy.orm import Session

from app.models.poblacion import Poblacion
from app.schemas.poblacion import PoblacionCreate, PoblacionUpdate


def get(db: Session, poblacion_id: int) -> Poblacion | None:
    return db.get(Poblacion, poblacion_id)


def list_by_pais(db: Session, pais_id: int) -> list[Poblacion]:
    return db.query(Poblacion).filter(Poblacion.pais_id == pais_id).all()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[Poblacion]:
    return db.query(Poblacion).offset(skip).limit(limit).all()


def create(db: Session, data: PoblacionCreate) -> Poblacion:
    poblacion = Poblacion(**data.model_dump())
    db.add(poblacion)
    db.commit()
    db.refresh(poblacion)
    return poblacion


def update(db: Session, poblacion: Poblacion, data: PoblacionUpdate) -> Poblacion:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(poblacion, field, value)
    db.commit()
    db.refresh(poblacion)
    return poblacion


def delete(db: Session, poblacion: Poblacion) -> None:
    db.delete(poblacion)
    db.commit()
