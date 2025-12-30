from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Union

from city_crud_api.schemas import CityBaseModel
from database import get_db
from temperature_api import crud
from temperature_api.schemas import Temperature


router = APIRouter()


@router.get("/temperatures/", tags=["temperatures"], response_model=list[Temperature])
def read_temperatures(city_id: int | None = None, db: Session = Depends(get_db)) -> list[Temperature]:
    if city_id:
        city_temperature_list = crud.get_city_temperatures(city_id=city_id, db=db)

        return [
            TemperatureValue(
                temperature=city_temperature[0],
                date_time=city_temperature[1]
            )
            for city_temperature in city_temperature_list
        ]
    return crud.get_temperatures(db=db)


@router.post("/temperatures/update", tags=["temperatures"])
def update_temperatures(db: Session = Depends(get_db)):
    return crud.update_cities(db=db)
