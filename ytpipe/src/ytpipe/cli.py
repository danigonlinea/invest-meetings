"""Command line entry point. Prints a plan, then writes the meeting folder."""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from ytpipe import naming
from ytpipe.fetch import extract_video_id, fetch_metadata, fetch_transcript, subtitle_languages
from ytpipe.jsonout import build_document, count_words, iso_time, write_json
from ytpipe.parse import chunk_cues, cues_to_text, merge_speakers, parse_json3, parse_vtt

DEFAULT_CHUNK_CHARS = 1200
CUE_SEPARATOR = " "
TRANSCRIPT_JSON = "transcript.json"
SUMMARY_FILENAME = "summary.md"
DEBUG_ENV = "YTPIPE_DEBUG"
UNKNOWN_CHANNEL = "desconocido"


def default_out_dir() -> Path:
    """Return the project root that holds the meeting folders."""
    return Path(__file__).resolve().parents[3]


def build_parser() -> argparse.ArgumentParser:
    """Build the parser with one subcommand per task."""
    parser = argparse.ArgumentParser(prog="ytpipe", description="Write a YouTube transcript as a meeting folder.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    fetch = subcommands.add_parser("fetch", help="Download the transcript and write the meeting folder.")
    fetch.add_argument("url", help="The YouTube URL of the video.")
    fetch.add_argument("--date", help="The meeting date as YYYY-MM-DD. Default: the upload date.")
    fetch.add_argument("--slug", help="The topic slug. Default: the title as a slug.")
    fetch.add_argument("--out", help="The parent folder. Default: the project root.")
    fetch.add_argument("--lang", action="append", default=[], help="A language code. Repeat the option for more languages.")
    fetch.add_argument("--chunk-chars", type=int, default=DEFAULT_CHUNK_CHARS, help="The target size of each chunk.")
    fetch.add_argument("--force", action="store_true", help="Overwrite the folder if it exists.")
    fetch.add_argument("--open", dest="open_folder", action="store_true", default=platform.system() == "Darwin", help="Open the folder at the end.")
    fetch.add_argument("--no-open", dest="open_folder", action="store_false", help="Do not open the folder.")
    fetch.add_argument("--dry-run", action="store_true", help="Print the plan and write nothing.")
    fetch.set_defaults(handler=run_fetch)

    languages = subcommands.add_parser("languages", help="List every subtitle track of a video.")
    languages.add_argument("url", help="The YouTube URL of the video.")
    languages.set_defaults(handler=run_languages)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one subcommand and return the exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return int(args.handler(args))
    except Exception as error:  # noqa: BLE001 - the CLI never shows a traceback
        print(f"error: {error}", file=sys.stderr)
        _log_traceback()
        return 1


def run_languages(args: argparse.Namespace) -> int:
    """Print one line per subtitle track."""
    video_id = extract_video_id(args.url)
    tracks = subtitle_languages(video_id)

    if not tracks:
        print("no subtitle track found")
        return 1

    print(f"{video_id}: {len(tracks)} tracks")
    for track in tracks:
        kind = "auto" if track.get("automatic") else "manual"
        print(f"{track['code']}\t{track['name']}\t{kind}")

    return 0


def run_fetch(args: argparse.Namespace) -> int:
    """Download the transcript, then write the meeting folder."""
    video_id = extract_video_id(args.url)
    metadata = fetch_metadata(args.url)

    title = str(metadata.get("title") or "")
    channel = str(metadata.get("channel") or "")

    date = args.date or _upload_date(metadata)
    channel_slug = naming.slugify(channel, max_words=3) or UNKNOWN_CHANNEL
    slug = _folder_slug(args.slug, title)
    folder = Path(args.out or default_out_dir()) / naming.folder_name(date, slug)

    duration = iso_time(float(metadata.get("duration") or 0))

    print_plan(folder, video_id, title, channel, date, duration, args.chunk_chars)

    if args.dry_run:
        print("dry run: nothing was written")
        return 0

    if folder.exists() and not args.force:
        print(f"error: the folder already exists: {folder}", file=sys.stderr)
        print("use --force to overwrite it")
        return 1

    if args.force:
        _remove_stale_summary(folder)

    topic_slug = slug if args.slug else _topic_slug(title, channel_slug)

    transcript_metadata, raw_text, subtitle_format = fetch_transcript(args.url, args.lang or None)
    cues = _parse_cues(raw_text, subtitle_format)
    tagged, speakers = merge_speakers(cues)
    text = cues_to_text(tagged, CUE_SEPARATOR)
    chunks = chunk_cues(tagged, text, args.chunk_chars, CUE_SEPARATOR)

    folder.mkdir(parents=True, exist_ok=True)
    json_path = folder / TRANSCRIPT_JSON
    document = build_document(
        transcript_metadata,
        tagged,
        speakers,
        chunks,
        text,
        subtitle_format,
        video_id,
        args.url,
        datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    write_json(document, str(json_path))

    txt_path = folder / naming.transcript_filename(channel_slug, topic_slug)
    _write_text(txt_path, text)

    language = document["source"]["language_code"] or ", ".join(args.lang) or "default list"
    print_result(folder, txt_path.stat().st_size, json_path.stat().st_size, len(tagged), len(chunks), count_words(text), language, subtitle_format)
    print_next_step()

    if args.open_folder:
        _open_folder(folder)

    return 0


def print_plan(folder: Path, video_id: str, title: str, channel: str, date: str, duration: str, chunk_chars: int) -> None:
    """Print the plan before any write."""
    print(f"plan: {folder.name}")
    print("```")
    print(f"video id  : {video_id}")
    print(f"title     : {title}")
    print(f"channel   : {channel}")
    print(f"upload    : {date}")
    print(f"duration  : {duration}")
    print(f"chunk size: {chunk_chars} characters")
    print(f"target    : {folder}")
    print("```")


def print_result(folder: Path, txt_bytes: int, json_bytes: int, segments: int, chunks: int, words: int, language: str, subtitle_format: str) -> None:
    """Print the counts of the files that the run wrote."""
    print(f"done: {folder.name}")
    print("```")
    print(f"folder    : {folder}")
    print(f"txt bytes : {txt_bytes}")
    print(f"json bytes: {json_bytes}")
    print(f"segments  : {segments}")
    print(f"chunks    : {chunks}")
    print(f"words     : {words}")
    print(f"format    : {subtitle_format}")
    print(f"language  : {language}")
    print("```")


def print_next_step() -> None:
    """Tell the user which skill writes the summary."""
    print("next step: run the ingest-meeting skill to write summary.md from transcript.json")


def _folder_slug(supplied: str | None, title: str) -> str:
    """Return the slug that names the folder.

    A supplied value goes through the slugifier, so a value such as
    `Q4/Earnings` cannot nest two directories. A value that leaves no text
    fails fast.
    """
    if not supplied:
        return naming.slugify(title)

    slug = naming.slugify(supplied)
    if not slug:
        raise ValueError(f"--slug has no usable text: {supplied!r}; pass a different value with --slug")

    return slug


def _remove_stale_summary(folder: Path) -> None:
    """Delete the summary of a transcript that `--force` is about to replace.

    A missing file is not an error. The folder itself stays.
    """
    (folder / SUMMARY_FILENAME).unlink(missing_ok=True)


def _topic_slug(title: str, channel_slug: str) -> str:
    """Return the topic slug of a title, without the words of the channel.

    A title such as "Rick Astley - Never Gonna Give You Up" repeats the
    channel name, so the file name would say "rick-astley-rick-astley".
    The leading words that the channel slug already starts with are dropped.
    """
    slug = naming.slugify(title)
    if not channel_slug or not slug:
        return slug

    words = slug.split("-")
    dropped = 0
    while dropped < len(words) and channel_slug.startswith("-".join(words[: dropped + 1])):
        dropped += 1

    topic = "-".join(words[dropped:])
    if not topic:
        raise ValueError(
            f"the title repeats the channel name: {title!r}; pass --slug with the topic"
        )

    return topic


def _upload_date(metadata: dict) -> str:
    """Read the upload date as YYYY-MM-DD. yt-dlp gives YYYYMMDD."""
    raw = str(metadata.get("upload_date") or "").strip()
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"

    if not naming.DATE_PATTERN.match(raw):
        raise ValueError(
            f"no usable upload date in the metadata: {raw!r}; pass --date YYYY-MM-DD"
        )

    return raw


def _parse_cues(raw: str, subtitle_format: str) -> list[dict]:
    """Parse the subtitle text with the parser that matches the format."""
    parsers = {"json3": parse_json3, "vtt": parse_vtt}
    parser = parsers.get(subtitle_format)
    if parser is None:
        raise ValueError(f"unsupported subtitle format: {subtitle_format!r}; use json3 or vtt")

    try:
        return parser(raw)
    except ValueError as error:
        raise ValueError(f"cannot parse the {subtitle_format} subtitle: {error}") from error


def _write_text(path: Path, text: str) -> None:
    """Write the plain transcript with one trailing newline."""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"{text.rstrip()}\n" if text.strip() else "")


def _open_folder(folder: Path) -> None:
    """Open the folder in Finder. A failure is only a warning."""
    try:
        subprocess.run(["open", str(folder)], check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"warning: cannot open {folder}: {error}", file=sys.stderr)


def _log_traceback() -> None:
    """Show the traceback only when YTPIPE_DEBUG is 1."""
    if os.environ.get(DEBUG_ENV) == "1":
        traceback.print_exc()


if __name__ == "__main__":
    raise SystemExit(main())