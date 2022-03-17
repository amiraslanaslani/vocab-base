from msvcrt import getch

from version import __version__
from setting import Settings
from cli.style import style, styles
from cli.utils import clear, get_details
from vocabbase import vocabbase
from vocabbase.vocabbase import VocabBase

AMAZING_ART = """
   $$$$$$\\                                    $$\\                     $$\\ 
  $$  __$$\\                                   \\__|                    $$ |
  $$ /  $$ |$$$$$$\\$$$$\\   $$$$$$\\  $$$$$$$$\\ $$\\ $$$$$$$\\   $$$$$$\\  $$ |
  $$$$$$$$ |$$  _$$  _$$\\  \\____$$\\ \\____$$  |$$ |$$  __$$\\ $$  __$$\\ $$ |
  $$  __$$ |$$ / $$ / $$ | $$$$$$$ |  $$$$ _/ $$ |$$ |  $$ |$$ /  $$ |\\__|
  $$ |  $$ |$$ | $$ | $$ |$$  __$$ | $$  _/   $$ |$$ |  $$ |$$ |  $$ |    
  $$ |  $$ |$$ | $$ | $$ |\\$$$$$$$ |$$$$$$$$\\ $$ |$$ |  $$ |\\$$$$$$$ |$$\\ 
  \\__|  \\__|\\__| \\__| \\__| \\_______|\\________|\\__|\\__|  \\__| \\____$$ |\\__|
                                                            $$\\   $$ |    
                                                            \\$$$$$$  |    
                                                             \\______/     
"""
TITLE_ART = """
   __     __              _       ____                 
   \\ \\   / /__   ___ __ _| |__   | __ )  __ _ ___  ___ 
    \\ \\ / / _ \\ / __/ _` | '_ \\  |  _ \\ / _` / __|/ _ \\
     \\ V / (_) | (_| (_| | |_) | | |_) | (_| \\__ \\  __/
      \\_/ \\___/ \\___\\__,_|_.__/  |____/ \\__,_|___/\\___|
"""
SETTING_ART = """
      ██████ ▓█████▄▄▄█████▓▄▄▄█████▓ ██▓ ███▄    █   ▄████ 
    ▒██    ▒ ▓█   ▀▓  ██▒ ▓▒▓  ██▒ ▓▒▓██▒ ██ ▀█   █  ██▒ ▀█▒
    ░ ▓██▄   ▒███  ▒ ▓██░ ▒░▒ ▓██░ ▒░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
      ▒   ██▒▒▓█  ▄░ ▓██▓ ░ ░ ▓██▓ ░ ░██░▓██▒  ▐▌██▒░▓█  ██▓
    ▒██████▒▒░▒████▒ ▒██▒ ░   ▒██▒ ░ ░██░▒██░   ▓██░░▒▓███▀▒
    ▒ ▒▓▒ ▒ ░░░ ▒░ ░ ▒ ░░     ▒ ░░   ░▓  ░ ▒░   ▒ ▒  ░▒   ▒ 
    ░ ░▒  ░ ░ ░ ░  ░   ░        ░     ▒ ░░ ░░   ░ ▒░  ░   ░ 
    ░  ░  ░     ░    ░        ░       ▒ ░   ░   ░ ░ ░ ░   ░ 
          ░     ░  ░                  ░           ░       ░  
"""

vb: VocabBase = None
settings = Settings.getInstance()


def about_page():
    clear()
    print(style(
        "    [ANY KEY] Back to Menu\n",
        styles.GREEN) + "\n"
    )
    print(f"""
    ██╗░░░██╗░█████╗░░█████╗░░█████╗░██████╗░
    ██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    ╚██╗░██╔╝██║░░██║██║░░╚═╝███████║██████╦╝
    ░╚████╔╝░██║░░██║██║░░██╗██╔══██║██╔══██╗
    ░░╚██╔╝░░╚█████╔╝╚█████╔╝██║░░██║██████╦╝
    ░░░╚═╝░░░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
    
    ██████╗░░█████╗░░██████╗███████╗
    ██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██████╦╝███████║╚█████╗░█████╗░░
    ██╔══██╗██╔══██║░╚═══██╗██╔══╝░░
    ██████╦╝██║░░██║██████╔╝███████╗
    ╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝
    
    
    Vocab Base -- version {__version__}
    Created 4U with ♥ by A. A. Aslani
    
    https://amiraslan.ir
    https://github.com/amiraslanaslani/vocab-base
    """)
    getch()
    return


