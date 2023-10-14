import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
import settings as conf

sys.path.append('utils/')
import translate as trans


from sqlalchemy.orm import Session
from . import db_models, schemas



def get_word(db: Session, word: str):
    return db.query(db_models.Word).filter(db_models.Word.word == word).first()


def get_words(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Word).offset(skip).limit(limit).all()


# TODO change source_language to more flexible option like global variable or conf variable with the possibility to
#  overriding it
def create_word(db: Session, word: schemas.WordCreate):
    # save the word in DB
    db_word = db_models.Word(word=word.word, language=conf.Settings.source_language)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    # save the translation in DB
    localTrans = trans.LocalTrans()
    trans_word = localTrans.translate(word.word)
    translation = get_translation(db, db_word.id)
    if not translation:
        create_translation(db, trans_word, conf.Settings.destination_language, word_id=db_word.id)
    return db_word


def get_translation(db: Session, word_id: int):
    return db.query(db_models.Translate).filter(db_models.Translate.word_id == word_id).first()


def get_translations_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Translate).offset(skip).limit(limit).all()


def create_translation(db: Session, translation: schemas.TranslationCreate, language: str, word_id: int):
    db_translation = db_models.Translate(translation=translation, language=language, word_id=word_id)
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation
