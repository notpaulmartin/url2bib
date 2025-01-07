"""URL to BibTeX converter."""

from .version import __version__
from .core import (
    url2bibtex,
    doi2bibtex,
    isbn2bibtex,
    parse_bibtex,
)

__all__ = [
    'url2bibtex',
    'doi2bibtex',
    'isbn2bibtex',
    'parse_bibtex',
    '__version__',
]
