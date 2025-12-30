from sqlalchemy import select
from sqlalchemy.orm import Session

from city_crud_api.models import DBCity
from temperature_api.models import DBTemperature
from fastapi import HTTPException

import requests
import json
import os


def get_location_key_of_whether_api(name: str) -> str:
    url = f"https://dataservice.accuweather.com/locations/v1/cities/search?q={name}"
    headers = {"Authorization": f"Bearer {os.environ["WHETHER_SERVICE_API_KEY"]}"}
    response = requests.get(url, headers=headers)
    if not json.loads(response.text):
        raise HTTPException(status_code=404, detail=f"City with this name {name} not found")
    return json.loads(response.text)[0]["Key"]


def get_temperature_by_location_key(key: str) -> float:
    url = f"https://dataservice.accuweather.com/currentconditions/v1/{key}"
    headers = {"Authorization": f"Bearer {os.environ["WHETHER_SERVICE_API_KEY"]}"}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)[0]["Temperature"]["Metric"]["Value"]


def get_temperatures(db: Session):
    return db.query(DBTemperature).all()


def get_city_temperatures(city_id: int, db: Session):
    stmt = select(DBTemperature.temperature, DBTemperature.data_time).filter_by(city_id=city_id)
    city_temperature_list = db.execute(stmt).all()
    return city_temperature_list