from difflib import SequenceMatcher
import re

from .models import CandidateRecord

TITLE_TOKEN_IGNORE_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
}


# ——— Title similarity —————————————————————————————————————————

def normalize_title(title: str) -> str:
    """
    Normalize a title for similarity matching across formatting variants:
        - Convert to lowercase
        - Remove non-word characters
        - Collapse whitespace
    """
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", title).lower()).strip()


def title_tokens(title: str) -> set[str]:
    """
    Extract meaningful normalized title tokens.

    Drop low-information words for computing token overlap.
    Common filler words like 'the', 'of', 'for' would otherwise dilute the overlap score.
    """
    return {
        token
        for token in normalize_title(title).split()
        if token and token not in TITLE_TOKEN_IGNORE_WORDS
    }


def title_similarity(source_title: str, candidate_title: str) -> float:
    """
    Score title similarity using both token overlap and string similarity.

    1. token_score = Jaccard similarity (intersection / union) of normalized title tokens
    2. string_score = SequenceMatcher ratio of normalized titles (fuzzy string similarity score between 0-1)
    Return a weighted average of the two scores.
    """
    source_tokens = title_tokens(source_title)
    candidate_tokens = title_tokens(candidate_title)
    if source_tokens or candidate_tokens:
        token_score = len(source_tokens & candidate_tokens) / len(source_tokens | candidate_tokens)
    else:
        token_score = 0.0

    string_score = SequenceMatcher(
        None, normalize_title(source_title), normalize_title(candidate_title)
    ).ratio()
    return 0.6 * token_score + 0.4 * string_score


# ——— Author similarity ————————————————————————————————————————

def extract_author_surnames(authors: str) -> list[str]:
    """Extract normalized author surnames from a BibTeX author field."""
    if not authors:
        return []

    surnames = []
    for author in authors.replace("\n", " ").split(" and "):
        author = author.strip()
        if not author:
            continue
        if "," in author:
            surname = author.split(",", 1)[0]
        else:
            surname = author.split(" ")[-1]
        surname = re.sub(r"[^\w-]", "", surname).lower()
        if surname:
            surnames.append(surname)
    return surnames


def author_similarity(source_authors: str, candidate_authors: str) -> tuple[float, bool]:
    """Score author overlap and first-author agreement."""
    source_surnames = extract_author_surnames(source_authors)
    candidate_surnames = extract_author_surnames(candidate_authors)
    if not source_surnames or not candidate_surnames:
        return 0.0, False

    overlap = len(set(source_surnames) & set(candidate_surnames)) / len(set(source_surnames))
    same_first_author = source_surnames[0] == candidate_surnames[0]
    return overlap, same_first_author


# ——— Ranking ——————————————————————————————————————————————————

def is_plausible_match(
    source_title: str,
    source_authors: str,
    candidate_title: str,
    candidate_authors: str,
) -> tuple[bool, float]:
    """Decide whether a candidate is a plausible match."""
    title_score = title_similarity(source_title, candidate_title)
    author_score, same_first_author = author_similarity(source_authors, candidate_authors)

    plausible = (
        title_score >= 0.97
        or (title_score >= 0.75 and same_first_author)
        or (title_score >= 0.6 and author_score >= 0.3)
    )
    combined_score = title_score + 0.2 * author_score + (0.05 if same_first_author else 0.0)
    return plausible, combined_score


def score_match_candidate(
    source_title: str, source_authors: str, candidate: CandidateRecord
) -> tuple[bool, float] | None:
    """Return selection metadata for a plausible paper match."""
    plausible, score = is_plausible_match(
        source_title, source_authors, candidate.title, candidate.authors
    )
    if not plausible:
        return None

    return candidate.is_published, score


def choose_candidate(
    source_title: str, source_authors: str, candidates: list[CandidateRecord]
) -> CandidateRecord | None:
    """Choose the best plausible paper match."""
    ranked_matches = []

    for candidate in candidates:
        ranking = score_match_candidate(source_title, source_authors, candidate)
        if ranking is None:
            continue
        ranked_matches.append((*ranking, candidate))

    if len(ranked_matches) == 0:
        return None

    _, _, chosen_candidate = max(ranked_matches, key=lambda item: (item[0], item[1]))
    return chosen_candidate


def choose_bibtex(
    source_title: str, source_authors: str, bibtex_entries: list[str]
) -> tuple[bool, str] | None:
    """Choose the best plausible paper match from raw BibTeX entries."""
    from .core import build_candidate_record

    candidates = [
        build_candidate_record("candidate", bibtex_entry) for bibtex_entry in bibtex_entries
    ]
    chosen_candidate = choose_candidate(source_title, source_authors, candidates)
    if chosen_candidate is None:
        return None
    return chosen_candidate.is_published, chosen_candidate.bibtex
