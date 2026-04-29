"""
Template for adding a new input parser.

Rename this file to `<name>.py` to enable it.
"""

from ..types import LookupContext

PRIORITY = 50


def matches_url(url: str) -> bool:
    """Return True when this parser should handle the URL."""
    return False


def normalize_url(url: str) -> str:
    """Normalize the URL before fetching content."""
    return url.strip()


def extract_bibtex(ctx: LookupContext, url: str) -> str | None:
    """Extract an initial BibTeX entry from the fetched page and URL."""
    return None
