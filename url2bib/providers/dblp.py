import urllib.parse
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from ..bibtex import build_candidate_record
from ..core import maybeprint
from ..identifiers import USER_AGENT, doi2bibtex
from ..types import CandidateRecord, LookupContext

NAME = "DBLP"


def search(ctx: LookupContext) -> list[CandidateRecord]:
    """Search DBLP by title and return publication candidates."""
    if not ctx.title:
        return []

    search_url = (
        "https://dblp.org/search/publ/api"
        f"?q={urllib.parse.quote(ctx.title)}&format=xml"
    )

    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
    except Exception as e:
        maybeprint(f"Error searching DBLP: {str(e)}")
        return []

    candidates = []
    for hit in root.findall(".//hit"):
        info = hit.find("info")
        if info is None:
            continue

        bibtex = _bibtex_from_hit(info, headers)
        if bibtex:
            candidates.append(build_candidate_record("dblp", bibtex))

    return candidates


def _bibtex_from_hit(info, headers: dict[str, str]) -> str | None:
    doi_element = info.find("doi")
    if doi_element is not None and doi_element.text:
        return doi2bibtex(doi_element.text)

    venue_element = info.find("venue")
    if venue_element is not None and venue_element.text:
        venue_name = venue_element.text.lower()
        url_element = info.find("ee")
        if url_element is not None and url_element.text:
            bibtex = _bibtex_from_venue_page(venue_name, url_element.text)
            if bibtex:
                print(f"Got bibtex from venue: {url_element.text}")
                return bibtex

    dblp_url = info.find("url")
    if dblp_url is None or not dblp_url.text:
        return None

    dblp_bib_url = dblp_url.text.split(".html")[0] + ".bib"
    response = requests.get(dblp_bib_url, headers=headers, timeout=10)
    if not response.ok:
        return None

    bibtex = response.text
    title = build_candidate_record("dblp", bibtex).title.replace("\n", " ").strip()
    print(f'Got bibtex from DBLP: {dblp_bib_url} ("{title}")')
    return bibtex


def _bibtex_from_venue_page(venue_name: str, paper_url: str) -> str | None:
    """Fetch BibTeX from a venue page when DBLP does not expose a DOI."""
    if venue_name == "neurips":
        return _bibtex_from_neurips_page(paper_url)
    return None


def _bibtex_from_neurips_page(paper_url: str) -> str | None:
    """Scrape the BibTeX export link from a NeurIPS paper page.

    Args:
        paper_url: URL of the paper page on `neurips.cc`.

    Returns:
        The BibTeX export URL if found, otherwise `None`.
    """
    response = requests.get(paper_url, timeout=10)
    if not response.ok:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    bibtex_link = soup.find("a", href=lambda href: href and "/bibtex" in href)
    if not bibtex_link:
        return None

    bibtex_url = urljoin(paper_url, bibtex_link["href"])
    bibtex_response = requests.get(bibtex_url, timeout=10)
    if not bibtex_response.ok:
        return None

    return bibtex_response.text.strip()
