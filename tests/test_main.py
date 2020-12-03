from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base, get_db
from api.main import app
from api import schemas, crud
from tests.fixtures import responses_data
from tests.fixtures.adverts import test_advert


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





'''def test_path_stat():
    advert_get_stat = schemas.AdvertStatRequest(advert_id=2, interval=1000)
    response = client.post(
        "/stat",
        json={'advert_id': advert_get_stat.advert_id, 'interval': advert_get_stat.interval}
    )
    assert response.status_code == 200
    assert response.json() == responses_data.response_id2_interval1000_data
    advert_get_stat = schemas.AdvertStatRequest(advert_id=0, interval=1000)
    response = client.post(
        "/stat",
        json={'advert_id': advert_get_stat.advert_id, 'interval': advert_get_stat.interval}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'No such advert'}
'''
