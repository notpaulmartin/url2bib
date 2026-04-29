"""DOI and ISBN extraction plus identifier-to-BibTeX lookup helpers."""

import re
from collections import Counter

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"


def count_strings_in_list(strings_list: list[str]) -> dict:
    """Count occurrences of strings in a list."""
    string_counts = Counter(strings_list)
    return dict(string_counts)


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
    most_common_doi, _ = max(dois_counted.items(), key=lambda x: x[1])
    return most_common_doi


def isbn_from_html(html: str) -> str:
    """Extract ISBN from HTML content."""
    html = " ".join(html.split())

    isbn_pattern = (
        r"(?:ISBN[- ]?13|ISBN)?[:]?\s*(?=[0-9]{13}|(?=(?:[0-9]+[- ]){4})[0-9-]{17})97[89][- ]?(?:[0-9]{1}[- ]?){9}[0-9]"
    )
    match = re.search(isbn_pattern, html, re.I)

    if match:
        isbn = match.group()
        return re.sub(r"[^0-9]", "", isbn)

    isbn_pattern = (
        r"(?:ISBN[- ]?10|ISBN)?[:]?\s*(?=[0-9]{10}|(?=(?:[0-9]+[- ]){3})[0-9-]{13})[0-9][- ]?(?:[0-9]{1}[- ]?){8}[0-9X]"
    )
    match = re.search(isbn_pattern, html, re.I)

    if match:
        isbn = match.group()
        return re.sub(r"[^0-9X]", "", isbn)

    return None


def doi2bibtex(doi: str) -> str:
    """Convert a DOI to BibTeX format."""
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex", "User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.text
    return None


def isbn2bibtex(isbn: str) -> str:
    """Convert an ISBN to BibTeX format."""
    url = f"https://www.ebook.de/{isbn}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.text
    return None
