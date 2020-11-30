from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base
from api import crud
from api import schemas, models

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/fixtures/test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_get_advert_by_phrase():
    db = TestingSessionLocal()
    phrase = 'test phrase'
    assert crud.get_advert_by_phrase(db, phrase).id == 2
    db.close()


def test_register_advert():
    db = TestingSessionLocal()
    moscow_location_id = 637640
    advert = schemas.Advert(phrase='test register', location_id=moscow_location_id)
    assert crud.register_advert(db, advert) == crud.get_advert_by_phrase(db, advert.phrase).id
    advert_to_delete = db.query(models.Adverts).filter(models.Adverts.phrase == 'test register').first()
    db.delete(advert_to_delete)
    db.commit()
    db.close()
