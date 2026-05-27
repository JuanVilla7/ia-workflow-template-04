import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.poblacion import PoblacionCreate, PoblacionRead, PoblacionUpdate
from app.services import poblacion as svc

logger = logging.getLogger("api.routers.poblacion")

router = APIRouter(prefix="/poblaciones", tags=["poblaciones"])


@router.get("/", response_model=list[PoblacionRead])
def list_poblaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return svc.list_poblaciones(db, skip, limit)


@router.get("/{poblacion_id}", response_model=PoblacionRead)
def get_poblacion(poblacion_id: int, db: Session = Depends(get_db)):
    return svc.get_poblacion(db, poblacion_id)


@router.post("/", response_model=PoblacionRead, status_code=status.HTTP_201_CREATED)
def create_poblacion(data: PoblacionCreate, db: Session = Depends(get_db)):
    return svc.create_poblacion(db, data)


@router.put("/{poblacion_id}", response_model=PoblacionRead)
def update_poblacion(poblacion_id: int, data: PoblacionUpdate, db: Session = Depends(get_db)):
    return svc.update_poblacion(db, poblacion_id, data)


@router.delete("/{poblacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poblacion(poblacion_id: int, db: Session = Depends(get_db)):
    svc.delete_poblacion(db, poblacion_id)
