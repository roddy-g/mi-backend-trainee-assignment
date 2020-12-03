from sqlalchemy.orm import Session
from api import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func


def get_advert_by_phrase(db: Session, phrase: str):
    return db.query(models.Adverts)\
        .filter(models.Adverts.phrase == phrase).first()


def add_advert(db: Session, advert: schemas.Advert):
    db_record = models.Adverts(
        phrase=advert.phrase,
        location_id=advert.location_id
    )
    db.add(db_record)
    db.commit()
    return db_record


def add_stats(db: Session, advert_stats: schemas.AdvertStats):
    db_record = models.AdvertsStats(phrase=advert_stats.phrase,
                                    location_id=advert_stats.location_id,
                                    advert_count=advert_stats.advert_count,
                                    timestamp=advert_stats.timestamp)
    db.add(db_record)
    db.commit()
    return db_record


def get_date_some_days_ago(days: int):
    return datetime.today() - timedelta(days=days)


def get_advert_by_id(db: Session, advert_id: int):
    return db.query(models.Adverts).\
        filter(models.Adverts.id == advert_id).first()


def get_advert_stat(db: Session, advert_get_stat: schemas.AdvertStatRequest):
    date_from = get_date_some_days_ago(advert_get_stat.interval)
    advert = get_advert_by_id(db, advert_get_stat.advert_id)
    if not advert:
        return None
    result = db.query(
        func.max(models.AdvertsStats.advert_count).
        filter(models.AdvertsStats.phrase == advert.phrase,
               models.AdvertsStats.location_id == advert.location_id,
               models.AdvertsStats.timestamp > date_from),
        func.min(models.AdvertsStats.advert_count).
        filter(models.AdvertsStats.phrase == advert.phrase,
               models.AdvertsStats.location_id == advert.location_id,
               models.AdvertsStats.timestamp > date_from),
        func.sum(models.AdvertsStats.advert_count).
        filter(models.AdvertsStats.phrase == advert.phrase,
               models.AdvertsStats.location_id == advert.location_id,
               models.AdvertsStats.timestamp > date_from)
        / func.count(models.AdvertsStats.location_id).
        filter(models.AdvertsStats.phrase == advert.phrase,
               models.AdvertsStats.location_id == advert.location_id,
               models.AdvertsStats.timestamp > date_from)
    )
    message_max_count = 'Максимальное количество объявлений за период'
    message_min_count = 'Минимальное количество объявлений за период'
    message_average_count = 'Среднее количество объявлений за период'
    return {message_max_count: result[0][0],
            message_min_count: result[0][1],
            message_average_count: result[0][2]}


def clear_db(db: Session):
    records_to_delete = db.query(models.AdvertsStats).all()
    for record in records_to_delete:
        db.delete(record)
    records_to_delete = db.query(models.Adverts).all()
    for record in records_to_delete:
        db.delete(record)
    db.commit()
