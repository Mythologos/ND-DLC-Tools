from pathlib import Path
from typing import Type, Union

from .corpus_corporum_loader import CorpusCorporumDataset
from .latin_bert_loader import LatinBERTDataset
from .mappings import NAMED_PRETRAINING_DATASET_CLASSES, NAMED_PRETRAINING_DATASET_PATHS


def get_corpus_dataset(name: str) -> tuple[Path, Type[Union[CorpusCorporumDataset, LatinBERTDataset]]]:
    try:
        named_dataset_path: Path = NAMED_PRETRAINING_DATASET_PATHS[name]
        named_dataset_class: Type[Union[CorpusCorporumDataset, LatinBERTDataset]] = \
            NAMED_PRETRAINING_DATASET_CLASSES[name]
    except KeyError:
        raise ValueError(f"The dataset named <{name}> is not recognized.")
    return named_dataset_path, named_dataset_class
