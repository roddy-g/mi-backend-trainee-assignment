from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from api import models, schemas, database_functions, get_data_from_avito
from api.db import engine, SessionLocal, get_db

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
@repeat_every(seconds=60 * 60)  # 1 hour
def get_stat() -> None:
    db = SessionLocal()
    records = db.query(models.Items).all()
    for record in records:
        item = schemas.Item(phrase=record.phrase,
                            location_id=record.location_id)
        item_data = get_data_from_avito.get_data_stat(item)
        if item_data:
            database_functions.add_stats(db, item_data)
    db.close()
