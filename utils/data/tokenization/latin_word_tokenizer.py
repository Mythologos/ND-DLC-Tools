from re import IGNORECASE, sub
from typing import Sequence

from nltk.tokenize.punkt import PunktLanguageVars, PunktParameters

from cltk.sentence.lat import LatinPunktSentenceTokenizer
from cltk.tokenizers.lat.params import ABBREVIATIONS, latin_exceptions as EXISTING_EXCEPTIONS, \
    latin_replacements as EXISTING_REPLACEMENTS
from cltk.tokenizers.word import WordTokenizer


class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars()._re_non_word_chars.replace("'", "")


class LatinWordTokenizer(WordTokenizer):
    """Tokenize according to rules specific to a given language."""

    ENCLITICS: Sequence[str] = ("que", "n", "ne", "ue", "ve", "st")
    EXCEPTIONS: Sequence[str] = list(set(list(ENCLITICS) + EXISTING_EXCEPTIONS))

    def __init__(self):
        self.punkt_param = PunktParameters()
        self.punkt_param.abbrev_types = set(ABBREVIATIONS)
        self.sentence_tokenizer: LatinPunktSentenceTokenizer = LatinPunktSentenceTokenizer()
        self.base_word_tokenizer: LatinLanguageVars = LatinLanguageVars()

    def tokenize(
        self,
        text: str,
        replacements: Sequence[tuple[str, str]] = tuple(EXISTING_REPLACEMENTS),
        enclitics_exceptions: Sequence[str] = EXCEPTIONS,
        enclitics: Sequence[str] = ENCLITICS,
    ) -> list[str]:
        """
        Tokenizer divides the text into a list of substrings

        :param text: This accepts the string value that needs to be tokenized
        :param replacements: List of replacements to apply to tokens such as "mecum" -> ["cum", "me"]
        :param enclitics_exceptions: List of words that look like they end with an enclitic but are not.
        :param enclitics: List of enclitics to check for in tokenization

        :returns: A list of substrings extracted from the text

        >>> toker = LatinWordTokenizer()
        >>> text = 'atque haec abuterque puerve paterne nihil'
        >>> toker.tokenize(text)
        ['atque', 'haec', 'abuter', '-que', 'puer', '-ve', 'pater', '-ne', 'nihil']

        >>> toker.tokenize('Cicero dixit orationem pro Sex. Roscio')
        ['Cicero', 'dixit', 'orationem', 'pro', 'Sex.', 'Roscio']

        >>> toker.tokenize('nihilne te nocturnum praesidium Palati')
        ['nihil', '-ne', 'te', 'nocturnum', 'praesidium', 'Palati']

        >>> toker.tokenize('Cenavin ego heri in navi in portu Persico?')
        ['Cenavi', '-ne', 'ego', 'heri', 'in', 'navi', 'in', 'portu', 'Persico', '?']

        >>> toker.tokenize('Dic si audes mihi, bellan videtur specie mulier?')
        ['Dic', 'si', 'audes', 'mihi', ',', 'bella', '-ne', 'videtur', 'specie', 'mulier', '?']

        >>> toker.tokenize("mecum")
        ['cum', 'me']

        You can specify how replacements are made using replacements

        >>> toker.tokenize("mecum", replacements=[(r"mecum", "me cum")])
        ['me', 'cum']

        Or change enclitics and enclitics exception:
        >>> toker.tokenize("atque haec abuterque puerve paterne nihil", enclitics=["que"])
        ['atque', 'haec', 'abuter', '-que', 'puerve', 'paterne', 'nihil']

        >>> toker.tokenize("atque haec abuterque puerve paterne nihil", enclitics=["que", "ve", "ne"],
        ...    enclitics_exceptions=('paterne', 'atque'))
        ['atque', 'haec', 'abuter', '-que', 'puer', '-ve', 'paterne', 'nihil']
        """

        def matchcase(word):
            """helper function From Python Cookbook"""

            def replace(matching):
                text = matching.group()
                if text.isupper():
                    return word.upper()
                elif text.islower():
                    return word.lower()
                elif text[0].isupper():
                    return word.capitalize()
                return word

            return replace

        for (original, replacement) in replacements:
            text = sub(original, matchcase(replacement), text, flags=IGNORECASE)

        sentences: list[str] = self.sentence_tokenizer.tokenize(text)
        tokens: list[str] = []

        for sentence in sentences:
            base_tokens: list[str] = self.base_word_tokenizer.word_tokenize(sentence)
            if len(base_tokens) > 0:
                # This seems to address a behavior of Punkt where ending periods are not split.
                if base_tokens[-1].endswith("."):
                    final_word = base_tokens[-1][:-1]
                    del base_tokens[-1]
                    base_tokens += [final_word, "."]

                for token in base_tokens:
                    tokens.append(token)

        encliticized_tokens: list[str] = self._handle_enclitics(tokens, enclitics, enclitics_exceptions)
        abbreviated_tokens: list[str] = self._handle_abbreviations(encliticized_tokens)
        return abbreviated_tokens

    @staticmethod
    def _handle_enclitics(
        base_tokens: list[str],
        enclitics: Sequence[str],
        exceptions: Sequence[str]
    ) -> list[str]:
        encliticized_tokens: list[str] = []

        for token in base_tokens:
            if token.lower() in exceptions:
                encliticized_tokens.append(token)
            else:
                # We iterate over enclitics to find matches.
                for enclitic in enclitics:
                    # The below assumes that we only have one enclitic per word,
                    #   which is largely a solid assumption for Latin.
                    if token.endswith(enclitic) is True:
                        ending_index: int = len(token) - len(enclitic)
                        if enclitic == "n":
                            encliticized_tokens += [token[:ending_index]] + ["-ne"]
                        elif enclitic == "st":
                            if token.endswith("ust"):
                                encliticized_tokens += [token[:ending_index + 1]] + ["est"]
                            else:
                                encliticized_tokens += [token[:ending_index]] + ["est"]
                        else:
                            encliticized_tokens += [token[:ending_index], "-" + enclitic]

                        break
                else:
                    encliticized_tokens.append(token)

        return encliticized_tokens

    def _handle_abbreviations(self, encliticized_tokens: list[str]) -> list[str]:
        # We collapse abbreviations.
        abbreviation_indices: list[int] = []
        for idx, token in enumerate(encliticized_tokens):
            if token.lower() in self.punkt_param.abbrev_types:
                abbreviation_indices.append(idx)

        for index in reversed(abbreviation_indices):
            if index + 1 < len(encliticized_tokens) and encliticized_tokens[index + 1] == ".":
                encliticized_tokens[index] = encliticized_tokens[index] + "."
                encliticized_tokens[index + 1] = ""

        abbreviated_tokens: list[str] = [token for token in encliticized_tokens if token != ""]
        return abbreviated_tokens

    @staticmethod
    def compute_indices(text: str, tokens):
        indices = []
        for i, token in enumerate(tokens):
            if 1 <= i:
                current_index = indices[-1] + len(tokens[i - 1])
                if token == "-ne":
                    indices.append(current_index + text[current_index:].find(token[1:]))
                else:
                    indices.append(current_index + text[current_index:].find(token))
            else:
                indices.append(text.find(token))
        return indices

    def tokenize_sign(self, text: str, model=None):
        raise NotImplementedError(f"Tokenization of signs not implemented for {self.__class__.__name__}.")
