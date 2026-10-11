"""Pure parsers for YouTube subtitle payloads. No network. No file I/O."""

from __future__ import annotations

import html
import json
import re

TIMESTAMP_LINE = re.compile(
    r"^\s*(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})"
)
TAG_PATTERN = re.compile(r"<[^>]*>")
WHITESPACE_RUN = re.compile(r"\s+")

SPEAKER_LABEL_KEY = "speaker_label"
TOUCH_TOLERANCE = 0.001


def _seconds(hours: str | None, minutes: str, seconds: str, milliseconds: str) -> float:
    return int(hours or 0) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000.0


def _clean_text(raw: str) -> str:
    """Strip tags, decode entities and collapse whitespace inside one cue."""
    decoded = html.unescape(TAG_PATTERN.sub(" ", raw)).replace("\n", " ")
    return WHITESPACE_RUN.sub(" ", decoded).strip()


def _cue_start(event: dict) -> float:
    return float(event.get("tStartMs") or 0) / 1000.0


def _cue_end(event: dict) -> float:
    return _cue_start(event) + float(event.get("dDurationMs") or 0) / 1000.0


def _speaker_label(event: dict) -> str | None:
    """Read the YouTube speaker tag `aAppend` from the first segment."""
    for segment in event.get("segs") or []:
        label = segment.get("aAppend")
        if label:
            return str(label)
    return None


def _touching(end: float, start: float) -> bool:
    return abs(start - end) <= TOUCH_TOLERANCE


def _longest_suffix_prefix(previous_text: str, text: str) -> int:
    """Return the length of the tail of `previous_text` that starts `text`.

    The rolling automatic captions of YouTube repeat the whole visible line
    in every event, so the new text starts with the words that the previous
    text already ends with. The comparison ignores case. The result is `0`
    when the two texts share no tail.
    """
    previous_lower = previous_text.lower()
    text_lower = text.lower()

    for length in range(min(len(previous_lower), len(text_lower)), 0, -1):
        if previous_lower.endswith(text_lower[:length]):
            return length

    return 0


def _new_words(previous_text: str, text: str) -> str:
    """Return the part of `text` that `previous_text` does not already end with.

    The result carries no surrounding space, so a caller can join it with one
    space or drop it when it is empty.
    """
    return text[_longest_suffix_prefix(previous_text, text):].strip()


def parse_json3(raw: str) -> list[dict]:
    """Parse a yt-dlp `json3` payload into cues sorted by start time.

    Merges consecutive cues that touch in time and share one speaker, so the
    rolling automatic captions of YouTube do not repeat the same words.
    """
    cues: list[dict] = []

    for event in _json3_events(raw):
        text = _clean_text("".join(segment.get("utf8", "") for segment in event.get("segs") or []))
        if not text:
            continue

        start = _cue_start(event)
        end = _cue_end(event)
        label = _speaker_label(event)

        previous = cues[-1] if cues else None
        if (
            previous is not None
            and previous.get(SPEAKER_LABEL_KEY) == label
            and _touching(previous["end"], start)
        ):
            addition = _new_words(previous["text"], text)
            if addition:
                previous["text"] = f"{previous['text']} {addition}"
            previous["end"] = max(previous["end"], end)
            continue

        cue = {"start": start, "end": end, "text": text}
        if label is not None:
            cue[SPEAKER_LABEL_KEY] = label
        cues.append(cue)

    if not cues:
        raise ValueError("json3 payload has no cue")

    _fill_zero_length_ends(cues)
    return cues


def _fill_zero_length_ends(cues: list[dict]) -> None:
    """Give a cue with no duration the start time of the cue that follows it.

    YouTube writes no `dDurationMs` on some events, so the cue ends where it
    starts. The next cue is the closest real end. The last cue keeps its own
    end, because nothing follows it.
    """
    for cue, following in zip(cues, cues[1:]):
        if cue["end"] <= cue["start"]:
            cue["end"] = following["start"]


def _json3_events(raw: str) -> list[dict]:
    """Read the `events` list, or fail with a message that names the problem."""
    try:
        payload = json.loads(raw)
    except (TypeError, ValueError) as error:
        raise ValueError(f"json3 payload is not valid JSON: {error}") from error

    if not isinstance(payload, dict) or "events" not in payload:
        raise ValueError("json3 payload has no 'events' key")

    return [event for event in payload.get("events") or [] if isinstance(event, dict)]


