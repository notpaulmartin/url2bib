from ..identifiers import doi2bibtex, doi_from_html, isbn2bibtex, isbn_from_html
from ..types import LookupContext

PRIORITY = 100  # Lower = earlier


def matches_url(url: str) -> bool:
    """Generic HTML is the fallback parser for any URL."""
    return True


def normalize_url(url: str) -> str:
    """Return the URL unchanged."""
    return url.strip()


def extract_bibtex(ctx: LookupContext, url: str) -> str | None:
    """Extract citation metadata from generic HTML using DOI or ISBN hints."""
    doi = doi_from_html(ctx.html)
    if doi:
        ctx.doi = doi
        return doi2bibtex(doi)

    isbn = isbn_from_html(ctx.html)
    if isbn:
        ctx.isbn = isbn
        return isbn2bibtex(isbn)

    return None
