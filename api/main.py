from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from api import models, schemas, crud, get_data_from_avito
from api.db import engine, SessionLocal, get_db

from fastapi_utils.tasks import repeat_every


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/add")
async def register(
        advert: schemas.Item,
        db: Session = Depends(get_db)
):
    db_record = crud.get_advert_by_phrase(db, phrase=advert.phrase)
    if db_record:
        message = "Advert already registered, id = '{}'".format(db_record.id)
        raise HTTPException(status_code=400, detail=message)
    advert_id = crud.add_advert(db, advert).id
    message = "Advert successfully registered with id = '{}'".format(advert_id)
    return {"message": message}


@app.post("/stat")
def stat(advert_get_stat: schemas.ItemStatRequest,
         db: Session = Depends(get_db)
         ):
    advert_stat = crud.get_advert_stat(db, advert_get_stat)
    if advert_stat:
        return advert_stat
    else:
        raise HTTPException(status_code=400, detail="No such advert")


@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
def get_stat() -> None:
    db = SessionLocal()
    records = db.query(models.Adverts).all()
    for record in records:
        advert = schemas.Item(phrase=record.phrase,
                              location_id=record.location_id)
        advert_data = get_data_from_avito.get_data_stat(advert)
        if advert_data:
            crud.add_stats(db, advert_data)
    db.close()
