from .types import NamedEnum


class EpiDocAnalyzerMessage(NamedEnum):
    INPUT_DIRECTORY: str = "path to directory containing EpiDoc-compliant digital editions of texts"


class GeneralMessage(NamedEnum):
    # from spelling_checker.py and spelling_map_builder.py
    MAP_FILEPATH: str = "path to JSON file in which the map between Latin words and their frequencies is saved"


class LaceMessage(NamedEnum):
    DATASET_TYPE: str = "the type of dataset (e.g., OCR or post-OCR) to be processed"
    OCR_TSV_FILEPATH: str = "a path to a TSV file containing OCR data in Lace's designated format"


class LaceAnalyzerMessage(NamedEnum):
    METRICS: str = "a set of one or more metrics to be computed in dataset analysis"
    PROCESSES: str = "number of processes to be used for computing metrics; only applies to error rates"
    TSV_DIRECTORY: str = "path to directory where collection of TSV files are stored"


class LaceOCRGeneratorMessage(NamedEnum):
    IMAGE_FORMAT: str = "type of image to save as output alongside ground truth text transcriptions"
    OUTPUT_DIRECTORY: str = "path to directory where images and ground truth text transcriptions will be stored"
    VERBOSE: str = "flag indicating whether additional information about training set generation should be displayed"


class LaceTrainingCheckerMessage(NamedEnum):
    OUTPUT_FILEPATH: str = "path to file where lines with potential text duplication will be recorded"


class LaceTrainingPostprocessorMessage(NamedEnum):
    CURRENT_TSV_FILEPATH: str = "path to where TSV file to be postprocessed is stored"
    FILTER_BOOKMARKS: str = "flag to determine whether bookmark symbols will be cleaned"
    FILTER_XML_ARTIFACTS: str = "flag to determine whether XML artifacts (e.g., &amp;) will be cleaned"
    FIX_SMART_QUOTES: str = "flag to determine whether initial smart quotes will be fixed to be the correct character"
    NEW_IMAGE_DIRECTORY: str = "path to directory where images will be relocated"
    NEW_TSV_FILEPATH: str = "path to where TSV file with postprocessing changes will be stored"


class hOCRApplierMessage(NamedEnum):
    INPUT_FORMAT: str = "type of image to be supplied to Tesseract"
    INPUT_PATH: str = "path to image file or directory containing image files upon which Tesseract will be applied"
    LANGUAGES: str = "the codes corresponding to the languages for which OCR models will be applied"
    OUTPUT_DIRECTORY: str = "path to directory where hOCR files resulting from the use of Tesseract will be saved"


class PDFConverterMessage(NamedEnum):
    CROPBOX: str = "flag indicating whether to apply cropbox instead of mediabox"
    DPI: str = "dots per inch corresponding to PDF input"
    GRAYSCALE: str = "flag indicating whether to apply grayscale onto segmented images"
    INPUT_PATH: str = "path to input PDF file or directory containing PDF files"
    OUTPUT_FORMAT: str = "format of output images"
    OUTPUT_PREFIX: str = "filename prefix for output images"
    OUTPUT_DIRECTORY: str = "path to directory in which output images will be saved"
    PDF_TO_CAIRO: str = "flag indicating whether to apply Cairo instead of a Portable Pixmap (ppm)"
    STRICT_ERRORS: str = "flag indicator whether to throw exceptions on PDF syntax errors"


class SpellingCheckerMessage(NamedEnum):
    MINIMUM_DISTANCE: str = "the minimum Levenshtein distance used to indicate spelling errors"
    INPUT_FILEPATH: str = "path to a text file with a line per text unit (e.g., sentence) which will be spellchecked"
    OUTPUT_FILEPATH: str = "path to a (potentially nonexistent) text file which will contain spellchecking results"


class SpellingMapBuilderMessage(NamedEnum):
    CORPORA: str = "the names of corpora to use to compute frequencies for Latin words"
    WORDLISTS: str = "the names of wordlists to use to form the vocabulary for the spellchecker"


class WiktionaryParserMessage(NamedEnum):
    INPUT_DIRECTORY: str = "path to directory in which Latin Wiktionary pages are saved"
    OUTPUT_DIRECTORY: str = "path to directory in which parses of Latin Wiktionary pages for inflections are saved"


class WiktionaryScraperMessage(NamedEnum):
    FILTERS: str = "the names of functions to apply to filter out Wiktionary page entries"
    INPUT_FILEPATH: str = "path to file containing one or more URLs from which to extract Latin Wiktionary pages"
    OUTPUT_DIRECTORY: str = "path to directory in which scraped Latin Wiktionary pages will be saved"


class WordlistConstructorMessage(NamedEnum):
    WORDLIST: str = "the name of the wordlist to build; wordlist data is loaded and saved automatically at preset paths"
