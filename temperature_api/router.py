from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Union

from city_crud_api.models import DBCity
from city_crud_api.schemas import CityBaseModel
from database import get_db
from temperature_api import crud
from temperature_api.crud import get_location_key_of_whether_api, get_temperature_by_location_key, add_temperature_to_db
from temperature_api.models import DBTemperature
from temperature_api.schemas import Temperature, TemperatureValue

import asyncio
import httpx

router = APIRouter()


@router.get("/temperatures/", tags=["temperatures"], response_model=Union[list[TemperatureValue], list[Temperature]])
def read_temperatures(city_id: int | None = None, db: Session = Depends(get_db)):
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
async def update_temperatures(db: Session = Depends(get_db)):
    cities_id_name = db.execute(select(DBCity.id, DBCity.name)).all()
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            [tg.create_task(add_temperature_to_db(id=id, name=name, db=db, client=client)) for id, name in cities_id_name]
        db.commit()
    return {"Updated": True}
