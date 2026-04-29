from dataclasses import dataclass


@dataclass
class LookupContext:
    input_url: str = ""
    normalized_url: str = ""
    source_domain: str = ""
    html: str = ""
    title: str = ""
    authors: str = ""
    doi: str = ""
    isbn: str = ""
    keywords: str = ""
    publisher: str = ""
    url: str = ""
    bibtex: str = ""


@dataclass
class CandidateRecord:
    source: str
    bibtex: str
    title: str = ""
    authors: str = ""
    is_published: bool = False
