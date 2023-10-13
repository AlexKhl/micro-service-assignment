from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from googletrans import Translator
from requests import Session

from settings import Settings as conf
from db.database import SessionLocal, engine, Base
from db import crud, db_models, schemas

app = FastAPI()
translate_client = Translator()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def read_default():
    result = translate_client.translate(text="matin", dest=conf.destination_language, src=conf.source_language)
    return result


@app.get("/words-list")
def words_list():
    return {"List": "Words"}


@app.put("/translate-word/{word}")
async def translate_word(word: str):
    result = translate_client.translate(text=word, dest=conf.destination_language, src=conf.source_language)
    return result


@app.post("/words/", response_model=schemas.Word)
def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
    db_word = crud.get_word(db, word=word.word)
    if db_word:
        raise HTTPException(status_code=400, detail="Word is already added")
    return crud.create_word(db=db, word=word)