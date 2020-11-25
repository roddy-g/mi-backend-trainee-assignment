from sqlalchemy import Column, Integer, String, DateTime
from api.db import Base


class Adverts(Base):
    __tablename__ = "adverts"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, unique=True)
    location_id = Column(String)


class AdvertsStats(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, unique=True)
    location_id = Column(String)
    advert_count = Column(Integer)
    timestamp = Column(DateTime)


