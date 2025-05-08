from pathlib import Path
from typing import Type, Union

from .constants import CORPUS_PATH_BASE
from .corpus_corporum_loader import CorpusCorporumDataset
from .latin_bert_loader import LatinBERTDataset
from .types import NamedCorpus


NAMED_PRETRAINING_DATASET_PATHS: dict[str, Path] = {
    NamedCorpus.CORPUS_CORPORUM.value: CORPUS_PATH_BASE / "corpus-corporum",
    NamedCorpus.LATIN_BERT_CORPUS.value: CORPUS_PATH_BASE / "latin-bert" / "training_base.txt"
}


NAMED_PRETRAINING_DATASET_CLASSES: dict[str, Type[Union[CorpusCorporumDataset, LatinBERTDataset]]] = {
    NamedCorpus.CORPUS_CORPORUM.value: CorpusCorporumDataset,
    NamedCorpus.LATIN_BERT_CORPUS.value: LatinBERTDataset
}
