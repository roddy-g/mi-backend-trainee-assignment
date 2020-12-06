from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from api import models, schemas, database_functions
from api.db import engine, SessionLocal, get_db
from datetime import datetime
import requests
from fastapi_utils.tasks import repeat_every


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/add")
async def register(
        item: schemas.Item,
        db: Session = Depends(get_db)
):
    db_record = database_functions.get_item(db, item)
    if db_record:
        message = "Advert already registered, id = '{}'".format(db_record.id)
        raise HTTPException(status_code=400, detail=message)
    item_id = database_functions.add_item(db, item).id
    message = "Advert successfully registered with id = '{}'".format(item_id)
    return {"message": message}


@app.post("/stat")
def stat(item_stat_request: schemas.ItemStatRequest,
         db: Session = Depends(get_db)
         ):
    item_stat = database_functions.get_item_stat(db, item_stat_request)
    if item_stat:
        return item_stat
    else:
        raise HTTPException(status_code=400, detail="No such advert")


@app.on_event("startup")
@repeat_every(seconds=3600)  # 1 hour
def get_stat() -> None:
    db = SessionLocal()
    records = db.query(models.Items).all()
    for record in records:
        url = 'https://m.avito.ru/api/9/items?' \
              'key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query={}&' \
              'locationId={}&context=H4sIAAAAAAAA_wFCAL3_YToxOntzOjU6Inhf' \
              'c2d0IjtzOjQwOiJhZWQxY2ZlNzQ4OTE5MDdkM2E3N2JlYjUyNWZlZDI0NmEyN' \
              '2MwNzNlIjt9e-eh1UIAAAA&' \
              'page=1&display=list&limit=30'.format(record.phrase,
                                                    record.location_id)
        response = requests.get(url)
        data = response.json()
        try:
            advert_count = data['result']['totalCount']
            timestamp = datetime.now()
        except KeyError:
            return 'No valid data'
        item_stat = schemas.ItemStats(item_id=record.id,
                                      items_quantity=advert_count,
                                      timestamp=timestamp)
        database_functions.add_stats(db, item_stat)
    db.close()
