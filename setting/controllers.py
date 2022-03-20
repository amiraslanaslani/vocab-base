import glob
from typing import Callable

from patinput.input_pattern import ALOW_NUMBERS, ALOW_NOSPACE

from setting.setting import VOCAB_BASE_FILE, AbstractController, Settings




class MinActiveWordsController(AbstractController):  # KEY_MIN_ACTIVE_WORDS
    def next(self):
        self.value = self.value + 1
        return self.value

    def previous(self):
        self.value = max(self.value - 1, 0)
        return self.value

    def from_string(self, string: str):
        return int(string)

    @staticmethod
    def get_key() -> str:
        return Settings.KEY_MIN_ACTIVE_WORDS
        
    @staticmethod
    def value_patinput_pattern() -> Callable[[int, int, str], bool]:
        return ALOW_NUMBERS


class FinalStageController(AbstractController):  # KEY_FINAL_STAGE
    def next(self):
        self.value = self.value + 1
        return self.value

    def previous(self):
        self.value = max(self.value - 1, 0)
        return self.value

    def from_string(self, string: str):
        return int(string)

    @staticmethod
    def get_key() -> str:
        return Settings.KEY_FINAL_STAGE
        
    @staticmethod
    def value_patinput_pattern() -> Callable[[int, int, str], bool]:
        return ALOW_NUMBERS


class SelectedDBController(AbstractController):  # KEY_SELECTED_DB
    def get_databases(self) -> list:
        result = glob.glob("*.vdb.json")
        if len(result) == 0:
            result = [VOCAB_BASE_FILE]
        return result

    def next(self):
        dbs = self.get_databases()
        if self.value in dbs:
            self.value = dbs[(dbs.index(self.value) + 1) % len(dbs)]
        else:
            self.value = dbs[0]
        return self.value

    def previous(self):
        dbs = self.get_databases()
        if self.value in dbs:
            self.value = dbs[dbs.index(self.value) - 1]
        else:
            self.value = dbs[0]
        return self.value

    def from_string(self, string: str):
        return string

    @staticmethod
    def get_key() -> str:
        return Settings.KEY_SELECTED_DB
        
    @staticmethod
    def value_patinput_pattern() -> Callable[[int, int, str], bool]:
        return ALOW_NOSPACE

