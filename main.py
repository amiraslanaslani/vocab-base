from cli.interface import MainMenu
from cli.interface_modules import Exit, About, AddNewWords, StartLearning, SettingPage
from vocabbase import vocabbase
from vocabbase.api_word_data_retriever import dictionaryapi_dev

if __name__ == "__main__":
    vocabbase.API_DATA_RETRIEVER = dictionaryapi_dev
    menu = MainMenu(About)  # CLI menu
    menu.add_module(StartLearning)
    menu.add_module(AddNewWords)
    menu.add_module(SettingPage)
    menu.add_module(Exit)
    menu.show()
    