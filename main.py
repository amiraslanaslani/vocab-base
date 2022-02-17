from cli.interface import menu
from cli.setting import Settings
from vocabbase import vocabbase
from vocabbase.api_word_data_retriever import dictionaryapi_dev

if __name__ == "__main__":
    vocabbase.API_DATA_RETRIEVER = dictionaryapi_dev
    vb = vocabbase.VocabBase()
    settings = Settings()
    menu()
