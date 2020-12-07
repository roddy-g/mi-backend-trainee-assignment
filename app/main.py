from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from app import models, schemas, storage
from app.storage_connection import engine, SessionLocal
from app.storage import get_db
from datetime import datetime
import requests
from fastapi_utils.tasks import repeat_every
from http import HTTPStatus

BASE_URL = 'https://m.avito.ru/api/9/items?' \
              'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query={}&' \
              'locationId={}&context=H4sIAAAAAAAA_wFCAL3_YToxOntzOjU6Inhf' \
              'c2d0IjtzOjQwOiJhZWQxY2ZlNzQ4OTE5MDdkM2E3N2JlYjUyNWZlZDI0NmEyN' \
              '2MwNzNlIjt9e-eh1UIAAAA&' \
              'page=1&display=list&limit=30'

INTERVAL_IN_SECONDS = 3600  # 1 hour

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/add")
async def register(
        item: schemas.Item,
        db: Session = Depends(get_db)
):
    db_record = storage.get_item(db, item)
    if db_record:
        message = "Advert already registered, id = '{}'".format(db_record.id)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=message)
    item_id = storage.add_item(db, item).id
    message = "Advert successfully registered with id = '{}'".format(item_id)
    return {"message": message}


@app.post("/stat")
def stat(item_stat_request: schemas.ItemStatRequest,
         db: Session = Depends(get_db)
         ):
    item_stat = storage.get_item_stat(db, item_stat_request)
    if item_stat:
        return item_stat
    else:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="No such advert")


@app.on_event("startup")
@repeat_every(seconds=INTERVAL_IN_SECONDS)
def get_stats_from_avito_for_all_records() -> None:
    db = SessionLocal()
    records = db.query(models.Items).all()
    for record in records:
        print(record)
        url = BASE_URL.format(record.phrase, record.location_id)
        response = requests.get(url)
        data = response.json()
        if response.status_code != HTTPStatus.OK:
            continue
        try:
            advert_count = data['result']['totalCount']
            timestamp = datetime.now()
        except KeyError:
            print('No valid data for id={}, search phrase={}'.
                  format(record.id, record.phrase))
            continue
        item_stat = schemas.ItemStats(item_id=record.id,
                                      items_quantity=advert_count,
                                      timestamp=timestamp)
        storage.add_stats(db, item_stat)
    db.close()
