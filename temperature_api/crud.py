from sqlalchemy import select
from sqlalchemy.orm import Session

from city_crud_api.models import DBCity
from temperature_api.models import DBTemperature
from fastapi import HTTPException

import requests
import json
import os
import httpx


async def get_location_key_of_whether_api(name: str, client: httpx.AsyncClient) -> str:
    url = f"https://dataservice.accuweather.com/locations/v1/cities/search?q={name}"
    headers = {"Authorization": f"Bearer {os.environ["WHETHER_SERVICE_API_KEY"]}"}
    response = await client.get(url, headers=headers)
    if not json.loads(response.text):
        raise HTTPException(status_code=404, detail=f"City with this name {name} not found")
    return json.loads(response.text)[0]["Key"]


async def get_temperature_by_location_key(key: str, client: httpx.AsyncClient) -> float:
    url = f"https://dataservice.accuweather.com/currentconditions/v1/{key}"
    headers = {"Authorization": f"Bearer {os.environ["WHETHER_SERVICE_API_KEY"]}"}
    response = await client.get(url, headers=headers)
    return json.loads(response.text)[0]["Temperature"]["Metric"]["Value"]


def get_temperatures(db: Session):
    return db.query(DBTemperature).all()


def get_city_temperatures(city_id: int, db: Session):
    stmt = select(DBTemperature.temperature, DBTemperature.date_time).filter_by(city_id=city_id)
    city_temperature_list = db.execute(stmt).all()
    return city_temperature_list


async def add_temperature_to_db(id: int, name: str, db: Session, client: httpx.AsyncClient):
        key = await get_location_key_of_whether_api(name, client)
        temperature_value = await get_temperature_by_location_key(key, client)
        temperature = DBTemperature(
            city_id=id,
            temperature=temperature_value,
        )
        db.add(temperature)

