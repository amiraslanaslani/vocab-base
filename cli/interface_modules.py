from datetime import datetime
from msvcrt import getch
from typing import List

from patinput import patinput
from patinput.input_pattern import ALOW_NUMBERS
from tinydb.operations import delete

from version import __version__
from cli.interface import ExitModule, MenuModule
from cli.utils import check_equal_char, clear, get_details
from cli.style import style, styles
from vocabbase import vocabbase
from setting.setting import SettingValueController
from setting.controllers import FinalStageController, MinActiveWordsController, SelectedDBController


class Exit(ExitModule):
    @staticmethod
    def get_title() -> str:
        return "Exit"

    def show(self) -> None:
        clear()
        print("Bye Bye...")


class About(MenuModule):
    @staticmethod
    def get_title() -> str:
        return ""

    def show(self) -> None:
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


class AddNewWords(MenuModule):
    TITLE_ART = """
   __     __              _       ____                 
   \\ \\   / /__   ___ __ _| |__   | __ )  __ _ ___  ___ 
    \\ \\ / / _ \\ / __/ _` | '_ \\  |  _ \\ / _` / __|/ _ \\
     \\ V / (_) | (_| (_| | |_) | | |_) | (_| \\__ \\  __/
      \\_/ \\___/ \\___\\__,_|_.__/  |____/ \\__,_|___/\\___|
"""
    api_completion = True
    custom_description = False
    
    @staticmethod
    def get_title() -> str:
        return "Add New Words"

    def _get_toggles_status(self):
        to_enable_disable = lambda e: 'Enable' if e else 'Disable'
        return style(f"API Completion [ {to_enable_disable(self.api_completion)} ]    Custom Description [ {to_enable_disable(self.custom_description)} ]\n", styles.YELLOW)

    def show(self) -> None:
        def strip_word(w: str):
            return w.lower().strip()

        def check_toggle_ascii(b) -> bool:
            update_status = lambda: print("\033[s", "\033[11;5H", "\033[0K", self._get_toggles_status(), "\033[u", end="", sep="")

            # global api_completion, custom_description
            if b == 1:
                self.api_completion = not self.api_completion
                update_status()
                return True
            elif b == 2:
                self.custom_description = not self.custom_description
                update_status()
                return True
            else:
                return False

        def interrupt(b, cursor_pos, inp):
            check_toggle_ascii(b)
            return False

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
            input_str = patinput(prompt="    Enter your word: ", interrupt=interrupt)
            w = strip_word(input_str)
            intr_result = intr(w)
            if intr_result == 1:
                return "+", "-", True
            elif intr_result == -1:
                return get_words()
            input_str = patinput(prompt="    Enter your word, again: ", interrupt=interrupt)
            r = strip_word(input_str)
            intr_result = intr(r)
            if intr_result == 1:
                return "+", "-", True
            elif intr_result == -1:
                return get_words()
            return w, r, False

        while True:
            clear()
            print(style("    [CTRL-A] Toggle API Completion    [CTRL-B] Toggle Custom Description", styles.GREEN))
            print(style("    Left fields empty to show menu choices.", styles.GREEN))
            print(self.TITLE_ART + "\n")
            print("    " + self._get_toggles_status())

            word, repeat, inter = get_words()
            while word != repeat:
                if inter:
                    return
                # print("    Inputs are not match.")
                print(style("    Inputs are not match.", styles.RED))
                word, repeat, inter = get_words()

            if self.custom_description:
                print("\n    Please enter your description about this word:")
                desciptin_value = input("    ").strip()
            else:
                desciptin_value = ""

            if self.vb.add(word, self.api_completion, desciptin_value):
                print(f"    Word `{word}` added to vocab base successfully.")
            else:
                print(f"    Word `{word}` is exists in vocab base, already!")
            print(style("    [ESC] Back to main menu   [ANY OTHER KEY] Add another word", styles.GREEN) + "\n\n")
            key = getch()
            if key == b'\x1b':
                return


