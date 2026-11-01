"""Talk to yt-dlp. Nothing here writes a file."""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from typing import TypeVar
from urllib.error import URLError
from urllib.request import Request, urlopen

from yt_dlp import YoutubeDL

DEFAULT_LANGUAGES = ["es", "es-ES", "es-419", "en", "en-US", "en-GB"]
SUBTITLE_FORMATS = ["json3", "vtt"]  # the order of preference, best first
VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
BASE_OPTIONS = {"quiet": True, "no_warnings": True, "noprogress": True}
USER_AGENT = "Mozilla/5.0 (compatible; ytpipe/0.1)"

RATE_LIMIT_BACKOFF = (5, 15, 45)  # the seconds to wait before each retry
RATE_LIMIT_MARKERS = ("429", "Too Many Requests")

T = TypeVar("T")

YOUTUBE_WATCH = "youtube.com/watch?v="
YOUTUBE_SHORT = "youtube.com/shorts/"
YOUTUBE_EMBED = "youtube.com/embed/"
YOUTUBE_SHORT_HOST = "youtu.be/"


def extract_video_id(url: str) -> str:
    """Return the 11 character video id of a YouTube URL."""
    candidate = (url or "").strip()

    for marker in (YOUTUBE_WATCH, YOUTUBE_SHORT, YOUTUBE_EMBED, YOUTUBE_SHORT_HOST):
        if marker in candidate:
            tail = candidate.split(marker, 1)[1].split("#")[0].split("?")[0]
            video_id = tail.split("&")[0].split("/")[0]
            if VIDEO_ID_PATTERN.match(video_id):
                return video_id

    if VIDEO_ID_PATTERN.match(candidate):
        return candidate

    raise ValueError(
        "cannot read a video id from the url; accepted forms are "
        "youtube.com/watch?v=ID, youtu.be/ID, youtube.com/shorts/ID, "
        "youtube.com/embed/ID and a bare 11 character id"
    )


def fetch_metadata(url: str) -> dict:
    """Return the yt-dlp info dict for a video, without any subtitle."""
    with YoutubeDL({**BASE_OPTIONS, "skip_download": True, "writesubtitles": False}) as ydl:
        return ydl.extract_info(url, download=False) or {}


def fetch_transcript(url: str, languages: list[str] | None = None) -> tuple[dict, str, str]:
    """Return `(metadata, raw_subtitle_text, subtitle_format)` for a video.

    YouTube answers with HTTP 429 when it rate limits caption requests, so the
    download runs again after a growing wait.
    """
    wanted = list(languages) if languages else list(DEFAULT_LANGUAGES)
    return _retry_on_rate_limit(url, lambda: _download_transcript(url, wanted))


def _download_transcript(url: str, wanted: list[str]) -> tuple[dict, str, str]:
    """Ask yt-dlp for the metadata and the subtitle text of one attempt."""
    options = {
        **BASE_OPTIONS,
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "/".join(SUBTITLE_FORMATS),
        "subtitleslangs": wanted,
    }

    with YoutubeDL(options) as ydl:
        metadata = ydl.extract_info(url, download=False) or {}

    metadata["ytpipe_subtitle"] = _pick_track(metadata, wanted)
    track = metadata["ytpipe_subtitle"]
    return metadata, _download_text(track["url"]), track["ext"]


def _retry_on_rate_limit(url: str, operation: Callable[[], T]) -> T:
    """Run `operation` and wait out every HTTP 429.

    The waits grow: 5 seconds, then 15, then 45. The run stops after the third
    wait. Any other error goes straight to the caller.
    """
    retries = 0

    while True:
        try:
            return operation()
        except Exception as error:  # noqa: BLE001 - only the 429 is handled here
            if not _is_rate_limited(error):
                raise

            if retries >= len(RATE_LIMIT_BACKOFF):
                raise RuntimeError(
                    f"YouTube rate limited the captions for {url} "
                    f"after {retries + 1} attempts"
                ) from error

            time.sleep(RATE_LIMIT_BACKOFF[retries])
            retries += 1


def _is_rate_limited(error: Exception) -> bool:
    """Tell an HTTP 429 from any other failure by its message."""
    message = str(error)
    return any(marker in message for marker in RATE_LIMIT_MARKERS)


