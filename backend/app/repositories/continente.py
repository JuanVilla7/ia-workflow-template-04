from sqlalchemy.orm import Session

from app.models.continente import Continente
from app.schemas.continente import ContinenteCreate, ContinenteUpdate


def get(db: Session, continente_id: int) -> Continente | None:
    return db.get(Continente, continente_id)


def get_by_nombre(db: Session, nombre: str) -> Continente | None:
    return db.query(Continente).filter(Continente.nombre == nombre).first()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[Continente]:
    return db.query(Continente).offset(skip).limit(limit).all()


def create(db: Session, data: ContinenteCreate) -> Continente:
    continente = Continente(**data.model_dump())
    db.add(continente)
    db.commit()
    db.refresh(continente)
    return continente


def update(db: Session, continente: Continente, data: ContinenteUpdate) -> Continente:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(continente, field, value)
    db.commit()
    db.refresh(continente)
    return continente


def delete(db: Session, continente: Continente) -> None:
    db.delete(continente)
    db.commit()
