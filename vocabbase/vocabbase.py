from datetime import timedelta, datetime
import random
from typing import Callable, Union

from tinydb import TinyDB, Query


API_DATA_RETRIEVER = lambda word: {}


class VocabBase:
    def __init__(self, file):
        self.db = TinyDB(file)
        self.q = Query()

    @staticmethod
    def __strip_word(word: str):
        return word.lower().strip()

    def add(self, word: str, api_completion_needed: bool = True, description: str = "") -> bool:
        word = self.__strip_word(word)
        if not self.db.contains(self.q.word == word):
            data = {
                'word': word, 
                'shown': False, 
                'stage': 0, 
                'api_completion_needed': api_completion_needed
            }
            if description.strip():
                data['description'] = description.strip()
            self.db.insert(data)
            return True
        return False

    def update(self, word: str, updates: dict):
        if bool(updates):  # if not empty
            self.db.update(updates, self.q.word == word)

    def remove(self, word: str):
        word = self.__strip_word(word)
        self.db.remove(self.q.word == word)

    def get(self, word: str):
        word = self.__strip_word(word)
        result = self.db.search(self.q.word == word)
        return Word(result[0], self) if len(result) > 0 else False


class WordSelector:
    def __init__(self, vocab_base: VocabBase, min_active_words: int, final_stage: int):
        self.vb = vocab_base
        self.active_words = min_active_words
        self.final_stage = final_stage
        self.lists = {}
        self.lists_len = {}

    def create_list(self, id):
        current_timestamp = int(datetime.now().timestamp())
        rlist = self.vb.db.search((self.vb.q.next_show <= current_timestamp) & (self.vb.q.stage <= self.final_stage))
        needed = max(self.active_words - len(rlist), 0)
        if needed > 0:
            result = self.vb.db.search((self.vb.q.shown == False))
            choices = random.sample(result, k=min(needed, len(result)))
            rlist += choices
        random.shuffle(rlist)
        self.lists[id] = [Word(word, self.vb) for word in rlist]
        self.lists_len[id] = len(self.lists[id])

    def get_list(self, complete: bool=False, id=1):
        if id not in self.lists:
            self.create_list(id)
        if complete:
            return self.lists[id]
        return self.lists[id][:self.lists_len[id]]

    def iterate_list(self, id=1):
        words_list = self.get_list(complete=True, id=id)
        for item in words_list:
            yield item

    def repeat_word(self, word: "Word", list_id=1):
        self.get_list(complete=True, id=list_id).append(word)


class Word:
    def __init__(self, data: dict, vocab_base: VocabBase, load=True):
        self.word = data['word']
        self.vb = vocab_base
        self.data = data
        self.stage = data['stage']
        self.api_completion_needed = bool(data['api_completion_needed'])
        if load and ('api_completion' not in data) and data['api_completion_needed']:
            self.complete_from_api()

    def update(self, updates: Union[dict, Callable]):
        self.vb.update(self.word, updates)
        if callable(updates):
            updates(self.data)
        else:
            self.data.update(updates)

    def complete_from_api(self):
        updates = API_DATA_RETRIEVER(self.word)
        if bool(updates):
            updates['api_completion'] = True
            self.update(updates)

    def remove(self):
        self.vb.remove(self.word)

    def show(self, correct: bool, delta_func=None):
        self.stage = self.stage + 1 if correct else 0
        if correct:
            if not callable(delta_func):
                delta_func = lambda stage: timedelta(days=self.stage)
        else:
            delta_func = lambda stage: timedelta(days=0)

        self.update({
            'shown': True,
            'last_shown': int(datetime.now().timestamp()),
            'stage': self.stage,
            'next_show': int((datetime.now() + delta_func(self.stage)).timestamp()),
        })

    def __str__(self):
        return f"Word({self.word})"

    def __lt__(self, other):
        return self.word < other.word

    def __eq__(self, other):
        return self.word == other.word

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    vb = VocabBase("./test.json")
    vb.add("Hello")
    vb.add("World")
    vb.add("Friends")
    vb.add("Life")
    vb.add("Draft")
    vb.add("Walk")
    vb.add("Magic")
    list = [Word(word, vb) for word in vb.db.all()]
    print(sorted(list))
    ws = WordSelector(vb, 5, 3)
    for idx, word in enumerate(ws.iterate_list()):
        print(idx, word)
        if idx in [0, 2]:
            ws.repeat_word(word)
