from sqlalchemy.orm import Session
from api import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func
from api.storage_connection import SessionLocal

MESSAGES = {'max_count': 'Максимальное количество объявлений за период',
            'min_count': 'Минимальное количество объявлений за период',
            'average_count': 'Среднее количество объявлений за период'}


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
    item_stats_to_add = models.\
        ItemsStats(item_id=item_stats.item_id,
                   advert_count=item_stats.items_quantity,
                   timestamp=item_stats.timestamp)
    db.add(item_stats_to_add)
    db.commit()
    return item_stats_to_add


def get_item_stat(db: Session, item_get_stat: schemas.ItemStatRequest):
    date_from = get_date_some_days_ago(item_get_stat.interval)
    result = db.query(
        func.max(models.ItemsStats.advert_count),
        func.min(models.ItemsStats.advert_count),
        func.avg(models.ItemsStats.advert_count)
    ).filter(models.ItemsStats.item_id == item_get_stat.item_id,
             models.ItemsStats.timestamp > date_from)
    if result[0][0] is not None:
        return {MESSAGES['max_count']: result[0][0],
                MESSAGES['min_count']: result[0][1],
                MESSAGES['average_count']: result[0][2]}


def get_date_some_days_ago(days: int):
    return datetime.today() - timedelta(days=days)


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Items).\
        filter(models.Items.id == item_id).first()


def clear_db(db: Session):
    records_to_delete = db.query(models.ItemsStats).all()
    for record in records_to_delete:
        db.delete(record)
    records_to_delete = db.query(models.Items).all()
    for record in records_to_delete:
        db.delete(record)
    db.commit()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
