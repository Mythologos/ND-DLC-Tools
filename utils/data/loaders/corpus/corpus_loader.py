from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from re import sub

from cltk.sentence.lat import LatinPunktSentenceTokenizer
from torch.utils.data.dataset import Dataset

from .constants import MULTISPACE_REGEX
from .types import CorpusSentence


class CorpusDataset(Dataset):
    def __init__(self, sequences: list[CorpusSentence], **options):
        self.data: list[CorpusSentence] = sequences

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int) -> CorpusSentence:
        return self.data[index]

    def __iter__(self):
        return iter(self.data)

    @abstractmethod
    def _load_dataset(self, dataset_filepath: Path, **kwargs) -> list[CorpusSentence]:
        raise NotImplementedError

    @staticmethod
    def _clean_sequence(sequence: str, **kwargs) -> list[str]:
        # We perform some basic whitespace cleaning...
        revised_sequence: str = sequence.strip().replace("\n", " ")
        revised_sequence: str = sub(MULTISPACE_REGEX, " ", revised_sequence)
        # We split clumps of sentences into individual sentences...
        sentence_tokenizer: LatinPunktSentenceTokenizer = kwargs["sentence_tokenizer"]
        tokenized_sentences: list[str] = sentence_tokenizer.tokenize(revised_sequence)
        return tokenized_sentences
