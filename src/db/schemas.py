from typing import List, Union
from pydantic import BaseModel
# TODO re-check the scheme

class TranslationBase(BaseModel):
    language: str
    translation: str


class TranslationCreate(TranslationBase):
    pass


class Translation(TranslationBase):
    id: int
    word_id: int

    class Config:
        orm_mode = True



class WordBase(BaseModel):
    word: str


class WordCreate(WordBase):
    pass


class Word(WordBase):
    id: int

    class Config:
        orm_mode = True