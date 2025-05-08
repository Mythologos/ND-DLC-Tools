from utils.data.loaders.common.constants import VOWEL_MAPPING


def map_vowels(word: str) -> str:
    for key, value in VOWEL_MAPPING.items():
        word = word.replace(key, value)

    return word
