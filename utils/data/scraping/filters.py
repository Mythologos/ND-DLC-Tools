from .enumerations import FilterType
from .types import FilterFunction

FILTER_MAPPING: dict[str, FilterFunction] = {
    FilterType.AFFIX: lambda word: word.startswith("-") or word.endswith("-"),
    FilterType.MULTIWORD: lambda word: word.count(" ") > 0,
    FilterType.NONALPHABETIC: lambda word: not word.isalpha(),
    FilterType.RECONSTRUCTION: lambda word: word.startswith("Reconstruction:Latin/")
}
