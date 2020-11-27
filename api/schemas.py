from pydantic import BaseModel
from datetime import datetime


class Advert(BaseModel):
    phrase: str
    location_id: int


class AdvertStats(Advert):
    advert_count: int
    timestamp: datetime
