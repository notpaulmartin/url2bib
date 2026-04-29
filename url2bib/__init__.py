"""URL to BibTeX converter."""

from .bibtex import parse_bibtex
from .core import set_verbosity, url2bibtex
from .identifiers import doi2bibtex, isbn2bibtex
from .version import __version__

__all__ = [
    "url2bibtex",
    "doi2bibtex",
    "isbn2bibtex",
    "parse_bibtex",
    "set_verbosity",
    "__version__",
]