def start_learning():
    ws = vocabbase.WordSelector(
        vb,
        settings.get(settings.KEY_MIN_ACTIVE_WORDS),
        settings.get(settings.KEY_FINAL_STAGE)
    )

    for word in ws.iterate_list():
        clear()
        print(style(
            "    [ESC] Back to Menu    [1] Wrong Answer    [~`] Correct Answer    [SPACE] Show Meaning\n" +
            "    You should press keys twice (Designed in this way to prevent you from wrong key presses)\n",
            styles.GREEN) + "\n\n"
        )

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
                    ws.repeat_word(word)
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
    def strip_word(w: str):
        return w.lower().strip()

    def intr(w: str) -> int:
        if w == "":
            print(style("    [ESC] Back to main menu   [ANY OTHER KEY] Continue", styles.GREEN) + "\n\n")
            k = getch()
            if k == b'\x1b':  # ESC
                return 1
            else:
                return -1  # repeat
        return 0

    def get_words():
        w = strip_word(input("    Enter your word: "))
        intr_result = intr(w)
        if intr_result == 1:
            return "+", "-", True
        elif intr_result == -1:
            return get_words()
        r = strip_word(input("    Enter your word, again: "))
        intr_result = intr(r)
        if intr_result == 1:
            return "+", "-", True
        elif intr_result == -1:
            return get_words()
        return w, r, False

    while True:
        clear()
        print(style("    Left fields empty to show menu choices.", styles.GREEN))
        print(TITLE_ART + "\n\n")

        word, repeat, inter = get_words()
        while word != repeat:
            if inter:
                return
            # print("    Inputs are not match.")
            print(style("    Inputs are not match.", styles.RED))
            word, repeat, inter = get_words()

        if vb.add(word):
            print(f"    Word `{word}` added to vocab base successfully.")
        else:
            print(f"    Word `{word}` is exists in vocab base, already!")
        print(style("    [ESC] Back to main menu   [ANY OTHER KEY] Add another word", styles.GREEN) + "\n\n")
        key = getch()
        if key == b'\x1b':
            return


def setting_page():
    keys = [
        settings.KEY_MIN_ACTIVE_WORDS,
        settings.KEY_FINAL_STAGE
    ]

    values = [
        settings.get(keys[0]),
        settings.get(keys[1])
    ]

    def menu_items(item: int):
        items_detail = ["", ""]
        items = ['  ', '  ']
        items[item] = '-►'
        return f"    {items[0]} Minimum active words at the moment       [ {values[0]:2} ]\n" + \
               f"    {items[1]} Final stage of a learned word            [ {values[1]:2} ]\n", items_detail[item]

    selected_item = 0
    message = ""
    while True:
        clear()
        print(style(
            "    [ESC] Main menu    [SPACE] Save    [W] Up    [S] Down\n    [A] Decrease Value   [D] Increase Value",
            styles.GREEN
        ) + "\n\n")

        print(SETTING_ART)

        print(message + "\n")
        items, desc = menu_items(selected_item)
        print(items + "\n\n\n" + desc)
        key = getch()
        if key == b'w' or key == b'W':
            selected_item = max(0, selected_item - 1)
        elif key == b's' or key == b'S':
            selected_item = min(1, selected_item + 1)
        elif key == b'a' or key == b'A':  # decrease value
            values[selected_item] = max(values[selected_item] - 1, 0)
            message = style("    Your changes are not saved, yet.", styles.RED)
        elif key == b'd' or key == b'D':  # increase value
            values[selected_item] = values[selected_item] + 1
            message = style("    Your changes are not saved, yet.", styles.RED)
        elif key == b' ':  # Save
            for key, value in zip(keys, values):
                settings.set(key, value)
            message = style("    Changes are saved successfully!", styles.GREEN)
        elif key == b'\x1b':
            return


def menu(vocabbase_instance: VocabBase):
    global vb
    vb = vocabbase_instance

    def menu_items(item: int):
        items = [' ', ' ', ' ', ' ']
        items[item] = 'X'
        return f"\n\n\n    [{items[0]}] Start Learning :)\n    [{items[1]}] Add New Words\n" + \
               f"    [{items[2]}] Setting\n    [{items[3]}] Exit\n\n\n"

    selected_item = 0
    while True:
        clear()
        print(style("    [W] Up    [S] Down    [ENTER] Select    [A] About", styles.GREEN) + "\n\n")
        print(TITLE_ART)
        print(menu_items(selected_item))
        key = getch()
        if key == b'w' or key == b'W':
            selected_item = max(0, selected_item - 1)
        elif key == b's' or key == b'S':
            selected_item = min(3, selected_item + 1)
        elif key == b'\r':
            if selected_item == 0:
                start_learning()
            elif selected_item == 1:
                add_words()
            elif selected_item == 2:
                setting_page()
            elif selected_item == 3:
                clear()
                print("Bye Bye...")
                break
        elif key == b'a' or key == b'A':
            about_page()
