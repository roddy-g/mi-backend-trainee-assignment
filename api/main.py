from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from api import models, schemas, crud, get_data_from_avito
from api.db import engine, SessionLocal, get_db
import time


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/add")
async def register(
        advert: schemas.Advert,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    db_record = crud.get_advert_by_phrase(db, phrase=advert.phrase)
    if db_record:
        message = "Advert already registered, id = '{}'".format(db_record.id)
        raise HTTPException(status_code=400, detail=message)
    advert_id = crud.add_advert(db, advert).id
    message = "Advert successfully registered with id = '{}'".format(advert_id)
    # comment out background_tasks.add_task(get_info_every_hour, advert)
    return {"message": message}


@app.post("/stat")
def stat(advert_get_stat: schemas.AdvertStatRequest,
         db: Session = Depends(get_db)
         ):
    advert_stat = crud.get_advert_stat(db, advert_get_stat)
    if advert_stat:
        return advert_stat
    else:
        raise HTTPException(status_code=400, detail="No such advert")


async def get_info_every_hour(advert: schemas.Advert):
    while True:
        advert_stats = get_data_from_avito.get_data_stat(advert)
        if advert_stats:
            db = SessionLocal()
            crud.add_stats(db=db, advert_stats=advert_stats)
            db.close()
        time.sleep(3600)
