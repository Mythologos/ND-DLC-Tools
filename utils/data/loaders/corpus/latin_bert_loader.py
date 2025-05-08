from pathlib import Path

from cltk.sentence.lat import LatinPunktSentenceTokenizer
from tqdm import tqdm

from .corpus_loader import CorpusDataset
from .types import CorpusSentence


class LatinBERTDataset(CorpusDataset):
    def __init__(self, dataset_filepath: Path, **loading_kwargs):
        sequences: list[CorpusSentence] = self._load_dataset(dataset_filepath, **loading_kwargs)
        super().__init__(sequences)

    def _load_dataset(self, dataset_filepath: Path, **kwargs) -> list[CorpusSentence]:
        data: list[CorpusSentence] = []
        document_id: int = 0
        checkpointed_sentence_id: int = 1
        sentence_tokenizer: LatinPunktSentenceTokenizer = \
            LatinPunktSentenceTokenizer(strict=kwargs["sentence_tokenization"])

        with dataset_filepath.open(encoding="utf-8", mode="r") as dataset_file:
            for line in tqdm(dataset_file, "Dataset Loading (Lines)"):
                if line.isspace():
                    document_id += 1
                    checkpointed_sentence_id: int = 1
                else:
                    cleaned_sentences: list[str] = self._clean_sequence(line, sentence_tokenizer=sentence_tokenizer)
                    for sentence_index, sentence in enumerate(cleaned_sentences):
                        sentence_id: int = checkpointed_sentence_id + sentence_index
                        new_sentence: CorpusSentence = CorpusSentence(sentence, document_id, sentence_id)
                        data.append(new_sentence)
                    else:
                        checkpointed_sentence_id += len(cleaned_sentences)

        return data
