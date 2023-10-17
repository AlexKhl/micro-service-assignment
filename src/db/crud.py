import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
import settings as conf

sys.path.append('utils/')
import translate as trans

from sqlalchemy.orm import Session, joinedload, defaultload, lazyload, relationship, contains_eager, outerjoin
from . import db_models, schemas


def get_word(db: Session, word: str):
    return db.query(db_models.Word).filter(db_models.Word.word == word).first()


def get_words(db: Session, query_string='__ALL__', page=1, page_size: int = 50, skip: int = 0, limit: int = 100):
    if query_string == '__ALL__':
        return db.query(db_models.Word).order_by(db_models.Word.word).offset((page - 1) * page_size).limit(
            page_size).all()
    else:
        return db.query(db_models.Word).filter(db_models.Word.word.ilike(f"%{query_string}%")).order_by(
            db_models.Word.word).offset((page - 1) * page_size).limit(page_size).all()


def get_words_with_synonyms(db: Session, query_string='__ALL__', page=1, page_size: int = 50, skip: int = 0, limit: int = 100):
    result = (db.query(db_models.Word, db_models.Translate)
            .filter(db_models.Word.word.ilike(f"%{query_string}%"))
            .join(db_models.Word.translation_rel)
            .order_by(db_models.Translate.translation)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
            )
    words_with_synonyms = []
    for word, translation in result:
        words_with_synonyms.append({
            "id": word.id,
            "word_id": word.id,
            "word": word.word,
            "language": word.language,
            "translation_id": translation.id,
            "translation": translation.translation,
            "synonyms": [synonym.synonym for synonym in translation.synonyms]
        })
    return words_with_synonyms



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


def delete_word(db: Session, word: str):
    item = db.query(db_models.Word).filter(db_models.Word.word == word).first()
    if item:
        db.delete(item)
        db.commit()
        return {"word": item.word, "status": "deleted"}
    else:
        return {"word": item.word, "status": "not found"}


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
