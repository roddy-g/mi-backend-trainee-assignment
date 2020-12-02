from sqlalchemy.orm import Session
from api import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func


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
    return db_record.id


def update_stats(db: Session, advert_stats: schemas.AdvertStats):
    db_record = models.AdvertsStats(phrase=advert_stats.phrase,
                                    location_id=advert_stats.location_id,
                                    advert_count=advert_stats.advert_count,
                                    timestamp=advert_stats.timestamp)
    db.add(db_record)
    db.commit()


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
    max_count = db.query(func.max(models.AdvertsStats.advert_count)).\
        filter(models.AdvertsStats.phrase == advert.phrase).\
        filter(models.AdvertsStats.location_id == advert.location_id).\
        filter(models.AdvertsStats.timestamp > date_from).scalar()
    min_count = db.query(func.min(models.AdvertsStats.advert_count)). \
        filter(models.AdvertsStats.phrase == advert.phrase). \
        filter(models.AdvertsStats.location_id == advert.location_id). \
        filter(models.AdvertsStats.timestamp > date_from).scalar()
    average_count = db.query(
        func.sum(models.AdvertsStats.advert_count)
        / func.count(models.AdvertsStats.location_id)
    ).\
        filter(models.AdvertsStats.phrase == advert.phrase).\
        filter(models.AdvertsStats.location_id == advert.location_id).\
        filter(models.AdvertsStats.timestamp > date_from).scalar()
    message_max_count = 'Максимальное количество объявлений за период'
    message_min_count = 'Минимальное количество объявлений за период'
    message_average_count = 'Среднее количество объявлений за период'
    return {message_max_count: max_count,
            message_min_count: min_count,
            message_average_count: average_count}
