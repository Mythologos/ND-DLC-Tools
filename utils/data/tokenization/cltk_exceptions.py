from cltk.tokenizers.lat.params import latin_exceptions as EXISTING_EXCEPTIONS


CUSTOM_ENCLITICS: list[str] = ["que", "ue", "ve"]

CUSTOM_LATIN_EXCEPTIONS: list[str] = [
    "Aaron", "Abessalon", "Abiron", "accessione", "achaten",  "acumen", "Aenon", "afflictione", "allegorian",
    "Ain", "Aman", "amen", "Ammaon", "Amnon", "antidoton", "assumptione", "Auxen",
    "Babylon", "Babylone", "Basan", "Belamon", "Beniamin", "bitumine", "bitumen", "Borean",
    "Cain", "carne", "chamaeleon", "Chanaan", "Charybdin", "Cherubin", "Chorazain", "comparatione", "compunctione",
    "confessione", "confusione", "conmune", "consuetudine", "contemplatione", "conuersatione", "conuersione",
    "Dan", "Dathan", "dilectione", "discerne", "dispositione", "diuine", "domine",
    "Ecclesiasten", "Eden", "Esebon", "Euphraten", "exaltatione", "examen", "Exameron",
    "foramen",
    "Gabaon", "Gedeon", "Geon", "germen", "Golian",
    "Helian", "Hermonin", "Hieremian", "hypocrisin",
    "iaspin", "Idithun", "Ionathan", "Iordanen", "Israeliten", "Iudan",
    "Laban", "leuamen", "Leuin", "leuiten", "lien", "luctamen",
    "Madian", "Manassen", "Matthan", "Matthian", "meditatione", "miseratione", "modulamen", "Moysen",
    "mundane", "munimen",
    "natione", "Naason", "Naasson", "Nathan", "Neman", "Noemin", "nomotheticen",
    "occasione", "offensione", "oportune",
    "pentecosten", "Pheoyson", "Philon", "Phison",
    "Rafidin", "regimen", "Ruben",
    "Sabain", "Salmon", "Salomon", "Salomone", "Samson", "Sampson", "Satanan",
    "secessione", "Selmon", "Serafin", "Seraphin", "Sidon", "Simon", "Sion", "siromasten",
    "Solomon", "Solomone", "spiramen", "suave", "subtegmen", "susceptione", "Symeon",
    "tegimen", "tegmen", "Theodotion", "Thoman", "Tigrin", "topazion", "transpone", "tribulatione", "tutamen",
    "uelamen", "uerumtamen",
    "Zabulon", "Zain"
]
FULL_EXCEPTIONS: list[str] = list(EXISTING_EXCEPTIONS) + \
                             [exception.lower() for exception in CUSTOM_LATIN_EXCEPTIONS]
