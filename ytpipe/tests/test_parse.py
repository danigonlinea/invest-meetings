from __future__ import annotations

import json
from pathlib import Path

import pytest

from ytpipe.jsonout import iso_time
from ytpipe.parse import (
    _longest_suffix_prefix,
    chunk_cues,
    cues_to_text,
    merge_speakers,
    parse_json3,
    parse_vtt,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_json3_keeps_two_cues() -> None:
    raw = json.dumps(
        {
            "events": [
                {"tStartMs": 1000, "dDurationMs": 1500, "segs": [{"utf8": "Primer segmento"}]},
                {"tStartMs": 4000, "dDurationMs": 2000, "segs": [{"utf8": "Segundo segmento"}]},
            ]
        }
    )

    cues = parse_json3(raw)

    assert cues == [
        {"start": 1.0, "end": 2.5, "text": "Primer segmento"},
        {"start": 4.0, "end": 6.0, "text": "Segundo segmento"},
    ]


def test_parse_json3_turns_newline_into_a_space() -> None:
    raw = json.dumps(
        {
            "events": [
                {
                    "tStartMs": 0,
                    "dDurationMs": 1000,
                    "segs": [{"utf8": "Hola\n"}, {"utf8": "mundo"}],
                }
            ]
        }
    )

    cues = parse_json3(raw)

    assert [cue["text"] for cue in cues] == ["Hola mundo"]


def test_parse_json3_drops_empty_cues() -> None:
    raw = json.dumps({"events": [{"tStartMs": 0, "segs": [{"utf8": "\n"}]}, {"tStartMs": 10, "segs": [{"utf8": "Texto"}]}]})

    cues = parse_json3(raw)

    assert len(cues) == 1
    assert cues[0]["text"] == "Texto"


def test_parse_json3_merges_rolling_captions_of_one_speaker() -> None:
    raw = (FIXTURES / "sample.json3").read_text(encoding="utf-8")

    cues = parse_json3(raw)

    assert [cue["text"] for cue in cues] == [
        "Hoy hablamos de burbujas y del gasto de capital.",
        "El ciclo de tipos no ha roto todavía.",
    ]
    assert [cue["speaker_label"] for cue in cues] == ["ANDRÉS", "INVITADA"]
    assert [(cue["start"], cue["end"]) for cue in cues] == [(0.0, 4.0), (4.0, 8.5)]


def test_parse_json3_merges_rolling_captions_without_repeating_a_word() -> None:
    raw = (FIXTURES / "rolling.json3").read_text(encoding="utf-8")

    cues = parse_json3(raw)

    assert [cue["text"] for cue in cues] == ["hello world and more"]
    assert cues[0]["end"] == 6.0
    words = cues[0]["text"].split()
    assert len(words) == len(set(words))


def test_longest_suffix_prefix_counts_a_full_overlap() -> None:
    assert _longest_suffix_prefix("hello world and", "hello world and more") == 15


def test_longest_suffix_prefix_counts_a_partial_overlap() -> None:
    assert _longest_suffix_prefix("hello world and", "and more") == 3


def test_longest_suffix_prefix_returns_zero_without_an_overlap() -> None:
    assert _longest_suffix_prefix("hello world", "and more") == 0


def test_longest_suffix_prefix_ignores_case() -> None:
    assert _longest_suffix_prefix("Hello World", "hello world and") == 11


def test_parse_json3_fails_on_invalid_json() -> None:
    with pytest.raises(ValueError, match="not valid JSON"):
        parse_json3("{not json")


def test_parse_json3_fails_without_events() -> None:
    with pytest.raises(ValueError, match="no 'events' key"):
        parse_json3(json.dumps({"wireMagic": "pb3"}))


def test_parse_vtt_reads_the_hms_form() -> None:
    raw = (FIXTURES / "sample.vtt").read_text(encoding="utf-8")

    cues = parse_vtt(raw)

    assert cues[0] == {"start": 2.4, "end": 5.1, "text": "Bienvenidos a La Pizarra de Andrés."}


def test_parse_vtt_skips_note_and_style_blocks() -> None:
    raw = (FIXTURES / "sample.vtt").read_text(encoding="utf-8")

    texts = [cue["text"] for cue in parse_vtt(raw)]

    assert len(texts) == 3
    assert all("color: white" not in text for text in texts)
    assert all("transcripción" not in text for text in texts)


def test_parse_vtt_reads_the_ms_form() -> None:
    raw = "WEBVTT\n\n00:05.100 --> 00:09.850\nHoy hablamos de burbujas.\n"

    cues = parse_vtt(raw)

    assert cues == [{"start": 5.1, "end": 9.85, "text": "Hoy hablamos de burbujas."}]


def test_parse_vtt_drops_a_duplicate_cue() -> None:
    raw = (
        "WEBVTT\n\n"
        "00:01.000 --> 00:02.000\nEl ciclo aguanta.\n\n"
        "00:01.000 --> 00:02.000\nEl ciclo aguanta.\n"
    )

    assert len(parse_vtt(raw)) == 1


def test_parse_vtt_merges_rolling_captions_without_repeating_a_word() -> None:
    raw = (FIXTURES / "rolling.vtt").read_text(encoding="utf-8")

    cues = parse_vtt(raw)

    assert [cue["text"] for cue in cues] == ["hello world", "and", "more"]
    assert [(cue["start"], cue["end"]) for cue in cues] == [(0.0, 2.0), (2.0, 4.0), (4.0, 6.0)]
    words = cues_to_text(cues).split()
    assert words == ["hello", "world", "and", "more"]


def test_parse_vtt_fails_when_no_cue_exists() -> None:
    with pytest.raises(ValueError, match="no cue"):
        parse_vtt("WEBVTT\n\nNOTE Solo una nota.\n")


def test_merge_speakers_numbers_two_speakers_by_appearance() -> None:
    cues = [
        {"start": 0.0, "end": 1.0, "text": "Hola", "speaker_label": "ANDRÉS"},
        {"start": 1.0, "end": 2.0, "text": "Gracias", "speaker_label": "INVITADO"},
    ]

    tagged, speakers = merge_speakers(cues)

    assert [cue["speaker"] for cue in tagged] == ["speaker-1", "speaker-2"]
    assert speakers == [
        {"id": "speaker-1", "name": None, "label": "ANDRÉS"},
        {"id": "speaker-2", "name": None, "label": "INVITADO"},
    ]


def test_merge_speakers_keeps_one_speaker_for_one_label() -> None:
    cues = [
        {"start": 0.0, "end": 1.0, "text": "Hola", "speaker_label": "ANDRÉS"},
        {"start": 1.0, "end": 2.0, "text": "Sigue", "speaker_label": "ANDRÉS"},
    ]

    tagged, speakers = merge_speakers(cues)

    assert [cue["speaker"] for cue in tagged] == ["speaker-1", "speaker-1"]
    assert len(speakers) == 1


def test_merge_speakers_gives_no_speaker_when_no_label_exists() -> None:
    cues = [
        {"start": 0.0, "end": 1.0, "text": "Hola"},
        {"start": 1.0, "end": 2.0, "text": "Gracias"},
    ]

    tagged, speakers = merge_speakers(cues)

    assert [cue["speaker"] for cue in tagged] == [None, None]
    assert speakers == []


def test_cues_to_text_collapses_whitespace() -> None:
    cues = [{"start": 0.0, "end": 1.0, "text": "El   ciclo"}]

    assert cues_to_text(cues) == "El ciclo"
    assert cues_to_text([]) == ""


def test_chunk_cues_puts_short_cues_in_one_chunk() -> None:
    cues = [
        {"start": 0.0, "end": 2.0, "text": "Primera frase"},
        {"start": 2.0, "end": 4.0, "text": "Segunda frase"},
    ]
    text = cues_to_text(cues)

    chunks = chunk_cues(cues, text)

    assert len(chunks) == 1
    assert chunks[0]["index"] == 0
    assert chunks[0]["char_start"] == 0
    assert chunks[0]["char_end"] == len(text)
    assert chunks[0]["text"] == text
    assert chunks[0]["speakers"] == []
    assert chunks[0]["time_start"] == 0.0
    assert chunks[0]["time_end"] == 4.0


def test_chunk_cues_splits_long_cues_into_chunks_that_fit() -> None:
    cues = [
        {"start": 0.0, "end": 2.0, "text": "a" * 400},
        {"start": 2.0, "end": 4.0, "text": "b" * 400},
        {"start": 4.0, "end": 6.0, "text": "c" * 400},
        {"start": 6.0, "end": 8.0, "text": "d" * 400},
    ]
    text = cues_to_text(cues)

    chunks = chunk_cues(cues, text)

    assert [chunk["index"] for chunk in chunks] == [0, 1]
    assert chunks[0]["char_start"] == 0
    assert chunks[0]["char_end"] == 801
    assert chunks[1]["char_start"] == 802
    assert chunks[1]["char_end"] == len(text)
    assert chunks[1]["time_start"] == 4.0
    assert chunks[1]["time_end"] == 8.0
    assert text.replace(" ", "") == "".join(chunk["text"].replace(" ", "") for chunk in chunks)
    assert text[chunks[1]["char_start"] : chunks[1]["char_end"]] == chunks[1]["text"]


def test_chunk_cues_does_not_count_the_separator_of_a_flushed_group() -> None:
    """A chunk holds at most `target_chars` characters, separator included."""
    target = 12
    cues = [
        {"start": 0.0, "end": 1.0, "text": "abcde", "speaker": "speaker-1"},
        {"start": 1.0, "end": 2.0, "text": "abcde", "speaker": "speaker-1"},
        {"start": 2.0, "end": 3.0, "text": "abcde", "speaker": "speaker-1"},
        {"start": 3.0, "end": 4.0, "text": "abcde", "speaker": "speaker-1"},
    ]
    text = cues_to_text(cues)

    chunks = chunk_cues(cues, text, target_chars=target)

    assert [chunk["text"] for chunk in chunks] == ["abcde abcde", "abcde abcde"]
    assert all(len(chunk["text"]) <= target for chunk in chunks)


def test_chunk_cues_uses_the_length_of_the_separator() -> None:
    """A separator of two characters counts as two, not as one."""
    cues = [{"start": 0.0, "end": 1.0, "text": "abcde"}, {"start": 1.0, "end": 2.0, "text": "abcde"}]
    text = "abcde  abcde"

    chunks = chunk_cues(cues, text, target_chars=11, separator="  ")

    assert [chunk["text"] for chunk in chunks] == ["abcde", "abcde"]


def test_chunk_cues_names_the_cue_it_cannot_find() -> None:
    cues = [{"start": 0.0, "end": 1.0, "text": "Primera"}, {"start": 1.0, "end": 2.0, "text": "Ausente"}]

    with pytest.raises(ValueError, match="cue 1"):
        chunk_cues(cues, "Primera sola")


def test_iso_time_returns_zero_for_zero() -> None:
    assert iso_time(0) == "00:00:00"


def test_iso_time_returns_zero_for_eight_seconds() -> None:
    assert iso_time(8) == "00:00:08"


def test_iso_time_returns_one_hour_and_one_second() -> None:
    assert iso_time(3661) == "01:01:01"


def test_iso_time_returns_zero_for_a_negative_value() -> None:
    assert iso_time(-42) == "00:00:00"