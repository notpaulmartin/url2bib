import html
import re

from bs4 import BeautifulSoup

from ..types import LookupContext

PRIORITY = 20  # Lower = earlier


def matches_url(url: str) -> bool:
    """Return True when the URL points to Semantic Scholar."""
    return "semanticscholar.org" in url.lower()


def normalize_url(url: str) -> str:
    """Return the URL unchanged."""
    return url.strip()


def extract_bibtex(ctx: LookupContext, url: str) -> str | None:
    """
    Extract BibTeX from a Semantic Scholar page.

    Prefer the linked arXiv URL when exactly one unique arXiv PDF URL is present.
    """
    matches = re.findall(r"https://arxiv\.org/pdf/\S+?\.pdf", ctx.html)
    unique_arxiv_urls = list(set(matches))
    if len(unique_arxiv_urls) == 1:
        from ..core import url2bibtex

        print(f"Using arXiv URL: {unique_arxiv_urls[0]}")
        return url2bibtex(unique_arxiv_urls[0])

    soup = BeautifulSoup(ctx.html, "html.parser")
    for pre in soup.select("pre.bibtex-citation"):
        bibtex = html.unescape(pre.get_text()).strip()
        if bibtex:
            return bibtex

    return None
