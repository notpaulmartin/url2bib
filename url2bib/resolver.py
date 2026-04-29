from urllib.parse import urlparse

import requests

from .core import USER_AGENT, maybeprint, parse_bibtex
from .models import LookupContext
from .paper_matching import choose_candidate
from .rules import select_input_parsers, select_providers


def extract_url_bibtex(url: str) -> str | None:
    """Extract an initial BibTeX entry from a URL."""
    parsers = select_input_parsers(url)
    ctx = _build_url_context(url, parsers)
    if ctx is None:
        return None

    for parser in parsers:
        bibtex = parser.extract_bibtex(ctx, ctx.normalized_url)
        if bibtex:
            return bibtex

    return None


def resolve_url_bibdict(url: str) -> dict | None:
    """Resolve a URL to the best available BibTeX dictionary."""
    bibtex = extract_url_bibtex(url)
    if bibtex is None:
        return None

    bibdict = parse_bibtex(bibtex)
    return resolve_publication_bibdict(bibdict)


def resolve_publication_bibdict(bibdict: dict) -> dict:
    """Search publication providers and prefer a matched published record."""
    ctx = _build_publication_context(bibdict)
    selected_bibdict = bibdict
    for provider in select_providers(ctx):
        print(f"Querying {provider.NAME}...")
        candidates = provider.search(ctx)
        if not candidates:
            continue

        best_match = choose_candidate(ctx.title, ctx.authors, candidates)
        if best_match is None:
            maybeprint(f"No matching publications found in {provider.NAME}")
            continue

        message = _selection_message(provider.NAME, best_match.is_published)
        if message:
            print(message)
        selected_bibdict = parse_bibtex(best_match.bibtex)
        if best_match.is_published:
            return selected_bibdict

    return selected_bibdict


def _build_url_context(url: str, parsers: list) -> LookupContext | None:
    normalized_url = url
    for parser in parsers:
        normalized_url = parser.normalize_url(normalized_url)

    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(normalized_url, headers=headers, verify=False)
    except Exception as e:
        maybeprint(f"Error processing URL: {str(e)}")
        return None

    if response.status_code != 200 and "semanticscholar.org" in normalized_url:
        print("Sometimes Semantic Scholar resists scraping. Try using the arXiv url instead.")

    return LookupContext(
        input_url=url,
        normalized_url=normalized_url,
        source_domain=urlparse(normalized_url).netloc.lower(),
        html=response.text,
    )


def _build_publication_context(bibdict: dict) -> LookupContext:
    url = bibdict.get("url", "")
    return LookupContext(
        title=bibdict.get("title", ""),
        authors=bibdict.get("author", ""),
        doi=bibdict.get("doi", ""),
        isbn=bibdict.get("isbn", ""),
        keywords=bibdict.get("keywords", ""),
        publisher=bibdict.get("publisher", ""),
        url=url,
        bibtex="",
        source_domain=urlparse(url).netloc.lower() if url else "",
    )


def _selection_message(provider_name: str, is_published: bool) -> str | None:
    if provider_name == "DBLP":
        return "Choosing paper from venue." if is_published else "Choosing paper from arXiv."
    if provider_name == "OpenReview" and is_published:
        return "Choosing paper from OpenReview venue."
    return None
