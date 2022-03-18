
from setting.setting import VOCAB_BASE_FILE, AbstractController, Settings
import glob

class MinActiveWordsController(AbstractController):  # KEY_MIN_ACTIVE_WORDS
    def next(self):
        self.value = self.value + 1
        return self.value

    def previous(self):
        self.value = max(self.value - 1, 0)
        return self.value

    @staticmethod
    def get_key() -> str:
        return Settings.KEY_MIN_ACTIVE_WORDS


class FinalStageController(AbstractController):  # KEY_FINAL_STAGE
    def next(self):
        self.value = self.value + 1
        return self.value

    def previous(self):
        self.value = max(self.value - 1, 0)
        return self.value

    @staticmethod
    def get_key() -> str:
        return Settings.KEY_FINAL_STAGE


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

    @staticmethod
    def get_key() -> str:
        return Settings.KEY_SELECTED_DB

