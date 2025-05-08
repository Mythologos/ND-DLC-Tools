from typing import TypeAlias, Union

from .constants import CORPUS_PATH_BASE
from .corpus_loader import CorpusDataset
from .corpus_corporum_loader import CorpusCorporumDataset
from .helpers import get_corpus_dataset
from .latin_bert_loader import LatinBERTDataset
from .mappings import NAMED_PRETRAINING_DATASET_CLASSES, NAMED_PRETRAINING_DATASET_PATHS
from .types import CorpusSentence, NamedCorpus, OrderedPath


CorpusDatasetSubclass: TypeAlias = Union[CorpusCorporumDataset, LatinBERTDataset]
