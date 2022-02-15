from tinydb import TinyDB, Query


VOCAB_BASE_FILE = './vocab.json'
API_DATA_RETRIEVER = lambda word: {}


class VocabBase:
    def __init__(self):
        self.db = TinyDB(VOCAB_BASE_FILE)
        self.q = Query()

    def _strip_word(self, word: str):
        return word.lower().strip()

    def add(self, word: str) -> bool:
        word = self._strip_word(word)
        if not vb.db.contains(self.q.word == word):
            self.db.insert({'word': word})
            return True
        return False

    def update(self, word: str, updates: dict):
        if bool(updates):  # if not empty
            self.db.update(updates, self.q.word == word)

    def remove(self, word: str):
        word = self._strip_word(word)
        self.db.remove(self.q.name == word)

    def get(self, word: str):
        word = self._strip_word(word)
        result = self.db.search(self.q.word == word)
        return Word(result[0], self) if len(result) > 0 else False


class Word:
    def __init__(self, data: dict, vocab_base: VocabBase):
        self.word = data['word']
        self.vb = vocab_base

    def update(self, updates: dict):
        self.vb.update(self.word, updates)

    def complete_from_api(self):
        updates = API_DATA_RETRIEVER(self.word)
        self.update(updates)

    def remove(self):
        self.vb.remove(self.word)

    def __str__(self):
        return f"Word({self.word})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    vb = VocabBase()
    vb.add("Hello")
    vb.add("World")
