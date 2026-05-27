import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.continente import ContinenteCreate, ContinenteRead, ContinenteUpdate
from app.services import continente as svc

logger = logging.getLogger("api.routers.continente")

router = APIRouter(prefix="/continentes", tags=["continentes"])


@router.get("/", response_model=list[ContinenteRead])
def list_continentes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("GET /continentes skip=%d limit=%d", skip, limit)
    return svc.list_continentes(db, skip, limit)


@router.get("/{continente_id}", response_model=ContinenteRead)
def get_continente(continente_id: int, db: Session = Depends(get_db)):
    logger.info("GET /continentes/%d", continente_id)
    return svc.get_continente(db, continente_id)


@router.post("/", response_model=ContinenteRead, status_code=status.HTTP_201_CREATED)
def create_continente(data: ContinenteCreate, db: Session = Depends(get_db)):
    logger.info("POST /continentes nombre=%s", data.nombre)
    return svc.create_continente(db, data)


@router.put("/{continente_id}", response_model=ContinenteRead)
def update_continente(continente_id: int, data: ContinenteUpdate, db: Session = Depends(get_db)):
    logger.info("PUT /continentes/%d", continente_id)
    return svc.update_continente(db, continente_id, data)


@router.delete("/{continente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_continente(continente_id: int, db: Session = Depends(get_db)):
    logger.info("DELETE /continentes/%d", continente_id)
    svc.delete_continente(db, continente_id)
