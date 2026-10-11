from __future__ import annotations

from urllib.error import HTTPError

import pytest

import ytpipe.fetch as fetch

WATCH = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_one_per_language_keeps_the_json3_entry_of_a_track() -> None:
    tracks = [
        {"code": "es", "name": "Spanish", "automatic": False, "ext": "vtt", "url": "u1"},
        {"code": "es", "name": "Spanish", "automatic": False, "ext": "json3", "url": "u2"},
    ]

    result = fetch._one_per_language(tracks)

    assert result == [{"code": "es", "name": "Spanish", "automatic": False}]


def test_one_per_language_keeps_a_track_with_one_format() -> None:
    tracks = [
        {"code": "fr", "name": "French", "automatic": True, "ext": "vtt", "url": "u1"},
    ]

    result = fetch._one_per_language(tracks)

    assert result == [{"code": "fr", "name": "French", "automatic": True}]


def test_one_per_language_returns_nothing_for_an_empty_dict() -> None:
    assert fetch._one_per_language([]) == []


def test_one_per_language_sorts_by_code_and_drops_the_format_fields() -> None:
    tracks = [
        {"code": "en", "name": "English", "automatic": True, "ext": "vtt", "url": "u1"},
        {"code": "es", "name": "Spanish", "automatic": False, "ext": "json3", "url": "u2"},
        {"code": "de", "name": "German", "automatic": False, "ext": "vtt", "url": "u3"},
    ]

    result = fetch._one_per_language(tracks)

    assert [track["code"] for track in result] == ["de", "en", "es"]
    assert result[1] == {"code": "en", "name": "English", "automatic": True}


def test_one_per_language_keeps_the_first_entry_when_the_format_order_ties() -> None:
    tracks = [
        {"code": "en", "name": "English", "automatic": False, "ext": "json3", "url": "u1"},
        {"code": "en", "name": "English (auto)", "automatic": True, "ext": "json3", "url": "u2"},
    ]

    result = fetch._one_per_language(tracks)

    assert result == [{"code": "en", "name": "English", "automatic": False}]


def _metadata_with_tracks() -> dict:
    """Return an info dict with a manual `en` track and an auto `es` translation."""
    return {
        "subtitles": {
            "en": [
                {"ext": "json3", "url": "manual-en", "name": "English"},
                {"ext": "vtt", "url": "manual-en-vtt", "name": "English"},
            ]
        },
        "automatic_captions": {
            "es": [{"ext": "json3", "url": "auto-es", "name": "Spanish (auto-generated)"}],
            "fr": [{"ext": "json3", "url": "auto-fr", "name": "French (auto-generated)"}],
        },
    }


def test_pick_track_prefers_a_manual_track_of_a_later_language(monkeypatch) -> None:
    monkeypatch.setattr(fetch, "_cue_count", lambda url, ext: 10)
    wanted = ["es", "en"]

    track = fetch._pick_track(_metadata_with_tracks(), wanted)

    assert track["code"] == "en"
    assert track["automatic"] is False


def test_pick_track_takes_the_auto_track_when_no_manual_track_matches(monkeypatch) -> None:
    monkeypatch.setattr(fetch, "_cue_count", lambda url, ext: 10)

    track = fetch._pick_track(_metadata_with_tracks(), ["es", "fr"])

    assert track["code"] == "es"
    assert track["automatic"] is True


def test_pick_track_skips_a_language_that_has_no_track(monkeypatch) -> None:
    metadata = _metadata_with_tracks()
    metadata["subtitles"] = {"de": [{"ext": "json3", "url": "manual-de", "name": "German"}]}
    monkeypatch.setattr(fetch, "_cue_count", lambda url, ext: 10)

    assert fetch._pick_track(metadata, ["es", "de"])["code"] == "de"


def test_pick_track_fails_when_no_language_matches(monkeypatch) -> None:
    monkeypatch.setattr(fetch, "_cue_count", lambda url, ext: 10)

    with pytest.raises(RuntimeError, match="no subtitle available"):
        fetch._pick_track(_metadata_with_tracks(), ["pt"])


def test_format_rank_places_an_unknown_format_last() -> None:
    known = {"ext": "json3"}
    unknown = {"ext": "srv3"}

    assert fetch._format_rank(known) < fetch._format_rank(unknown)


def _rate_limited() -> HTTPError:
    return HTTPError(WATCH, 429, "Too Many Requests", {}, None)


def test_transcript_waits_out_a_rate_limit_and_comes_back(monkeypatch) -> None:
    calls = {"count": 0}
    waits: list[float] = []

    def flaky(url: str, wanted: list[str]) -> tuple[dict, str, str]:
        calls["count"] += 1
        if calls["count"] < 3:
            raise _rate_limited()

        return {"title": "A video"}, "Hola", "json3"

    monkeypatch.setattr(fetch, "_download_transcript", flaky)
    monkeypatch.setattr(fetch.time, "sleep", waits.append)

    metadata, raw, subtitle_format = fetch.fetch_transcript(WATCH, ["en"])

    assert raw == "Hola"
    assert subtitle_format == "json3"
    assert metadata["title"] == "A video"
    assert calls["count"] == 3
    assert waits == [5, 15]


def test_transcript_gives_up_after_the_third_wait(monkeypatch) -> None:
    calls = {"count": 0}
    waits: list[float] = []

    def always_limited(url: str, wanted: list[str]) -> tuple[dict, str, str]:
        calls["count"] += 1
        raise _rate_limited()

    monkeypatch.setattr(fetch, "_download_transcript", always_limited)
    monkeypatch.setattr(fetch.time, "sleep", waits.append)

    with pytest.raises(RuntimeError, match="after 4 attempts") as raised:
        fetch.fetch_transcript(WATCH, ["en"])

    assert WATCH in str(raised.value)
    assert calls["count"] == 4
    assert waits == [5, 15, 45]


def test_transcript_lets_another_error_through(monkeypatch) -> None:
    waits: list[float] = []

    def broken(url: str, wanted: list[str]) -> tuple[dict, str, str]:
        raise RuntimeError("no subtitle available")

    monkeypatch.setattr(fetch, "_download_transcript", broken)
    monkeypatch.setattr(fetch.time, "sleep", waits.append)

    with pytest.raises(RuntimeError, match="no subtitle available"):
        fetch.fetch_transcript(WATCH, ["en"])

    assert waits == []