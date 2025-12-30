from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city_crud_api import crud
from city_crud_api.schemas import CityCreate, City, CityUpdate
from database import get_db

router = APIRouter()


@router.get("/cities/", tags=["cities"])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/cities/{city_id}", tags=["cities"])
def read_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city(city_id=city_id, db=db)


@router.post("/cities/", tags=["cities"], response_model=City)
def create_cities(city_schema: CityCreate, db: Session = Depends(get_db)):
    return crud.create_cities(db=db, city_schema=city_schema)


@router.put("/cities/{city_id}", tags=["cities"], response_model=City)
def update_cities(city_id: int, city_schema: CityUpdate, db: Session = Depends(get_db)):
    return crud.update_cities(city_id=city_id, db=db, city_schema=city_schema)


@router.delete("/cities/{city_id}", tags=["cities"])
def delete_cities(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_cities(city_id=city_id, db=db)
