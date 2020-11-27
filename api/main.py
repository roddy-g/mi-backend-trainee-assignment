from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from api import models, schemas, crud, get_data_from_avito
from api.db import engine, SessionLocal
import time


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/add")
def register(
        advert: schemas.Advert,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    db_record = crud.get_advert_by_phrase(db, phrase=advert.phrase)
    if db_record:
        message = "Advert already registered, id='{}'".format(db_record.id)
        raise HTTPException(status_code=400, detail=message)
    advert_id = crud.register_advert(db, advert)
    message = "Advert successfully registered with id = '{}'".format(advert_id)
    background_tasks.add_task(get_info_every_hour, advert)
    return {"message": message}


@app.get("/get")
def get(phrase: str, db: Session = Depends(get_db)):
    db_record = crud.get_advert_by_phrase(db, phrase=phrase)
    if db_record:
        return db_record
    else:
        raise HTTPException(status_code=400, detail="No such advert")


def get_info_every_hour(advert: schemas.Advert, db: Session = Depends(get_db)):
    i = 1
    while i < 5:
        advert_stats = get_data_from_avito.get_data_stat(advert)
        print(advert_stats)
        crud.write_stats(db, advert_stats)
        print('database problem')
        time.sleep(1)
        i += 1
