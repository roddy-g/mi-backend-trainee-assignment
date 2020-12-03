from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base, get_db
from api.main import app
from api import schemas, crud
from tests.fixtures import responses_data
from tests.fixtures.adverts import test_advert
from tests.fixtures.adverts_stats import test_advert_stats
from tests.fixtures.advert_stat_requests import test_advert_stat_request


SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/fixtures/test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_path_add():
    response = client.post(
        "/add",
        json={'phrase': test_advert.phrase,
              'location_id': 'string type of location'}
    )
    assert response.status_code == 422
    response = client.post(
        "/add",
        json={'phrase': test_advert.phrase,
              'location_id': test_advert.location_id}
    )
    assert response.status_code == 200
    assert response.json()['message'] == "Advert successfully registered with id = '1'"
    response = client.post(
        "/add",
        json={'phrase': test_advert.phrase,
              'location_id': test_advert.location_id}
    )
    assert response.status_code == 400
    assert response.json()['detail'] == "Advert already registered, id = '1'"
    db = TestingSessionLocal()
    crud.delete_advert_by_phrase(db, test_advert.phrase)
    db.close()


def test_path_stat():
    response = client.post(
        "/stat",
        json={'advert_id': test_advert_stat_request.advert_id,
              'interval': test_advert_stat_request.interval}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'No such advert'}
    db = TestingSessionLocal()
    crud.add_advert(db, test_advert)
    crud.add_stats(db, test_advert_stats)
    crud.add_stats(db, test_advert_stats)
    crud.add_stats(db, test_advert_stats)
    db.close()
    response = client.post(
        "/stat",
        json={'advert_id': test_advert_stat_request.advert_id,
              'interval': test_advert_stat_request.interval}
    )
    assert response.status_code == 200
    assert response.json()['Среднее количество объявлений за период'] == 100
    db = TestingSessionLocal()
    crud.delete_advert_by_phrase(db, test_advert.phrase)
    crud.delete_advert_stat_by_phrase(db, test_advert_stats.phrase)
    db.close()
    response = client.post(
        "/stat",
        json={'advert_id': test_advert_stat_request.advert_id,
              'interval': 'string'}
    )
    assert response.status_code == 422