class StartLearning(MenuModule):
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

    @staticmethod
    def get_title() -> str:
        return "Start Learning :)"

    def show(self) -> None:
        ws = vocabbase.WordSelector(
            self.vb,
            self.settings.get(self.settings.KEY_MIN_ACTIVE_WORDS),
            self.settings.get(self.settings.KEY_FINAL_STAGE)
        )

        for word in ws.iterate_list():
            clear()
            print(style(
                "    [ESC] Back to Menu    [1] Wrong Answer    [~`] Correct Answer    [SPACE] Show Meaning\n" +
                "    You should press keys twice (Designed in this way to prevent you from wrong key presses)\n",
                styles.GREEN) + "\n\n"
            )

            main_str, meanings, descitpions = get_details(word)
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
                        if descitpions:
                            print(style(style("    Descriptions:", styles.YELLOW), styles.BOLD))
                            print("    " + descitpions + "\n\n")

                        if meanings:
                            print(style(style("    API Dictionary:", styles.YELLOW), styles.BOLD))
                            print(meanings)

                        meaning_shown = True
                prev = new
        clear()
        print(f"\n{self.AMAZING_ART}\n\n\n    Good job! You've done all of what you should do.\n ")
        print("    See you tomorrow MASTER!\n\n\n")
        input("    Press any key to continue...")


class SettingPage(MenuModule):
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

    @staticmethod
    def get_title() -> str:
        return "Setting"

    def show(self) -> None:
        svc = SettingValueController(self.settings)
        svc.add_controller(MinActiveWordsController)
        svc.add_controller(FinalStageController)
        svc.add_controller(SelectedDBController)

        def menu_items(item: int):
            items_detail = ["", "", ""]
            items = ['  ', '  ', '  ']
            items[item] = '-►'
            return f"    {items[0]} Minimum active words at the moment       [ {svc.get(0).get_value():2} ]\n" + \
                f"    {items[1]} Final stage of a learned word            [ {svc.get(1).get_value():2} ]\n" + \
                f"    {items[2]} Selected VB (vocab base)                 [ {svc.get(2).get_value():2} ]\n" , items_detail[item]
        
        selected_item = 0
        message = ""
        while True:
            clear()
            print(style(
                "    [ESC] Main menu    [SPACE] Save    [W] Up    [S] Down\n    [A] Decrease Value   [D] Increase Value   [C] Custom Value",
                styles.GREEN
            ) + "\n\n")
            print(self.SETTING_ART)

            print(message + "\n")
            items, desc = menu_items(selected_item)
            print(items + "\n\n\n" + desc)
            key = getch()
            if check_equal_char(key, 'w'):
                selected_item = max(0, selected_item - 1)
            elif check_equal_char(key, 's'):
                selected_item = min(2, selected_item + 1)
            elif check_equal_char(key, 'a'):  # decrease value
                svc.get(selected_item).previous()
                message = style("    Your changes are not saved, yet.", styles.RED)
            elif check_equal_char(key, 'd'):  # increase value
                svc.get(selected_item).next()
                message = style("    Your changes are not saved, yet.", styles.RED)
            elif key == b' ':  # Save
                svc.save()
                message = style("    Changes are saved successfully!", styles.GREEN)
            elif check_equal_char(key, 'c'):
                print(style("       [ESC] Cancel", styles.GREEN) + "            New value: ", end="", flush=True)
                controller = svc.get(selected_item)
                interrupt = lambda key, cursor_pos, inp: key == b'\x1b'[0]
                new_value = patinput(
                    allowness=controller.value_patinput_pattern(), 
                    default=str(controller.get_value()), 
                    interrupt=interrupt
                )
                if (new_value is not None) and (new_value != ""):
                    controller.value = controller.from_string(new_value)
                    message = style("    Your changes are not saved, yet.", styles.RED)
            elif key == b'\x1b':
                return


