from sqlalchemy.orm import Session

from api import models, schemas


def get_advert_by_phrase(db: Session, phrase: str):
    return db.query(models.Adverts).filter(models.Adverts.phrase == phrase).first()


def register_advert(db: Session, advert: schemas.Advert):
    db_user = models.Adverts(phrase=advert.phrase, location_id=advert.location_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
