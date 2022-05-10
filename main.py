import argparse

from webservice import core as webapp
from cli.interface import MainMenu
from cli.interface_modules import Exit, About, AddNewWords, StartLearning, SettingPage, ManageWords, Statistics
from vocabbase import vocabbase
from vocabbase.api_word_data_retriever import dictionaryapi_dev


def start_cli():
    vocabbase.API_DATA_RETRIEVER = dictionaryapi_dev
    menu = MainMenu(About)  # CLI menu
    menu.add_module(StartLearning)
    menu.add_module(ManageWords)
    menu.add_module(Statistics)
    menu.add_module(AddNewWords)
    menu.add_module(SettingPage)
    menu.add_module(Exit)
    menu.show()


def start_webapp():
    webapp.initialize()
    webapp.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'VocabBase',
        description='You could vast your vocabulary knowledge easily!'
    )

    parser.add_argument('-w', '--webapp', action='store_true')
    args = parser.parse_args()

    if args.webapp:
        start_webapp()
    else:
        start_cli()
    