class ManageWords(MenuModule):
    _show_from_top = 2
    _show_from_bottom = 10

    @staticmethod
    def get_title() -> str:
        return "Manage Words"

    def words_list_show(self, wlist: List, selected_index: int, selected_column: int):
        print(style(f"    {'-':5} {'Word':20} {'Description':18} {'Next Appearance':23} {'Stage':5}", styles.YELLOW))
        if len(wlist) == 0:
            print("Empty List")
            return
        from_idx = max(selected_index - self._show_from_top, 0)
        to_idx = min(selected_index + self._show_from_bottom, len(wlist))
        wlist_4_show = wlist[from_idx: to_idx]
        for word, idx in zip(wlist_4_show, range(from_idx, to_idx)):
            next_show = ""
            if "next_show" in word.data:
                dt = datetime.fromtimestamp(word.data['next_show'])
                next_show = str(dt)
            
            desc = ""
            if "description" in word.data:
                desc = "[Editable]"

            p_id, p_word, p_desc, p_next, p_stage = f"{idx+1:<5}", f" {word.word:20}", f" {desc:18}", f" {next_show:23}", f" {word.stage:<5}"
            if idx == selected_index:
                c_styles = [styles.BG_GREY]
                if selected_column == 0:
                    p_word = style(p_word, c_styles) + styles.BG_WHITE + styles.BLACK
                elif selected_column == 1:
                    p_desc = style(p_desc, c_styles) + styles.BG_WHITE + styles.BLACK
                elif selected_column == 2:
                    p_next = style(p_next, c_styles) + styles.BG_WHITE + styles.BLACK
                elif selected_column == 3:
                    p_stage = style(p_stage, c_styles) + styles.BG_WHITE + styles.BLACK

            row = f"    {p_id}{p_word}{p_desc:18}{p_next:23}{p_stage:<5}    "
            if idx == selected_index:
                row = style(row, [styles.BG_WHITE, styles.BLACK])
            print(row)

    def show(self) -> None:
        load_all_words_list = lambda: sorted([vocabbase.Word(word, self.vb, False) for word in self.vb.db.all()])
        all_words_list = load_all_words_list()
        selected_index = 0
        selected_column = 0
        search_for = ""
        searching = False
        while True:
            current_list = all_words_list if search_for.strip() == "" else list(filter(lambda k: search_for in k.word, all_words_list))
            clear()
            print(style(
                "    [ESC] Main menu    [W] Up    [S] Down    [A] Left   [D] Right\n    [Q] Search    [C] Edit/Toggle Value    [Z] Delete Word",
                styles.GREEN
            ) + "\n")

            if searching:
                print(style(f"    Search for: {'':63}", [styles.BG_YELLOW, styles.BLACK]), end="")
                print()
            elif search_for.strip() == "":
                print()
            else:
                print(style(f"    Search for: {search_for:63}", [styles.BG_YELLOW, styles.BLACK]))

            self.words_list_show(current_list, selected_index, selected_column)
            print("\n\n\n")

            if searching:
                print("\033[4;0H", end="")
                print(style(f"    Search for: {'':63}", [styles.BG_YELLOW, styles.BLACK]), end="")
                print("\033[4;17H", end="")
                search_for_new = patinput(default=search_for)
                searching = False
                if search_for_new != search_for:
                    selected_index = 0
                    search_for = search_for_new
                continue
            
            selected_word = current_list[selected_index]
            
            key = getch()
            if check_equal_char(key, 'w'):
                selected_index = max(0, selected_index - 1)
            elif check_equal_char(key, 's'):
                selected_index = min(len(current_list) - 1, selected_index + 1)
            elif check_equal_char(key, 'a'):
                selected_column = max(0, selected_column - 1)
            elif check_equal_char(key, 'd'):
                selected_column = min(3, selected_column + 1)
            elif check_equal_char(key, 'q'):
                searching = True
            elif key == b'\x1b':
                break
            elif check_equal_char(key, 'z'):
                sure = input(style("Are you sure you want to delete this word? [y/N] ", styles.YELLOW))
                if sure.strip() in ["y", 'Y']:
                    selected_word.remove()
                    all_words_list = load_all_words_list()
            elif check_equal_char(key, 'c'):
                if selected_column == 0:
                    new_value = patinput(prompt="    Edit Word: ", default=selected_word.word)
                    selected_word.update({'word': new_value})
                elif selected_column == 1:
                    if "description" in selected_word.data:
                        default_val = selected_word.data["description"]
                        prompt = "    Edit Description: "
                    else:
                        default_val = ""
                        prompt = "    Add Description: "
                    new_value = patinput(prompt=prompt, default=default_val)
                    if new_value.strip() == "":
                        selected_word.update(delete('description'))
                    else:
                        selected_word.update({'description': new_value})
                elif selected_column == 2:
                    if "next_show" in selected_word.data:
                        default_val = str(selected_word.data['next_show'])
                    else:
                        default_val = ""
                    new_value = patinput(prompt="    Edit Next Appearance: ", default=default_val, allowness=ALOW_NUMBERS)
                    if new_value.strip() != "":
                        selected_word.update({'next_show': int(new_value)})
                elif selected_column == 3:
                    new_value = patinput(prompt="    Edit Stage: ", default=str(selected_word.stage), allowness=ALOW_NUMBERS)
                    selected_word.update({'stage': int(new_value)})
                all_words_list = load_all_words_list()
