"""Pure helpers for folder and file names."""

from __future__ import annotations

import re
import unicodedata

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9]+")

# Connectors carry no meaning alone, so a connector at the end of a slug
# only makes the slug read worse.
CONNECTORS = frozenset(
    {
        "a", "al", "and", "con", "de", "del", "el", "en", "in", "la", "las",
        "los", "of", "o", "or", "para", "por", "the", "to", "u", "un", "una",
        "unas", "unos", "y",
    }
)


def slugify(text: str, max_words: int = 10) -> str:
    """Turn free text into a lowercase hyphenated slug.

    Strips accents, replaces every non-alphanumeric run with one hyphen,
    keeps at most `max_words` words, then drops the connectors at the end.
    The drop runs after the cut, because the cut can leave a connector.
    One word always survives, so a non-empty text never gives an empty slug.
    """
    if max_words < 1:
        return ""

    words = _words(text)
    if not words:
        return ""

    return "-".join(_drop_trailing_connectors(words[:max_words]))


def _words(text: str) -> list[str]:
    """Split text into lowercase words. Returns no words for text without letters or digits."""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))
    hyphenated = NON_ALNUM_PATTERN.sub("-", without_accents.lower()).strip("-")
    if not hyphenated:
        return []

    return hyphenated.split("-")


def _drop_trailing_connectors(words: list[str]) -> list[str]:
    """Drop the connectors at the end of the words.

    The loop runs because each drop can expose another connector. The last
    word stays, so a title of only connectors keeps one word.
    """
    kept = list(words)
    while len(kept) > 1 and kept[-1] in CONNECTORS:
        kept.pop()

    return kept


def folder_name(date: str, slug: str) -> str:
    """Join the meeting date and slug into the folder name."""
    if not DATE_PATTERN.match(date):
        raise ValueError(f"date must look like YYYY-MM-DD, got {date!r}")

    return f"{date}-{slug}"


def transcript_filename(channel_slug: str, topic_slug: str) -> str:
    """Build the transcript file name for a channel and a topic.

    The topic keeps the default word budget of `slugify`, because the topic
    carries the meaning. The channel keeps three words, because a long channel
    name reads badly and the first words already tell the channels apart.
    """
    channel = slugify(channel_slug, max_words=3)
    topic = slugify(topic_slug)
    if not channel:
        raise ValueError("channel_slug reduces to an empty slug")
    if not topic:
        raise ValueError("topic_slug reduces to an empty slug")

    return f"invest-{channel}-{topic}.txt"