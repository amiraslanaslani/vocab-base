from os import name, system

from cli.style import style, styles
from vocabbase import vocabbase


def clear():
    if name == 'nt':  # for windows
        _ = system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        _ = system('clear')


def get_details(word: vocabbase.Word):
    if "phonetic" in word.data:
        phonetic = f"[ {word.data['phonetic']} ]"
    else:
        phonetic = ""

    meanings = ""
    if 'meanings' in word.data:
        for meaning in word.data['meanings']:
            definition_str = ""
            for definition in meaning['definitions']:
                definition_str += f"    {definition['definition']}\n    Example: {definition['example']}"
                definition_str += "\n\n"
            meanings += f"    [ {meaning['partOfSpeech']} ]\n" + definition_str
            meanings += "\n"

    main_str = f"\n\n    {style(word.word.title(), styles.BOLD)}       {phonetic}\n\n\n"
    return main_str, meanings
