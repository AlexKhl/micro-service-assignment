from typing import List
from fastapi import Depends, FastAPI, HTTPException
from requests import Session

from settings import Settings as conf
from db.database import SessionLocal, engine, Base
from db import crud, schemas

app = FastAPI()


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


@app.get("/generate/", response_model=List[schemas.Word])
def generate_words(db: Session = Depends(get_db)):
    list = ["porte", "avion", "table", "chien", "fleur", "lumiere", "voiture", "jardin", "fenetre", "orange", "cheval",
            "montre", "argent", "chemin", "visage", "cafe", "camion", "carte", "ecole", "livre", "hiver", "guitare",
            "papier", "garcon", "carton", "bureau", "chaise", "chambre", "pomme", "crayon", "poulet", "parler",
            "maison", "image", "verre", "fraise", "pomme", "poire", "souris", "tigre", "panda", "python", "source",
            "valeur", "tableau", "ecran", "manger", "apporter"]

    for word in list:
        crud.create_word(db=db, word=word)
    return crud.get_words(db, '', 1, 50)


@app.get("/words-list/{query_string}/{page}/{page_size}", response_model=List[schemas.Word])
def words_list(
        query_string: str,
        page: int,
        page_size: int,
        db: Session = Depends(get_db)
) -> List[schemas.Word]:
    result = crud.get_words(db, query_string, page, page_size)
    return result


@app.post("/add-word/", response_model=schemas.Word)
def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
    db_word = crud.get_word(db, word=word.word)
    if db_word:
        raise HTTPException(status_code=400, detail="Word is already added")
    return crud.create_word(db=db, word=word)


@app.delete("/delete-word/{word}")
def delete_item(word: str, db: Session = Depends(get_db)):
    crud.delete_word(db=db, word=word)
    return {"word": word, "status": "deleted"}