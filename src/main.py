from typing import Union
from fastapi import FastAPI
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

app = FastAPI()
API_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
API_KEY = "AIzaSyDv6Vn1MPww8ZU4aVWMrPqz1g7MGRiJ6jg"
creds = service_account.Credentials.from_service_account_file("../key_file.json")
translate_client = translate.Client(credentials=creds)


@app.get("/")
def read_root():
    result = translate_client.translate("matin", target_language="en", source_language="fr")
    return result


@app.get("/words-list")
def read_root():
    # translation = translator.translate("good morning", dest='ru')
    # print(translation.text)
    return {"List": "Words"}


@app.get("/words/{word_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"word_id": item_id, "q": q}


