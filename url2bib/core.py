#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Compatibility wrappers and shared verbosity helpers for the package API."""

from .bibtex import (
    build_bibtex,
    build_candidate_record,
    create_bib_id as _create_bib_id,
    format_bibtex,
    parse_bibtex,
)
from .identifiers import (
    USER_AGENT,
    doi2bibtex,
    doi_from_html,
    dois_from_html,
    isbn2bibtex,
    isbn_from_html,
)
from .types import CandidateRecord, LookupContext

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

def create_bib_id(bibdict: dict) -> str:
    """Create a BibTeX ID from a bibliography dictionary."""
    return _create_bib_id(bibdict, warn=maybeprint)


def url2bibtex(url: str) -> str:
    """Convert a URL to BibTeX format."""
    from .resolver import extract_url_bibtex

    return extract_url_bibtex(url)

def get_dblp_bibtexs(paper_title: str) -> list:
    """Search for publications on DBLP and return their BibTeX entries."""
    from .providers import dblp

    return [candidate.bibtex for candidate in dblp.search(LookupContext(title=paper_title))]


def get_openreview_bibtexs(paper_title: str) -> list:
    """Search OpenReview by exact title and return any BibTeX entries found."""
    from .providers import openreview

    return [candidate.bibtex for candidate in openreview.search(LookupContext(title=paper_title))]
