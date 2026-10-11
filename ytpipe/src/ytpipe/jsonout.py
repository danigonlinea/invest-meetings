"""Build the structured transcript document and write it as JSON."""

from __future__ import annotations

import json

from ytpipe.naming import DATE_PATTERN

SCHEMA_VERSION = "1.0"
KIND = "meeting-transcript"
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60


def iso_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS. Negative values become 00:00:00."""
    total = max(0, int(seconds))
    hours = total // SECONDS_PER_HOUR
    minutes = (total % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE
    remainder = total % SECONDS_PER_MINUTE
    return f"{hours:02d}:{minutes:02d}:{remainder:02d}"


def count_words(text: str) -> int:
    """Count the whitespace separated tokens in the text."""
    return len(text.split())


def build_document(
    metadata: dict,
    cues: list[dict],
    speakers: list[dict],
    chunks: list[dict],
    text: str,
    subtitle_format: str,
    video_id: str,
    url: str,
    fetched_at: str,
) -> dict:
    """Build the transcript document from parsed data and yt-dlp metadata.

    The `speakers` and `chapters` keys stay out of the document when the
    video has none, so a reader never has to check an empty list.
    """
    subtitle = _subtitle_track(metadata)
    ends = [cue["end"] for cue in cues] or [0.0]

    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
        "source": _source_document(metadata, subtitle, subtitle_format, video_id, url, fetched_at, bool(speakers)),
        "stats": _stats_document(cues, chunks, speakers, text, ends),
        "chunks": [
            {
                "index": chunk["index"],
                "text_start": chunk["char_start"],
                "text_end": chunk["char_end"],
                "time_start_iso": iso_time(chunk["time_start"]),
                "time_end_iso": iso_time(chunk["time_end"]),
                "speakers": chunk["speakers"],
                "text": chunk["text"],
            }
            for chunk in chunks
        ],
        "segments": [
            {
                "index": index,
                "speaker": cue.get("speaker"),
                "start": cue["start"],
                "end": cue["end"],
                "text": cue["text"],
            }
            for index, cue in enumerate(cues)
        ],
    }

    chapters = _chapters(metadata)
    if chapters:
        document["chapters"] = chapters

    if speakers:
        document["speakers"] = _speaker_documents(speakers, cues)

    return document


def write_json(document: dict, path: str) -> None:
    """Write the document as UTF-8 JSON with two spaces of indent."""
    payload = json.dumps(document, ensure_ascii=False, indent=2)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"{payload}\n")


def _source_document(
    metadata: dict,
    subtitle: dict,
    subtitle_format: str,
    video_id: str,
    url: str,
    fetched_at: str,
    has_speaker_labels: bool,
) -> dict:
    """Build the `source` section, which names the video and its track."""
    return {
        "url": url,
        "video_id": video_id,
        "title": _text(metadata.get("title")),
        "description": _text(metadata.get("description")),
        "channel": _text(metadata.get("channel")),
        "uploader": _text(metadata.get("uploader")),
        "uploader_id": _text(metadata.get("uploader_id")),
        "upload_date": _upload_date(metadata.get("upload_date")),
        "duration_seconds": int(metadata.get("duration") or 0),
        "language_code": _text(subtitle.get("code")),
        "language_name": _text(subtitle.get("name")),
        "subtitle_kind": _subtitle_kind(subtitle),
        "subtitle_format": subtitle_format,
        "has_speaker_labels": has_speaker_labels,
        "fetched_at": fetched_at,
    }


def _stats_document(cues: list[dict], chunks: list[dict], speakers: list[dict], text: str, ends: list[float]) -> dict:
    """Build the `stats` section, which counts what the document holds."""
    return {
        "segment_count": len(cues),
        "chunk_count": len(chunks),
        "speaker_count": len(speakers),
        "word_count": count_words(text),
        "character_count": len(text),
        "time_span_seconds": int(round(max(ends))),
    }


def _chapters(metadata: dict) -> list[dict]:
    """Build the `chapters` section from the yt-dlp chapter list."""
    chapters: list[dict] = []

    for index, chapter in enumerate(metadata.get("chapters") or []):
        if not isinstance(chapter, dict):
            continue

        start = _chapter_seconds(chapter, "start_time")
        end = _chapter_seconds(chapter, "end_time")
        chapters.append(
            {
                "index": index,
                "start": start,
                "start_iso": iso_time(start),
                "end": end,
                "end_iso": iso_time(end),
                "title": _text(chapter.get("title")),
            }
        )

    return chapters


def _chapter_seconds(chapter: dict, key: str) -> float:
    """Read one chapter bound in seconds. A missing bound becomes zero."""
    return float(chapter.get(key) or 0)


def _speaker_documents(speakers: list[dict], cues: list[dict]) -> list[dict]:
    """Build the `speakers` section, counting the words of every speaker."""
    words = _words_by_speaker(cues)

    return [
        {
            "id": speaker["id"],
            "name": speaker.get("name"),
            "label": speaker.get("label", ""),
            "word_count": words.get(speaker["id"], 0),
        }
        for speaker in speakers
    ]


def _words_by_speaker(cues: list[dict]) -> dict[str, int]:
    """Count the words of every speaker in one pass over the cues."""
    counts: dict[str, int] = {}

    for cue in cues:
        speaker = cue.get("speaker")
        if speaker is None:
            continue

        counts[speaker] = counts.get(speaker, 0) + count_words(cue["text"])

    return counts


def _text(value: object) -> str:
    """Metadata never stores null in the document, so empty string stands in."""
    return value if isinstance(value, str) else ""


def _upload_date(value: object) -> str:
    """Return the upload date as YYYY-MM-DD. yt-dlp gives YYYYMMDD.

    A date that already has dashes stays as it is. A missing or malformed
    value becomes an empty string, because the document never fails to build.
    """
    raw = _text(value).strip()
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"

    if DATE_PATTERN.match(raw):
        return raw

    return ""


def _subtitle_track(metadata: dict) -> dict:
    """Read the track that yt-dlp stored during the subtitle download."""
    track = metadata.get("ytpipe_subtitle")
    return track if isinstance(track, dict) else {}


def _subtitle_kind(subtitle: dict) -> str:
    return "auto" if subtitle.get("automatic") else "manual"