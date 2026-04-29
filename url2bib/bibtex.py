"""BibTeX parsing, formatting, and candidate record construction helpers."""

import re

import bibtexparser

from .types import CandidateRecord


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


def create_bib_id(bibdict: dict, warn=None) -> str:
    """Create a BibTeX ID from a bibliography dictionary."""
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
        if warn is not None:
            warn("\033[93mWARNING: No author found in BibTeX entry\033[0m")
        first_author_surname = "Unk"

    first_author_surname = re.sub(r"[^\w-]", "", first_author_surname)
    first_author_surname = re.split(r"-| ", first_author_surname)
    first_author_surname = list(filter(None, first_author_surname))
    first_author_surname = first_author_surname[-1]

    if "year" in bibdict:
        year = bibdict["year"]
    else:
        if warn is not None:
            warn("\033[93mWARNING: No year found in BibTeX entry\033[0m")
        year = "0000"
    title_firstword = [word for word in bibdict["title"].split(" ") if len(word) > 3][0]
    title_firstword = re.sub(r"[^\w-]", "", title_firstword)
    bib_id = f"{first_author_surname.lower()}_{year}_{title_firstword.lower()}"
    return bib_id
