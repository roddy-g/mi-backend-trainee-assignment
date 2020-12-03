from sqlalchemy import Column, Integer, String, DateTime
from api.db import Base
from sqlalchemy.schema import UniqueConstraint


class Adverts(Base):
    __tablename__ = "adverts"

    UniqueConstraint('phrase', 'location_id')

    id = Column(Integer, primary_key=True)
    phrase = Column(String)
    location_id = Column(Integer)


class AdvertsStats(Base):
    __tablename__ = "adverts stats"

    id = Column(Integer, primary_key=True)
    phrase = Column(String)
    location_id = Column(Integer)
    advert_count = Column(Integer)
    timestamp = Column(DateTime)
