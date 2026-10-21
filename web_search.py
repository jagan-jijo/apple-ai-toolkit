"""Small, synchronous web-search adapter for the /search command."""

import re
import unicodedata
from urllib.parse import urlparse

try:
    from ddgs import DDGS
except (ImportError, OSError) as error:  # Local chat can start without search.
    DDGS = None
    _DDGS_IMPORT_ERROR = error
else:
    _DDGS_IMPORT_ERROR = None


MAX_RESULTS = 5
MAX_TITLE_LENGTH = 200
MAX_SNIPPET_LENGTH = 500
SEARCH_TIMEOUT_SECONDS = 10
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class SearchError(RuntimeError):
    """Raised when the external search provider cannot return results."""


def sanitize_text(value: object, max_length: int | None = None) -> str:
    """Remove terminal control sequences and collapse whitespace."""
    text = _ANSI_ESCAPE.sub("", str(value or ""))
    text = "".join(
        " " if unicodedata.category(character).startswith("C") else character
        for character in text
    )
    text = " ".join(text.split())
    return text[:max_length] if max_length is not None else text


def _is_web_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def search_web(
    query: str,
    max_results: int = MAX_RESULTS,
) -> list[dict[str, str]]:
    """Return up to five normalized DDGS text-search results."""
    cleaned_query = str(query).strip()
    if not cleaned_query:
        raise ValueError("Search query cannot be empty.")
    if DDGS is None:
        raise SearchError(
            f"ddgs could not be imported: {_DDGS_IMPORT_ERROR}. "
            "Run: python -m pip install -r requirements.txt"
        )

    limit = max(1, min(int(max_results), MAX_RESULTS))
    try:
        with DDGS(timeout=SEARCH_TIMEOUT_SECONDS) as searcher:
            raw_results = searcher.text(cleaned_query, max_results=limit)
    except Exception as error:
        message = str(error) or type(error).__name__
        raise SearchError(message) from error

    results = []
    for item in raw_results or []:
        url = sanitize_text(item.get("href", ""))
        if not _is_web_url(url):
            continue
        results.append(
            {
                "title": sanitize_text(item.get("title") or "Untitled", MAX_TITLE_LENGTH),
                "url": url,
                "snippet": sanitize_text(item.get("body", ""), MAX_SNIPPET_LENGTH),
            }
        )
        if len(results) == limit:
            break

    return results
