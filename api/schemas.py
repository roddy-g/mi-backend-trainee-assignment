from typing import List
from pydantic import BaseModel
from datetime import datetime


class Advert(BaseModel):
    phrase: str
    location_id: str


class AdvertStats(Advert):
    advert_count: int
    timestamp: datetime


