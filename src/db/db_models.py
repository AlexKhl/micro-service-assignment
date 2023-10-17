from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=False, index=True)
    language = Column(String, unique=False, index=True)

    translation_rel = relationship("Translate", back_populates="word_rel")


class Translate(Base):
    __tablename__ = "translates"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, unique=False, index=True)
    translation = Column(String, unique=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))

    word_rel = relationship("Word", back_populates="translation_rel")
    synonyms = relationship("Synonym", back_populates="synonym_rel")


class Synonym(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, index=True)
    synonym = Column(String, unique=False, index=True)
    translation_id = Column(Integer, ForeignKey("translates.id"))

    synonym_rel = relationship("Translate", back_populates="synonyms")