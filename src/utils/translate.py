import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)
import settings as conf

from googletrans import Translator

translate_client = Translator()


class LocalTrans:
    def translate(self, word: str):
        translation = translate_client.translate(text=word, dest=conf.Settings.destination_language,
                                                 src=conf.Settings.source_language)
        return translation.text
