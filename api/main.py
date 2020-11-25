from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from api import models, schemas, crud
from api.db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add")
def register(advert: schemas.Advert, db: Session = Depends(get_db)):
    db_user = crud.get_advert_by_phrase(db, phrase=advert.phrase)
    if db_user:
        raise HTTPException(status_code=400, detail="Advert already registered")
    crud.register_advert(db=db, advert=advert)
    return {"message": "registered successfully"}


@app.get("/get")
def get(phrase: str, db: Session = Depends(get_db)):
    db_user = crud.get_advert_by_phrase(db, phrase=phrase)
    if not db_user:
        raise HTTPException(status_code=400, detail="No such advert")
    return crud.get_advert_by_phrase(db, phrase=phrase)


@app.get("/stat")
def get(phrase: str, db: Session = Depends(get_db)):
    return {'message':'message'}