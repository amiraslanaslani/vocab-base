from datetime import timedelta, datetime
import random

from tinydb import TinyDB, Query

VOCAB_BASE_FILE = './vocab.json'
API_DATA_RETRIEVER = lambda word: {}


class VocabBase:
    def __init__(self):
        self.db = TinyDB(VOCAB_BASE_FILE)
        self.q = Query()

    @staticmethod
    def __strip_word(word: str):
        return word.lower().strip()

    def add(self, word: str) -> bool:
        word = self.__strip_word(word)
        if not self.db.contains(self.q.word == word):
            self.db.insert({'word': word, 'shown': False, 'stage': 0})
            return True
        return False

    def update(self, word: str, updates: dict):
        if bool(updates):  # if not empty
            self.db.update(updates, self.q.word == word)

    def remove(self, word: str):
        word = self.__strip_word(word)
        self.db.remove(self.q.name == word)

    def get(self, word: str):
        word = self.__strip_word(word)
        result = self.db.search(self.q.word == word)
        return Word(result[0], self) if len(result) > 0 else False


class WordSelector:
    def __init__(self, vocab_base: VocabBase, min_active_words: int, final_stage: int):
        self.vb = vocab_base
        self.active_words = min_active_words
        self.final_stage = final_stage

    def get_list(self):
        current_timestamp = int(datetime.now().timestamp())
        rlist = self.vb.db.search((self.vb.q.next_show <= current_timestamp) & (self.vb.q.stage <= self.final_stage))
        needed = max(self.active_words - len(rlist), 0)
        if needed > 0:
            result = self.vb.db.search((self.vb.q.shown == False))
            choices = random.choices(result, k=min(needed, len(result)))
            rlist += choices
        random.shuffle(rlist)
        return [Word(word, self.vb) for word in rlist]


class Word:
    def __init__(self, data: dict, vocab_base: VocabBase):
        self.word = data['word']
        self.vb = vocab_base
        self.data = data
        self.stage = data['stage']
        if not ('api_completion' in data):
            self.complete_from_api()

    def update(self, updates: dict):
        self.vb.update(self.word, updates)
        self.data.update(updates)

    def complete_from_api(self):
        updates = API_DATA_RETRIEVER(self.word)
        if bool(updates):
            updates['api_completion'] = True
            self.update(updates)

    def remove(self):
        self.vb.remove(self.word)

    def show(self, correct: bool):
        self.stage = self.stage + 1 if correct else 0
        self.update({
            'shown': True,
            'last_shown': int(datetime.now().timestamp()),
            'stage': self.stage,
            'next_show': int((datetime.now() + timedelta(days=self.stage)).timestamp()),
        })

    def __str__(self):
        return f"Word({self.word})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    vb = VocabBase()
    vb.add("Hello")
    vb.add("World")
    print('hello!!')
