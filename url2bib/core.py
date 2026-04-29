#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import Counter

import bibtexparser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .models import CandidateRecord

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"

verbose = False


# ——— Helper Functions ———————————————————————————————————————————————

def set_verbosity(verbose_: bool) -> None:
    global verbose
    verbose = verbose_


def maybeprint(*args, **kwargs) -> None:
    """
    Print a message only if verbose mode is enabled.
    """
    if verbose:
        print(*args, **kwargs)


def count_strings_in_list(strings_list: list[str]) -> dict:
    """Count occurrences of strings in a list."""
    string_counts = Counter(strings_list)
    return dict(string_counts)


# ——— BibTex Handling ————————————————————————————————————————————————

def parse_bibtex(bibtex: str) -> dict:
    """Parse a BibTeX string into a dictionary."""
    if bibtex is None:
        return dict()
    return bibtexparser.loads(bibtex).entries[0]


def format_bibtex(bibtex: str) -> str:
    """Indent continued BibTeX field lines."""
    indented_lines = []

    for line in bibtex.splitlines():
        if (
            line
            and not line.startswith((" ", "@", "}"))
            and indented_lines
            and indented_lines[-1].startswith(" ")
        ):
            line = f"  {line}"
        indented_lines.append(line)

    return "\n".join(indented_lines)


def build_bibtex(bibdict: dict) -> str:
    """Convert a bibliography dictionary into a BibTeX string."""
    new_lib = bibtexparser.bibdatabase.BibDatabase()
    new_lib.entries = [bibdict]
    bibtex = bibtexparser.dumps(new_lib)
    return format_bibtex(bibtex)


def build_candidate_record(source: str, bibtex: str) -> CandidateRecord:
    """Build a structured candidate from a BibTeX entry."""
    bibdict = parse_bibtex(bibtex)
    return CandidateRecord(
        source=source,
        bibtex=bibtex,
        title=bibdict.get("title", ""),
        authors=bibdict.get("author", ""),
        is_published=not re.search(r"(corr|arxiv)", bibtex, re.I),
    )


def create_bib_id(bibdict: dict) -> str:
    """Create a BibTeX ID from a bibliography dictionary."""
    # Extract first author
    if "author" in bibdict:
        authors = bibdict["author"].replace("\n", " ").split("and")
        first_author_fullname = authors[0].strip()
        if "," in first_author_fullname:
            first_author_surname = first_author_fullname.split(",")[0].strip()
        elif " " in first_author_fullname:
            first_author_surname = first_author_fullname.split(" ")[-1].strip()
        else:
            first_author_surname = first_author_fullname.strip()
    else:
        maybeprint("\033[93mWARNING: No author found in BibTeX entry\033[0m")
        first_author_surname = "Unk"

    # Clean first author surname
    first_author_surname = re.sub(r"[^\w-]", "", first_author_surname)
    first_author_surname = re.split(r"-| ", first_author_surname)
    first_author_surname = list(filter(None, first_author_surname))
    first_author_surname = first_author_surname[-1]

    if "year" in bibdict:
        year = bibdict["year"]
    else:
        maybeprint("\033[93mWARNING: No year found in BibTeX entry\033[0m")
        year = "0000"
    title_firstword = [word for word in bibdict["title"].split(" ") if len(word) > 3][0]
    title_firstword = re.sub(r"[^\w-]", "", title_firstword)
    bib_id = f"{first_author_surname.lower()}_{year}_{title_firstword.lower()}"
    return bib_id


# ——— Extract from HTML ——————————————————————————————————————————————

def dois_from_html(html_content: str) -> list:
    """Extract DOIs from HTML content."""
    doi_pattern = r"(10.\d+/[^\s\>\"\<]+)"
    dois = re.findall(doi_pattern, html_content)
    dois = [re.split(r"[^0-9a-zA-Z\-./+_\(\)]", doi)[0] for doi in dois]
    return dois


def doi_from_html(html_content: str) -> str:
    """Extract the most common DOI from HTML content."""
    dois = dois_from_html(html_content)
    if len(dois) == 0:
        return None

    dois_counted = count_strings_in_list(dois)
    most_common_doi, most_common_count = max(dois_counted.items(), key=lambda x: x[1])

    maybeprint(f"DOI found: {most_common_doi}")
    return most_common_doi


def isbn_from_html(html: str) -> str:
    """Extract ISBN from HTML content."""
    # Remove whitespace and newlines
    html = " ".join(html.split())

    # Try to find ISBN-13
    isbn_pattern = (
        r"(?:ISBN[- ]?13|ISBN)?[:]?\s*(?=[0-9]{13}|(?=(?:[0-9]+[- ]){4})[0-9-]{17})97[89][- ]?(?:[0-9]{1}[- ]?){9}[0-9]"
    )
    match = re.search(isbn_pattern, html, re.I)

    if match:
        isbn = match.group()
        # Keep only numbers
        isbn = re.sub(r"[^0-9]", "", isbn)
        maybeprint(f"ISBN found: {isbn}")
        return isbn

    # If ISBN-13 not found, try ISBN-10
    isbn_pattern = (
        r"(?:ISBN[- ]?10|ISBN)?[:]?\s*(?=[0-9]{10}|(?=(?:[0-9]+[- ]){3})[0-9-]{13})[0-9][- ]?(?:[0-9]{1}[- ]?){8}[0-9X]"
    )
    match = re.search(isbn_pattern, html, re.I)

    if match:
        isbn = match.group()
        # Keep only numbers and X
        isbn = re.sub(r"[^0-9X]", "", isbn)
        maybeprint(f"ISBN found: {isbn}")
        return isbn

    return None

# ——— *2bibtex ———————————————————————————————————————————————————————

def doi2bibtex(doi: str) -> str:
    """Convert a DOI to BibTeX format."""
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex", "User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, verify=False)
    if r.status_code == 200:
        return r.text
    return None


def isbn2bibtex(isbn: str) -> str:
    """Convert an ISBN to BibTeX format."""
    url = f"https://www.ebook.de/{isbn}"
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, verify=False)
    if r.status_code == 200:
        return r.text  # This needs to be implemented properly
    return None


def url2bibtex(url: str) -> str:
    """Convert a URL to BibTeX format."""
    from .resolver import extract_url_bibtex

    return extract_url_bibtex(url)

def get_dblp_bibtexs(paper_title: str) -> list:
    """Search for publications on DBLP and return their BibTeX entries."""
    from .models import LookupContext
    from .providers import dblp

    return [candidate.bibtex for candidate in dblp.search(LookupContext(title=paper_title))]


def get_openreview_bibtexs(paper_title: str) -> list:
    """Search OpenReview by exact title and return any BibTeX entries found."""
    from .models import LookupContext
    from .providers import openreview

    return [candidate.bibtex for candidate in openreview.search(LookupContext(title=paper_title))]