def parse_vtt(raw: str) -> list[dict]:
    """Parse WebVTT text into cues sorted by start time.

    YouTube repeats the growing line at a new start time, so a cue drops the
    part that the previous cue already ends with.
    """
    blocks = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n\n")
    cues: list[dict] = []
    seen: set[tuple[float, str]] = set()
    previous_line = ""

    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines or _is_skipped_block(lines[0]):
            continue

        line_index = next((i for i, line in enumerate(lines) if TIMESTAMP_LINE.match(line)), None)
        if line_index is None:
            continue

        match = TIMESTAMP_LINE.match(lines[line_index])
        if match is None:
            continue

        text = _clean_text(" ".join(lines[line_index + 1 :]))
        if not text:
            continue

        start = _seconds(match.group(1), match.group(2), match.group(3), match.group(4))
        if (start, text) in seen:
            continue

        seen.add((start, text))

        addition = _new_words(previous_line, text)
        if not addition:
            continue

        previous_line = text
        end = _seconds(match.group(5), match.group(6), match.group(7), match.group(8))
        cues.append({"start": start, "end": end, "text": addition})

    if not cues:
        raise ValueError("vtt payload has no cue")

    cues = sorted(cues, key=lambda cue: cue["start"])
    _fill_zero_length_ends(cues)
    return cues


def _is_skipped_block(first_line: str) -> bool:
    """A header, a NOTE block and a STYLE block carry no cue text."""
    head = first_line.strip()
    return head.startswith(("WEBVTT", "NOTE", "STYLE"))


def merge_speakers(cues: list[dict]) -> tuple[list[dict], list[dict]]:
    """Tag every cue with a `speaker` id and return the speaker list.

    Ids follow the first appearance order. `label` keeps the json3
    `aAppend` value and `name` stays null, because YouTube gives no real
    name for a speaker.

    A transcript with no speaker label has no speaker at all. Every cue then
    carries `speaker` as None and the speaker list stays empty, so no reader
    can credit a quote to a person who does not exist.
    """
    labels = [_cue_label(cue) for cue in cues]

    if not any(label is not None for label in labels):
        return [{**cue, "speaker": None} for cue in cues], []

    ids: dict[str | None, str] = {}
    speakers: list[dict] = []
    tagged: list[dict] = []

    for cue, label in zip(cues, labels):
        if label not in ids:
            ids[label] = f"speaker-{len(ids) + 1}"
            speakers.append(
                {
                    "id": ids[label],
                    "name": None,
                    "label": label if isinstance(label, str) else "",
                }
            )

        tagged.append({**cue, "speaker": ids[label]})

    return tagged, speakers


def _cue_label(cue: dict) -> str | None:
    """Read the speaker label of a cue, from either key a parser wrote."""
    return cue.get(SPEAKER_LABEL_KEY, cue.get("speaker"))


def cues_to_text(cues: list[dict], separator: str = " ") -> str:
    """Join cue texts into one plain text block."""
    if not cues:
        return ""

    return WHITESPACE_RUN.sub(" ", separator.join(cue["text"] for cue in cues)).strip()


def chunk_cues(
    cues: list[dict],
    text: str,
    target_chars: int = 1200,
    separator: str = " ",
) -> list[dict]:
    """Group cues into chunks of about `target_chars` characters.

    One cue never splits across two chunks. The `separator` must be the same
    one that `cues_to_text` used, because it sits between every two cues.
    Each chunk maps back to exact character offsets inside `text`.
    """
    chunks: list[dict] = []
    group: list[dict] = []
    cursor = 0
    char_start = 0
    char_end = 0
    group_length = 0
    separator_length = len(separator)

    for index, cue in enumerate(cues):
        cue_text = cue["text"]
        start_in_text = text.find(cue_text, cursor)
        if start_in_text < 0:
            raise ValueError(f"cue {index} text is not found in the transcript text")

        cursor = start_in_text + len(cue_text)
        grown = group_length + len(cue_text) + (separator_length if group else 0)

        if group and grown > target_chars:
            chunks.append(_build_chunk(len(chunks), group, char_start, char_end, text))
            group = []
            group_length = len(cue_text)
            char_start = start_in_text
        else:
            group_length = grown

        group.append(cue)
        char_end = start_in_text + len(cue_text)

    if group:
        chunks.append(_build_chunk(len(chunks), group, char_start, char_end, text))

    return chunks


def _build_chunk(index: int, group: list[dict], char_start: int, char_end: int, text: str) -> dict:
    """Build one chunk dict from the cues it holds."""
    return {
        "index": index,
        "char_start": char_start,
        "char_end": char_end,
        "time_start": group[0]["start"],
        "time_end": group[-1]["end"],
        "speakers": _chunk_speakers(group),
        "text": text[char_start:char_end],
    }


def _chunk_speakers(group: list[dict]) -> list[str]:
    """List the speaker ids of a chunk in order, with no name repeated."""
    return sorted({cue["speaker"] for cue in group if cue.get("speaker") is not None})