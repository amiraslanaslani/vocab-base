from tinydb import TinyDB, Query


SETTINGS_FILE = './setting.json'


class Settings:
    KEY_MIN_ACTIVE_WORDS = "min_active_words"
    KEY_FINAL_STAGE = "final_stage"

    __defaults = {
        KEY_MIN_ACTIVE_WORDS: 10,
        KEY_FINAL_STAGE: 7,
    }

    def __init__(self):
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

