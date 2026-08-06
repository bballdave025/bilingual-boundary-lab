from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterator

_WHITESPACE_RE = re.compile(r"\s+")


def normalized_tokens(text: str) -> list[str]:
    """Return tokens after compatibility decomposition and separator mapping.

    Letters and decimal digits survive. Combining marks are discarded.
    Everything else becomes a separator, so punctuation never becomes an
    OTHER token and never silently joins neighboring text.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    characters: list[str] = []

    for character in decomposed:
        category = unicodedata.category(character)

        if category.startswith("M"):
            continue
        if category.startswith("L") or category == "Nd":
            characters.append(character)
        else:
            characters.append(" ")

    normalized = _WHITESPACE_RE.sub(" ", "".join(characters)).strip()
    return normalized.split() if normalized else []


def normalized_character_stream(text: str) -> list[str]:
    """Return a character stream suitable for character n-grams.

    Word boundaries become one literal space; punctuation is removed as a
    separator rather than joining text across the punctuation.
    """
    return list(" ".join(normalized_tokens(text)))


def iter_original_tokens(text: str) -> Iterator[str]:
    """Yield whitespace-delimited original tokens for anomaly inspection."""
    yield from text.split()
