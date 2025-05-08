from typing import Sequence

CORRECTION_ELEMENT_XPATH: str = ".//corr"
ENTRY_ELEMENT_XPATH: str = ".//entryFree"
ORTHOGRAPHY_ELEMENT_XPATH: str = ".//orth"

MISCELLANEOUS_CHARACTERS: Sequence[str] = ("?", "!", ".", "=", "—", "/", "1", "^", "†", "_")
ENTRY_MARKERS: Sequence[str] = \
    ("anteclass.", "class.", "dissyl.", "dissyll.", "trisyl.", "trisyll.", "quadrisyl.", "quinquesyl.",  "sc.")
PARTIAL_FORMS: Sequence[str] = ("adc.", "adqu.", "delin.")
ERRONEOUS_FORMS: Sequence[str] = ("acc", "b. inaugŭrāto", "i. e")
