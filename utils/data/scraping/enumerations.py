from utils.common import NamedEnum


class FilterType(NamedEnum):
    AFFIX: str = "affix"
    NONALPHABETIC: str = "non-alphabetic"
    MULTIWORD: str = "multiword"
    RECONSTRUCTION: str = "reconstruction"
