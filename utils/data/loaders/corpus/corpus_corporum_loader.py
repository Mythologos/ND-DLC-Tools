from functools import partial
from math import ceil, sqrt
from multiprocessing import Pool
from pathlib import Path
from os import cpu_count
from typing import Optional
# noinspection PyPep8Naming
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from cltk.sentence.lat import LatinPunktSentenceTokenizer
from tqdm import tqdm

from .constants import NAMESPACE_MAPPING, XML_SUFFIX
from .corpus_loader import CorpusDataset
from .types import OrderedPath, CorpusSentence


class CorpusCorporumDataset(CorpusDataset):
    def __init__(self, dataset_filepath: Optional[Path], processes: int = ceil(sqrt(cpu_count())),
                 chunk_size: int = ceil(sqrt(cpu_count()))**2, **loading_kwargs):
        sequences: list[CorpusSentence] = self._load_dataset(
            dataset_filepath, processes=processes, chunk_size=chunk_size, loading_kwargs=loading_kwargs
        )
        super().__init__(sequences)

    def _load_dataset(self, dataset_filepath: Path, **kwargs) -> list[CorpusSentence]:
        filepaths: list[OrderedPath] = self._gather_files(dataset_filepath)
        sequences: list[CorpusSentence] = []

        with Pool(processes=kwargs["processes"]) as pool:
            with tqdm(total=len(filepaths)) as completion_tracker:
                loader_partial = partial(self._load_sequences, **kwargs["loading_kwargs"])
                for result in pool.imap_unordered(loader_partial, filepaths, chunksize=kwargs["chunk_size"]):
                    sequences.extend(result)
                    completion_tracker.update()

        return sequences

    def _load_sequences(self, path_data: OrderedPath, **kwargs):
        path_number, path = path_data
        sequences: list[CorpusSentence] = []

        sentence_tokenizer: LatinPunktSentenceTokenizer = \
            LatinPunktSentenceTokenizer(strict=kwargs["sentence_tokenization"])

        xml_tree: ElementTree = ET.parse(path)
        xml_root: Element = xml_tree.getroot()
        child: Element = xml_root.find("text", NAMESPACE_MAPPING)
        checkpointed_sentence_id: int = 1
        for sequence in child.itertext():
            if sequence.isspace():
                continue
            else:
                cleaned_sentences: list[str] = self._clean_sequence(sequence, sentence_tokenizer=sentence_tokenizer)
                for sentence_index, sentence in enumerate(cleaned_sentences, start=0):
                    sentence_id: int = checkpointed_sentence_id + sentence_index
                    new_sentence: CorpusSentence = CorpusSentence(sentence, path_number, sentence_id)
                    sequences.append(new_sentence)
                else:
                    checkpointed_sentence_id += len(cleaned_sentences)

        return sequences

    @staticmethod
    def _gather_files(head_directory: Path) -> list[OrderedPath]:
        filepaths: list[OrderedPath] = []
        directories: list[Path] = [head_directory]
        while len(directories) > 0:
            current_directory: Path = directories.pop(0)
            for path in current_directory.iterdir():
                if path.is_dir():
                    directories.append(path)
                elif path.is_file() and path.suffix == XML_SUFFIX:
                    filepaths.append((len(filepaths) + 1, path))

        return filepaths
