from tinydb import TinyDB, Query

from vocabbase.vocabbase import VOCAB_BASE_FILE


SETTINGS_FILE = './setting.json'
instance = None


class Settings:

    KEY_MIN_ACTIVE_WORDS = "min_active_words"
    KEY_FINAL_STAGE = "final_stage"
    KEY_SELECTED_DB = "selected_db"

    __defaults = {
        KEY_MIN_ACTIVE_WORDS: 10,
        KEY_FINAL_STAGE: 7,
        KEY_SELECTED_DB: VOCAB_BASE_FILE,
    }

    @staticmethod 
    def getInstance(): # Singleton instance
        global instance
        if instance is None:
            Settings()
        return instance

    def __init__(self):
        global instance
        if instance != None:
            raise Exception("This class is a singleton!")
        else:
            instance = self

        self.db = TinyDB(SETTINGS_FILE)
        self.q = Query()
        for key in self.__defaults:
            if not self.contains(key):
                self.set(key, self.__defaults[key])

    def set(self, key: str, value):
        if self.contains(key):
            self.db.update({"value": value}, self.q.key == key)
        else:
            self.db.insert({'key': key, 'value': value})

    def get(self, key: str):
        return self.db.search(self.q.key == key)[0]['value']

    def contains(self, key: str):
        return self.db.contains(self.q.key == key)

    

if __name__ == "__main__":
    settings = Settings()
    settings.set(Settings.KEY_MIN_ACTIVE_WORDS, 10)
    settings.set(Settings.KEY_FINAL_STAGE, 7)

