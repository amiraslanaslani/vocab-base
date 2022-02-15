import requests


def dictionaryapi_dev(word: str) -> dict:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url).json()
    if isinstance(response, list) and len(response) > 0:
        return {
            'phonetic': response[0]['phonetic'],
            'meanings': response[0]['meanings'],
        }
    else:
        return {}


if __name__ == "__main__":
    print(dictionaryapi_dev('dfghjkljgj'))
    print(dictionaryapi_dev('hello'))
