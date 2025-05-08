from re import compile, Pattern

# Pattern with additional symbols found in texts upon which the spellchecker was applied.
PUNCTUATION_PATTERN: Pattern = compile(r"[!\"#$%&'()*+,-./:;<=>?@\[\\\]^_`{|}~—〈〉†]")
