from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base
from api import crud
from api import schemas, models
from tests.fixtures.adverts import test_advert
from tests.fixtures.adverts_stats import *
from tests.fixtures.advert_stat_requests import test_advert_stat_request
from tests.fixtures.responses_data import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/fixtures/test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_get_advert_by_phrase():
    db = TestingSessionLocal()
    crud.add_advert(db, test_advert)
    location_id = crud.get_advert_by_phrase(db, test_advert.phrase).location_id
    assert location_id == test_advert.location_id
    crud.clear_db(db)
    db.close()


def test_add_advert():
    db = TestingSessionLocal()
    advert_id = crud.add_advert(db, test_advert).id
    assert advert_id == crud.get_advert_by_phrase(db, test_advert.phrase).id
    crud.clear_db(db)
    db.close()


def test_add_stats():
    db = TestingSessionLocal()
    crud.add_advert(db, test_advert)
    crud.add_stats(db, test_advert_stats_count_30)
    crud.add_stats(db, test_advert_stats_count_70)
    crud.add_stats(db, test_advert_stats_count_170)
    assert crud.get_advert_stat(db, test_advert_stat_request) == response_stat
    crud.clear_db(db)
    db.close()


def test_get_advert_stat():
    db = TestingSessionLocal()
    crud.add_advert(db, test_advert)
    crud.add_stats(db, test_advert_stats_count_30)
    crud.add_stats(db, test_advert_stats_count_70)
    crud.add_stats(db, test_advert_stats_count_170)
    assert crud.get_advert_stat(db, test_advert_stat_request) == response_stat
    crud.clear_db(db)
    db.close()



