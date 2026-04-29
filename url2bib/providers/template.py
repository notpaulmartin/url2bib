"""
Template for adding a new search provider.

Rename this file to `<name>.py` and set NAME to match the provider name.
"""

from ..types import CandidateRecord, LookupContext

NAME = "Template"


def search(ctx: LookupContext) -> list[CandidateRecord]:
    """
    Search for publication candidates using the metadata in `ctx`.

    Return a list of CandidateRecord objects. Return an empty list when the
    provider does not apply or finds no plausible candidates.
    """
    return []