def subtitle_languages(video_id: str) -> list[dict]:
    """List every subtitle track so the user can pick one."""
    url = f"https://www.youtube.com/watch?v={extract_video_id(video_id)}"
    try:
        metadata = fetch_metadata(url)
    except Exception:
        return []

    tracks = [
        *_manual_tracks(metadata.get("subtitles")),
        *_automatic_tracks(metadata.get("automatic_captions")),
    ]
    return _one_per_language(tracks)


def _one_per_language(tracks: list[dict]) -> list[dict]:
    """Collapse the per-format entries into one entry per language code.

    A group is one track. Inside a group the best format wins, where the
    best format is the first one in `SUBTITLE_FORMATS`. The result is
    sorted by code.
    """
    groups: dict[str, list[dict]] = {}
    for track in tracks:
        groups.setdefault(track["code"], []).append(track)

    chosen = [_best_format(group) for _, group in sorted(groups.items())]
    return [
        {"code": track["code"], "name": track["name"], "automatic": track["automatic"]}
        for track in chosen
    ]


def _best_format(group: list[dict]) -> dict:
    """Return the entry of a group whose format comes first in the order.

    `min` keeps the first entry when no format ranks first, so an unknown
    format never loses against a known one.
    """
    return min(group, key=_format_rank)


def _format_rank(track: dict) -> int:
    """Give a lower number to a better format. An unknown format ranks last."""
    ext = track["ext"]
    return SUBTITLE_FORMATS.index(ext) if ext in SUBTITLE_FORMATS else len(SUBTITLE_FORMATS)


def _pick_track(metadata: dict, wanted: list[str]) -> dict:
    """Choose the best track: every manual track first, then every automatic one.

    A manual track of a later language beats a machine translation of an
    earlier language. Inside one kind, the order of `wanted` ranks the codes
    and the cue count ranks the tracks of the same code.
    """
    for tracks in (
        _manual_tracks(metadata.get("subtitles")),
        _automatic_tracks(metadata.get("automatic_captions")),
    ):
        matching = [track for track in tracks if track["code"] in wanted]
        if matching:
            ranked = sorted(matching, key=lambda track: wanted.index(track["code"]))
            return _best_of(ranked)

    raise RuntimeError(
        "no subtitle available: the video has no track in any requested language. "
        f"Run `ytpipe languages {metadata.get('webpage_url') or metadata.get('id') or '<url>'}` "
        "to list the tracks it does have."
    )


def _manual_tracks(source: object, code: str | None = None) -> list[dict]:
    """Normalise the manual `subtitles` group of the info dict."""
    return _tracks(source, code, automatic=False)


def _automatic_tracks(source: object, code: str | None = None) -> list[dict]:
    """Normalise the `automatic_captions` group of the info dict."""
    return _tracks(source, code, automatic=True)


def _tracks(source: object, code: str | None, automatic: bool) -> list[dict]:
    """Build one dict per format of every track that matches `code`."""
    if not isinstance(source, dict):
        return []

    found: list[dict] = []
    for name, formats in source.items():
        if code is not None and name != code:
            continue

        for item in formats if isinstance(formats, list) else []:
            ext = item.get("ext")
            url = item.get("url")
            if ext not in SUBTITLE_FORMATS or not url:
                continue

            found.append(
                {
                    "code": name,
                    "name": item.get("name") or name,
                    "automatic": automatic,
                    "ext": ext,
                    "url": url,
                }
            )
    return found


def _best_of(tracks: list[dict]) -> dict:
    """Keep the track with the highest cue count."""
    return max(tracks, key=lambda track: _cue_count(track["url"], track["ext"]))


def _cue_count(url: str, ext: str) -> int:
    """Count the cues of one subtitle file. Failure means zero cues."""
    try:
        raw = _download_text(url)
    except (URLError, OSError, ValueError):
        return 0

    if ext == "json3":
        try:
            return len(json.loads(raw).get("events") or [])
        except (TypeError, ValueError):
            return 0

    return sum(1 for line in raw.split("\n") if "-->" in line)


def _download_text(url: str) -> str:
    """Read a subtitle URL into text."""
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")