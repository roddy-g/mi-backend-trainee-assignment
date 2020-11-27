from sqlalchemy.orm import Session
from api import models, schemas


def get_advert_by_phrase(db: Session, phrase: str):
    return db.query(models.Adverts)\
        .filter(models.Adverts.phrase == phrase).first()


def register_advert(db: Session, advert: schemas.Advert):
    db_record = models.Adverts(
        phrase=advert.phrase,
        location_id=advert.location_id
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db.query(models.Adverts).\
        filter(models.Adverts.phrase == advert.phrase).first().id


def write_stats(db: Session, advert_stats: schemas.AdvertStats):
    db_record = models.AdvertsStats(phrase=advert_stats.phrase,
                                    location_id=advert_stats.location_id,
                                    advert_count=advert_stats.advert_count,
                                    timestamp=advert_stats.timestamp)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
