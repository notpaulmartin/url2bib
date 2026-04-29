import html
import re
import urllib.parse

import requests

from ..bibtex import build_candidate_record
from ..core import maybeprint
from ..identifiers import USER_AGENT
from ..types import CandidateRecord, LookupContext

NAME = "OpenReview"


def search(ctx: LookupContext) -> list[CandidateRecord]:
    """Search OpenReview by exact title and return publication candidates."""
    if not ctx.title:
        return []

    headers = {"User-Agent": USER_AGENT}
    params = {
        "term": ctx.title,
        "type": "exact",
        "content": "title",
    }

    try:
        response = requests.get(
            "https://api2.openreview.net/notes/search",
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        notes = response.json().get("notes", [])
    except Exception as e:
        maybeprint(f"Error searching OpenReview: {str(e)}")
        return []

    candidates = []
    for note in notes:
        bibtex = _nested_content_value(note.get("content", {}).get("_bibtex"))
        if bibtex:
            candidates.append(build_candidate_record("openreview", bibtex.strip()))
            continue

        forum_id = note.get("forum") or note.get("id")
        if not forum_id:
            continue

        forum_url = f"https://openreview.net/forum?id={forum_id}"
        forum_response = requests.get(forum_url, headers=headers, timeout=10)
        if not forum_response.ok:
            continue
        bibtex = _bibtex_from_forum_html(forum_response.text)
        if bibtex:
            candidates.append(build_candidate_record("openreview", bibtex))

    return candidates


def _nested_content_value(value):
    if isinstance(value, dict):
        return value.get("value")
    return value


def _bibtex_from_forum_html(html_content: str) -> str | None:
    match = re.search(r'data-bibtex="([^"]+)"', html_content)
    if not match:
        return None
    return html.unescape(urllib.parse.unquote(match.group(1))).strip()
