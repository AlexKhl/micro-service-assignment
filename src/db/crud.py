from sqlalchemy.orm import Session
from . import db_models, schemas


def get_word(db: Session, word: str):
    return db.query(db_models.Word).filter(db_models.Word.word == word).first()


def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Word).offset(skip).limit(limit).all()


def create_word(db: Session, word: schemas.WordCreate):
    db_word = db_models.Word(word=word.word)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def get_translations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Translate).offset(skip).limit(limit).all()


def create_translation(db: Session, translation: schemas.TranslationCreate, word_id: int):
    db_translation = db_models.Translate(**translation.dict(), owner_id=word_id)
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation