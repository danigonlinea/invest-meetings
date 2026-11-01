from __future__ import annotations

import json
from pathlib import Path

import pytest

import ytpipe.cli as cli

WATCH = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
VIDEO_ID = "dQw4w9WgXcQ"

METADATA = {
    "title": "Burbujas y CAPEX",
    "channel": "La Pizarra de Andrés",
    "uploader": "La Pizarra de Andrés",
    "uploader_id": "@lapizarra",
    "upload_date": "20260101",
    "duration": 754,
    "subtitles": {},
    "automatic_captions": {},
}


def fake_transcript() -> tuple[dict, str, str]:
    raw = json.dumps(
        {
            "events": [
                {"tStartMs": 0, "dDurationMs": 2000, "segs": [{"utf8": "Hola amigos"}]},
                {"tStartMs": 2000, "dDurationMs": 2000, "segs": [{"utf8": "de la pizarra"}]},
            ]
        }
    )
    metadata = dict(METADATA)
    metadata["ytpipe_subtitle"] = {"code": "es", "name": "Spanish", "automatic": True}
    return metadata, raw, "json3"


def test_help_names_every_subcommand(capsys) -> None:
    with pytest.raises(SystemExit) as raised:
        cli.main(["--help"])

    assert raised.value.code == 0
    out = capsys.readouterr().out
    assert "fetch" in out
    assert "languages" in out


def test_extract_video_id_accepts_every_documented_form() -> None:
    assert cli.extract_video_id(WATCH) == VIDEO_ID
    assert cli.extract_video_id("https://youtu.be/dQw4w9WgXcQ") == VIDEO_ID
    assert cli.extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == VIDEO_ID
    assert cli.extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == VIDEO_ID
    assert cli.extract_video_id("dQw4w9WgXcQ") == VIDEO_ID


def test_extract_video_id_fails_on_a_bad_url() -> None:
    with pytest.raises(ValueError, match="cannot read a video id"):
        cli.extract_video_id("https://vimeo.com/12345")


def test_default_out_dir_ends_with_the_project_root() -> None:
    root = cli.default_out_dir()
    assert (root / "ytpipe" / "pyproject.toml").exists()
    assert (root / "AGENTS.md").exists()


def test_dry_run_writes_nothing(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: dict(METADATA))
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path), "--dry-run"])

    assert code == 0
    assert list(tmp_path.iterdir()) == []
    assert "2026-01-01-burbujas-y-capex" in capsys.readouterr().out


def test_existing_folder_stops_the_run(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: dict(METADATA))
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())
    taken = tmp_path / "2026-01-01-burbujas-y-capex"
    taken.mkdir()

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path)])

    assert code == 1
    assert list(taken.iterdir()) == []
    assert "already exists" in capsys.readouterr().err


RICK_TITLE = "Rick Astley - Never Gonna Give You Up"
RICK_CHANNEL = "Rick Astley"


def test_topic_slug_drops_the_words_the_channel_already_gives() -> None:
    assert cli._topic_slug(RICK_TITLE, "rick-astley") == "never-gonna-give-you-up"


def test_topic_slug_keeps_a_title_without_the_channel_words() -> None:
    assert cli._topic_slug("Burbujas y CAPEX", "la-pizarra-de") == "burbujas-y-capex"


def test_topic_slug_stops_on_a_partial_word() -> None:
    assert cli._topic_slug("Ricky Martin - Hola", "rick-astley") == "ricky-martin-hola"


def test_topic_slug_fails_when_the_title_is_only_the_channel_name() -> None:
    with pytest.raises(ValueError, match="repeats the channel name"):
        cli._topic_slug(RICK_CHANNEL, "rick-astley")


def test_slug_with_a_slash_writes_one_flat_folder(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: dict(METADATA))
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path), "--slug", "Q4/Earnings", "--no-open"])

    assert code == 0
    assert (tmp_path / "2026-01-01-q4-earnings").is_dir()
    assert not (tmp_path / "2026-01-01-q4").exists()
    assert len(list(tmp_path.iterdir())) == 1


def test_slug_with_no_usable_text_fails(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: dict(METADATA))
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path), "--slug", "///", "--no-open"])

    assert code == 1
    assert "--slug" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_dry_run_prints_a_plan_when_the_title_is_only_the_channel_name(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: {**METADATA, "title": RICK_CHANNEL})
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path), "--dry-run"])

    assert code == 0
    assert "dry run: nothing was written" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_force_removes_the_stale_summary(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: dict(METADATA))
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())
    folder = tmp_path / "2026-01-01-burbujas-y-capex"
    folder.mkdir()
    (folder / "summary.md").write_text("un resumen viejo", encoding="utf-8")

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path), "--force", "--no-open"])

    assert code == 0
    assert not (folder / "summary.md").exists()
    assert folder.is_dir()
    assert (folder / "transcript.json").is_file()


def test_fetch_writes_both_files(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "fetch_metadata", lambda url: dict(METADATA))
    monkeypatch.setattr(cli, "fetch_transcript", lambda url, languages: fake_transcript())

    code = cli.main(["fetch", WATCH, "--out", str(tmp_path), "--date", "2026-01-02", "--no-open"])

    folder = tmp_path / "2026-01-02-burbujas-y-capex"
    assert code == 0
    assert (folder / "transcript.json").is_file()
    txt = folder / "invest-la-pizarra-burbujas-y-capex.txt"
    assert txt.is_file()
    assert txt.read_text(encoding="utf-8").endswith("\n")
    assert json.loads((folder / "transcript.json").read_text(encoding="utf-8"))["source"]["video_id"] == VIDEO_ID