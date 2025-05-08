from pathlib import Path
from typing import NamedTuple, TypeAlias

from utils.common import NamedEnum

OrderedPath: TypeAlias = tuple[int, Path]


class NamedCorpus(NamedEnum):
    CORPUS_CORPORUM = "corpus-corporum"
    LATIN_BERT_CORPUS = "latin-bert-corpus"


class CorpusSentence(NamedTuple):
    sentence: str
    document_id: int
    item_id: int
