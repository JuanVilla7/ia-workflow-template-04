import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.poblacion import Poblacion
from app.repositories import poblacion as repo
from app.repositories import pais as pais_repo
from app.schemas.poblacion import PoblacionCreate, PoblacionRead, PoblacionUpdate

logger = logging.getLogger("api.services.poblacion")


def _get_or_404(db: Session, poblacion_id: int) -> Poblacion:
    poblacion = repo.get(db, poblacion_id)
    if not poblacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro de población con id {poblacion_id} no encontrado",
        )
    return poblacion


def get_poblacion(db: Session, poblacion_id: int) -> PoblacionRead:
    return PoblacionRead.model_validate(_get_or_404(db, poblacion_id))


def list_poblaciones(db: Session, skip: int = 0, limit: int = 100) -> list[PoblacionRead]:
    return [PoblacionRead.model_validate(p) for p in repo.list_all(db, skip, limit)]


def create_poblacion(db: Session, data: PoblacionCreate) -> PoblacionRead:
    # Verify pais exists
    if not pais_repo.get(db, data.pais_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"País con id {data.pais_id} no encontrado",
        )
    return PoblacionRead.model_validate(repo.create(db, data))


def update_poblacion(db: Session, poblacion_id: int, data: PoblacionUpdate) -> PoblacionRead:
    poblacion = _get_or_404(db, poblacion_id)
    return PoblacionRead.model_validate(repo.update(db, poblacion, data))


def delete_poblacion(db: Session, poblacion_id: int) -> None:
    poblacion = _get_or_404(db, poblacion_id)
    repo.delete(db, poblacion)
