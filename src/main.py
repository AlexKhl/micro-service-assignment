from typing import Union
from fastapi import FastAPI
from googletrans import Translator
from settings import Settings as conf

app = FastAPI()
translate_client = Translator()


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
