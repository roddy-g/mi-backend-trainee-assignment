from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base
from api import crud
from api import schemas, models
from tests.fixtures.adverts import test_advert
from tests.fixtures.adverts_stats import test_advert_stats
from tests.fixtures.advert_stat_requests import test_advert_stat_request

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
    crud.delete_advert_by_phrase(db, test_advert.phrase)
    db.close()


def test_add_advert():
    db = TestingSessionLocal()
    advert_id = crud.add_advert(db, test_advert).id
    assert advert_id == crud.get_advert_by_phrase(db, test_advert.phrase).id
    crud.delete_advert_by_phrase(db, test_advert.phrase)
    db.close()


def test_add_stats():
    db = TestingSessionLocal()
    crud.add_advert(db, test_advert)
    crud.add_stats(db, test_advert_stats)
    crud.add_stats(db, test_advert_stats)
    crud.add_stats(db, test_advert_stats)
    assert crud.get_advert_stat(db, test_advert_stat_request)['Среднее количество объявлений за период'] == 100
    crud.delete_advert_by_phrase(db, test_advert.phrase)
    crud.delete_advert_stat_by_phrase(db, test_advert_stats.phrase)
    db.close()


