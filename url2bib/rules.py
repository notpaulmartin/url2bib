from .input_parsers import load_input_parsers
from .models import LookupContext
from .providers import dblp, openreview

OPENREVIEW_ARXIV_TOPICS = {
    "artificial intelligence",
    "computation and language",
    "computer vision and pattern recognition",
    "information retrieval",
    "machine learning",
    "neural and evolutionary computing",
    "robotics",
    "stat.ml",
    "cs.ai",
    "cs.cl",
    "cs.cv",
    "cs.ir",
    "cs.lg",
    "cs.ne",
    "cs.ro",
}


def select_input_parsers(url: str) -> list:
    """Choose the ordered set of input parsers for a URL."""
    return [parser for parser in load_input_parsers() if parser.matches_url(url)]


def select_providers(ctx: LookupContext) -> list:
    """Choose the ordered set of publication search providers."""
    providers = [dblp]
    if _is_arxiv_publication(ctx) and _has_openreview_topics(ctx):
        providers.append(openreview)
    return providers


def _is_arxiv_publication(ctx: LookupContext) -> bool:
    publisher = ctx.publisher.lower()
    doi = ctx.doi.lower()
    url = ctx.url.lower()
    return publisher == "arxiv" or "arxiv" in doi or "arxiv.org" in url


def _has_openreview_topics(ctx: LookupContext) -> bool:
    keywords = ctx.keywords.lower()
    return any(topic in keywords for topic in OPENREVIEW_ARXIV_TOPICS)
