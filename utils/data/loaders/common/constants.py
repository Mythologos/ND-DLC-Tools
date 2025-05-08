
# See: https://latin.meta.stackexchange.com/questions/172/how-to-type-a-breve
# ... for capital y with breve, non-combining
VOWEL_MAPPING: dict[str, str] = {
    "ā̆": "a",   # combining
    "ā̆": "a",   # partial combination (macron a + combining breve)
    "ă": "a",   # combining
    "ă": "a",   # non-combining
    "ā": "a",   # combining
    "ā": "a",   # non-combining
    "á": "a",
    "Ā̆": "A",   # combining
    "Ā̆": "A",   # partial combination (macron A + combining breve)
    "Ā": "A",   # combining
    "Ā": "A",   # non-combining
    "Ă": "A",   # combining
    "Ă": "A",   # non-combining
    "æ": "ae",
    "Æ": "Ae",
    "ē̆": "e",   # combining
    "ē̆": "e",   # partial combination (macron e + combining breve)
    "ĕ": "e",   # combining
    "ĕ": "e",   # non-combining
    "ē": "e",   # combining
    "ē": "e",   # non-combining
    "è": "e",
    "ë": "e",
    "Ē̆": "E",   # combining
    "Ē̆": "E",   # partial combination (macron E + combining breve)
    "Ē": "E",   # combining
    "Ē": "E",   # non-combining
    "Ĕ": "E",   # combining
    "Ĕ": "E",   # non-combining
    "ī̆": "i",   # combining
    "ī̆": "i",   # partial combination (macron i + combining breve)
    "ĭ": "i",   # combining
    "ĭ": "i",   # non-combining
    "ī": "i",   # combining
    "ī": "i",   # non-combining
    "ì": "i",
    "ï": "i",
    "Ī̆": "I",   # combining
    "Ī̆": "I",   # partial combination (macron I + combining breve)
    "Ī": "I",   # combining
    "Ī": "I",   # non-combining
    "Ĭ": "I",   # combining
    "Ĭ": "I",   # non-combining
    "ō̆": "o",   # combining
    "ō̆": "o",   # partial combination (macron o + combining breve)
    "ŏ": "o",   # combining
    "ŏ": "o",   # non-combining
    "ō": "o",   # combining
    "ō": "o",   # non-combining
    "ö": "o",
    "Ō̆": "O",   # combining
    "Ō̆": "O",   # partial combination (macron O + combining breve)
    "Ō": "O",   # combining
    "Ō": "O",   # non-combining
    "Ŏ": "O",   # combining
    "Ŏ": "O",   # non-combining
    "œ": "oe",
    "ū̆": "u",   # combining
    "ū̆": "u",   # partial combination (macron u + combining breve)
    "ŭ": "u",   # combining
    "ŭ": "u",   # non-combining
    "ū": "u",   # combining
    "ū": "u",   # non-combining
    "ù": "u",
    "ü": "u",
    "û": "u",
    "Ū̆": "U",   # combining
    "Ū̆": "U",   # partial combination (macron U + combining breve)
    "Ū": "U",   # combining
    "Ū": "U",   # non-combining
    "Ŭ": "U",   # combining
    "Ŭ": "U",   # non-combining
    "ȳ̆": "y",   # combining
    "ȳ̆": "y",   # partial combination (macron y + combining breve)
    "y̆": "y",   # combining
    "ў": "y",   # non-combining
    "ȳ": "y",   # combining
    "ȳ": "y",   # non-combining
    "ÿ": "y",
    "Ȳ̆": "Y",   # combining
    "Ȳ̆": "Y",   # partial combination (macron Y + combining breve)
    "Ȳ": "Y",   # combining
    "Ȳ": "Y",   # non-combining
    "Y̆": "Y",   # combining
    "Ῠ": "Y",   # non-combining
    "︤": "",
    "︥": "",
    "͡": ""
}
