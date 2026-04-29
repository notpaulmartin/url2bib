import re

from ..core import doi2bibtex, doi_from_html
from ..models import LookupContext

PRIORITY = 10  # Lower = earlier


def matches_url(url: str) -> bool:
    """Return True when the URL points to arXiv."""
    return "arxiv.org" in url.lower()


def normalize_url(url: str) -> str:
    """Normalize arXiv PDF URLs to abstract pages."""
    normalized_url = url.strip()
    if re.match(r"https://arxiv\.org/pdf/[\d\.]+", normalized_url):
        normalized_url = normalized_url.replace("/pdf/", "/abs/").rstrip(".pdf")
    return normalized_url


def extract_bibtex(ctx: LookupContext, url: str) -> str | None:
    """Extract BibTeX from an arXiv page via its DOI."""
    doi = doi_from_html(ctx.html)
    if doi:
        ctx.doi = doi
        return doi2bibtex(doi)
    return None
