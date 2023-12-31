from typing import List, Union
from pydantic import BaseModel

class SynonymBase(BaseModel):
    id: int
    synonym: str


class SynonymCreate(SynonymBase):
    pass


class Synonym(SynonymBase):
    id: int
    translation_id: int

    class Config:
        orm_mode = True


class TranslationBase(BaseModel):
    language: str
    translation: str
    word_id: int


class TranslationCreate(TranslationBase):
    translation: str
    language: str


class Translation(TranslationBase):
    id: int
    word_id: int
    synonyms: List[Synonym] = []

    class Config:
        orm_mode = True


class WordBase(BaseModel):
    word: str
    language: str


class WordCreate(WordBase):
    word: str


class Word(WordBase):
    id: int
    translates: List[Translation] = []

    class Config:
        orm_mode = True
