import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.continente import Continente
from app.repositories import continente as repo
from app.schemas.continente import ContinenteCreate, ContinenteRead, ContinenteUpdate

logger = logging.getLogger("api.services.continente")


def _check_nombre_unique(db: Session, nombre: str, exclude_id: int | None = None) -> None:
    existing = repo.get_by_nombre(db, nombre)
    if existing and existing.id != exclude_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Continente con nombre '{nombre}' ya existe",
        )


def _get_or_404(db: Session, continente_id: int) -> Continente:
    continente = repo.get(db, continente_id)
    if not continente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Continente con id {continente_id} no encontrado",
        )
    return continente


def get_continente(db: Session, continente_id: int) -> ContinenteRead:
    logger.debug("get_continente id=%d", continente_id)
    return ContinenteRead.model_validate(_get_or_404(db, continente_id))


def list_continentes(db: Session, skip: int = 0, limit: int = 100) -> list[ContinenteRead]:
    logger.debug("list_continentes skip=%d limit=%d", skip, limit)
    return [ContinenteRead.model_validate(c) for c in repo.list_all(db, skip, limit)]


def create_continente(db: Session, data: ContinenteCreate) -> ContinenteRead:
    logger.info("create_continente nombre=%s", data.nombre)
    _check_nombre_unique(db, data.nombre)
    return ContinenteRead.model_validate(repo.create(db, data))


def update_continente(db: Session, continente_id: int, data: ContinenteUpdate) -> ContinenteRead:
    logger.info("update_continente id=%d", continente_id)
    continente = _get_or_404(db, continente_id)
    if data.nombre:
        _check_nombre_unique(db, data.nombre, exclude_id=continente_id)
    return ContinenteRead.model_validate(repo.update(db, continente, data))


def delete_continente(db: Session, continente_id: int) -> None:
    logger.info("delete_continente id=%d", continente_id)
    continente = _get_or_404(db, continente_id)
    repo.delete(db, continente)
