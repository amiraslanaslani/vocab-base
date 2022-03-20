from abc import ABC, abstractmethod
from typing import Callable, Type
from tinydb import TinyDB, Query


SETTINGS_FILE = './setting.json'
VOCAB_BASE_FILE = './vocab.vdb.json'  # DB names must finished with .vdb.json extention

_instance = None


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
    def get_instance(): # Singleton instance
        global _instance
        if _instance is None:
            Settings()
        return _instance

    def __init__(self):
        global _instance
        if _instance != None:
            raise Exception("This class is a singleton!")
        else:
            _instance = self

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


class AbstractController(ABC):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.value = self.settings.get(self.get_key())

    def save(self) -> None:
        self.settings.set(self.get_key(), self.get_value())
    
    def get_value(self):
        return self.value

    @staticmethod
    @abstractmethod
    def get_key() -> str:
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def previous(self):
        pass
    
    @abstractmethod
    def from_string(self, string: str):
        pass

    @staticmethod
    @abstractmethod
    def value_patinput_pattern(self) -> Callable[[int, int, str], bool]:
        pass


class SettingValueController:
    __controllers = {}

    def __init__(self, settings: Settings):
        self.settings = settings
        
    def add_controller(self, controller: Type[AbstractController]):
        self.__controllers[controller.get_key()] = controller(self.settings)

    def get(self, key) -> AbstractController:
        if isinstance(key, int):
            return list(self.__controllers.values())[key]
        else:
            return self.__controllers[key]

    def save(self) -> None:
        for key in self.__controllers:
            self.__controllers[key].save()

        

if __name__ == "__main__":
    settings = Settings()
    settings.set(Settings.KEY_MIN_ACTIVE_WORDS, 10)
    settings.set(Settings.KEY_FINAL_STAGE, 7)

