from abc import ABC, abstractmethod
from msvcrt import getch
from typing import Type

from version import __version__
from setting.setting import Settings
from cli.style import style, styles
from cli.utils import check_equal_char, clear
from vocabbase.vocabbase import VocabBase


TITLE_ART = """
   __     __              _       ____                 
   \\ \\   / /__   ___ __ _| |__   | __ )  __ _ ___  ___ 
    \\ \\ / / _ \\ / __/ _` | '_ \\  |  _ \\ / _` / __|/ _ \\
     \\ V / (_) | (_| (_| | |_) | | |_) | (_| \\__ \\  __/
      \\_/ \\___/ \\___\\__,_|_.__/  |____/ \\__,_|___/\\___|
"""


class MenuModule(ABC):
    def __init__(self, settings: Settings, vocabbase: VocabBase) -> None:
        self.settings = settings
        self.vb = vocabbase

    @staticmethod
    @abstractmethod
    def get_title() -> str:
        pass

    @abstractmethod
    def show(self) -> None:
        pass


class ExitModule(MenuModule):
    pass
        

class MainMenu(MenuModule):
    def __init__(self, about_page: Type[MenuModule]) -> None:
        self.modules = []
        self.settings = Settings.get_instance()
        self._reload_vocabbase()
        self.about_page = about_page(self.settings, self.vb)

    @staticmethod
    def get_title() -> str:
        return "CLI Mode"

    def _reload_vocabbase(self):
        self.vb = VocabBase(self.settings.get(self.settings.KEY_SELECTED_DB))
        for module in self.modules:
            module.vb = self.vb

    def add_module(self, module: Type[MenuModule]) -> None:
        self.modules.append(
            module(
                self.settings, 
                self.vb
            )
        )

    def show(self) -> None:
        def menu_items(item: int):
            items = [' '] * len(self.modules)
            items[item] = 'X'
            result = ""
            for idx, module in enumerate(self.modules):
                result += f"\n    [{items[idx]}] {module.get_title()}"
            result += "\n\n\n"
            return result

        selected_item = 0
        while True:
            clear()
            print(style("    [W] Up    [S] Down    [ENTER] Select    [A] About", styles.GREEN) + "\n")
            print(TITLE_ART)
            print(
                style(style("\n\n    Current vocabulary base: ", styles.BOLD), styles.YELLOW) + 
                style(self.settings.get(self.settings.KEY_SELECTED_DB), styles.YELLOW)
                )
            print(menu_items(selected_item))
            key = getch()
            if check_equal_char(key, 'w'):
                selected_item = max(0, selected_item - 1)
            elif check_equal_char(key, 's'):
                selected_item = min(3, selected_item + 1)
            elif key == b'\r':
                selected_module = self.modules[selected_item]
                self._reload_vocabbase()
                selected_module.show()
                if isinstance(selected_module, ExitModule):
                    break
            elif check_equal_char(key, 'a'):
                self.about_page.show()

