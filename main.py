from os import system, name
from msvcrt import getch

import vocabbase
from api_word_data_retriever import dictionaryapi_dev
from style import styles, style


AMAZING_ART = """
   $$$$$$\                                    $$\                     $$\ 
  $$  __$$\                                   \__|                    $$ |
  $$ /  $$ |$$$$$$\$$$$\   $$$$$$\  $$$$$$$$\ $$\ $$$$$$$\   $$$$$$\  $$ |
  $$$$$$$$ |$$  _$$  _$$\  \____$$\ \____$$  |$$ |$$  __$$\ $$  __$$\ $$ |
  $$  __$$ |$$ / $$ / $$ | $$$$$$$ |  $$$$ _/ $$ |$$ |  $$ |$$ /  $$ |\__|
  $$ |  $$ |$$ | $$ | $$ |$$  __$$ | $$  _/   $$ |$$ |  $$ |$$ |  $$ |    
  $$ |  $$ |$$ | $$ | $$ |\$$$$$$$ |$$$$$$$$\ $$ |$$ |  $$ |\$$$$$$$ |$$\ 
  \__|  \__|\__| \__| \__| \_______|\________|\__|\__|  \__| \____$$ |\__|
                                                            $$\   $$ |    
                                                            \$$$$$$  |    
                                                             \______/     
"""

TITLE_ART = """
   __     __              _       ____                 
   \ \   / /__   ___ __ _| |__   | __ )  __ _ ___  ___ 
    \ \ / / _ \ / __/ _` | '_ \  |  _ \ / _` / __|/ _ \\
     \ V / (_) | (_| (_| | |_) | | |_) | (_| \__ \  __/
      \_/ \___/ \___\__,_|_.__/  |____/ \__,_|___/\___|
"""


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


def start_learning():
    ws = vocabbase.WordSelector(vb, 10, 7)
    for word in ws.get_list():
        clear()
        print(style("    [ESC] Back to Menu    [1] Wrong Answer    [~`] Correct Answer    [SPACE] Show Meaning"
                    , styles.GREEN) + "\n\n")
        main_str, meanings = get_details(word)
        print(main_str)

        prev = getch()
        meaning_shown = False
        while True:
            new = getch()
            if new == prev:
                if new == b'\x1b':  # ESC
                    return
                elif new == b'1':
                    word.show(False)
                    break
                elif new == b'`':  # `~
                    word.show(True)
                    break
                elif new == b' ' and not meaning_shown:  # SPACE
                    print(meanings)
                    meaning_shown = True
            prev = new
    clear()
    print(f"\n{AMAZING_ART}\n\n\n    Good job! You've done all of what you should do.\n ")
    print("    See you tomorrow MASTER!\n\n\n")
    input("    Press any key to continue...")


def add_words():
    def strip_word(word: str):
        return word.lower().strip()

    def intr(word: str) -> int:
        if word == "":
            print(style("    [ESC] Back to main menu   [ANY OTHER KEY] Continue", styles.GREEN) + "\n\n")
            key = getch()
            if key == b'\x1b':  # ESC
                return 1
            else:
                return -1  # repeat
        return 0

    def get_words():
        word = strip_word(input("    Enter your word:"))
        intr_result = intr(word)
        if intr_result == 1:
            return "+", "-", True
        elif intr_result == -1:
            return get_words()
        repeat = strip_word(input("    Enter your word, again:"))
        intr_result = intr(repeat)
        if intr_result == 1:
            return "+", "-", True
        elif intr_result == -1:
            return get_words()
        return word, repeat, False

    while True:
        clear()
        print(style("    Left fields empty to show menu choices.", styles.GREEN))
        print(TITLE_ART + "\n\n")

        word, repeat, inter = get_words()
        while word != repeat:
            if inter:
                return
            print("    Inputs are not match.")
            word, repeat, inter = get_words()

        if vb.add(word):
            print(f"    Word `{word}` added to vocab base successfully.")
        else:
            print(f"    Word `{word}` is exists in vocab base, already!")
        print(style("    [ESC] Back to main menu   [ANY OTHER KEY] Add another word", styles.GREEN) + "\n\n")
        key = getch()
        if key == b'\x1b':
            return


def menu():
    def menu_items(item: int):
        items = [' ', ' ', ' ']
        items[item] = 'X'
        return f"\n\n\n    [{items[0]}] Start Learning :)\n    [{items[1]}] Add New Words\n    [{items[2]}] Exit\n\n\n"

    selected_item = 0
    while True:
        clear()
        print(style("    [W] Up    [S] Down    [ENTER] Select", styles.GREEN) + "\n\n")
        print(TITLE_ART)
        print(menu_items(selected_item))
        key = getch()
        if key == b'w' or key == b'W':
            selected_item = max(0, selected_item - 1)
        elif key == b's' or key == b'S':
            selected_item = min(2, selected_item + 1)
        elif key == b'\r':
            if selected_item == 0:
                start_learning()
            elif selected_item == 1:
                add_words()
            elif selected_item == 2:
                clear()
                print("Bye Bye...")
                break


vocabbase.API_DATA_RETRIEVER = dictionaryapi_dev
vb = vocabbase.VocabBase()
menu()
# add_words()
# start_learning()
