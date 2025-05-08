from typing import NamedTuple


class EpidocDocument(NamedTuple):
    metadata: dict[str, str]
    text: str
