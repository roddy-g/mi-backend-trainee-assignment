from sqlalchemy.orm import Session
from api import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func


def get_item(db: Session, item: schemas.Item):
    return db.query(models.Items)\
        .filter(models.Items.phrase == item.phrase,
                models.Items.location_id == item.location_id).first()


def add_item(db: Session, item: schemas.Item):
    item_to_add = models.Items(
        phrase=item.phrase,
        location_id=item.location_id
    )
    db.add(item_to_add)
    db.commit()
    return item_to_add


def add_stats(db: Session, item_stats: schemas.ItemStats):
    db_record = models.ItemsStats(phrase=item_stats.phrase,
                                  location_id=item_stats.location_id,
                                  advert_count=item_stats.advert_count,
                                  timestamp=item_stats.timestamp)
    db.add(db_record)
    db.commit()
    return db_record


def get_date_some_days_ago(days: int):
    return datetime.today() - timedelta(days=days)


def get_item_by_id(db: Session, advert_id: int):
    return db.query(models.Items).\
        filter(models.Items.id == advert_id).first()


def get_item_stat(db: Session, advert_get_stat: schemas.ItemStatRequest):
    date_from = get_date_some_days_ago(advert_get_stat.interval)
    advert = get_item_by_id(db, advert_get_stat.advert_id)
    if not advert:
        return None
    result = db.query(
        func.max(models.ItemsStats.advert_count).
        filter(models.ItemsStats.phrase == advert.phrase,
               models.ItemsStats.location_id == advert.location_id,
               models.ItemsStats.timestamp > date_from),
        func.min(models.ItemsStats.advert_count).
        filter(models.ItemsStats.phrase == advert.phrase,
               models.ItemsStats.location_id == advert.location_id,
               models.ItemsStats.timestamp > date_from),
        func.sum(models.ItemsStats.advert_count).
        filter(models.ItemsStats.phrase == advert.phrase,
               models.ItemsStats.location_id == advert.location_id,
               models.ItemsStats.timestamp > date_from)
        / func.count(models.ItemsStats.location_id).
        filter(models.ItemsStats.phrase == advert.phrase,
               models.ItemsStats.location_id == advert.location_id,
               models.ItemsStats.timestamp > date_from)
    )
    message_max_count = 'Максимальное количество объявлений за период'
    message_min_count = 'Минимальное количество объявлений за период'
    message_average_count = 'Среднее количество объявлений за период'
    return {message_max_count: result[0][0],
            message_min_count: result[0][1],
            message_average_count: result[0][2]}


def clear_db(db: Session):
    records_to_delete = db.query(models.ItemsStats).all()
    for record in records_to_delete:
        db.delete(record)
    records_to_delete = db.query(models.Items).all()
    for record in records_to_delete:
        db.delete(record)
    db.commit()
