from typing import Callable, TypeAlias

WordFilter: TypeAlias = Callable[[str], bool]
WordPreprocessor: TypeAlias = Callable[[str], str]
