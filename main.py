from cli.interface import menu
from vocabbase import vocabbase
from vocabbase.api_word_data_retriever import dictionaryapi_dev
from setting import Settings

if __name__ == "__main__":
    settings = Settings.getInstance()
    vocabbase.API_DATA_RETRIEVER = dictionaryapi_dev
    vb = vocabbase.VocabBase(settings.get(settings.KEY_SELECTED_DB))
    menu(vb)
