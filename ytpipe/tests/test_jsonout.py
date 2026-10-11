from __future__ import annotations

import json
from pathlib import Path

import pytest

from ytpipe.jsonout import build_document
from ytpipe.parse import chunk_cues, cues_to_text, merge_speakers, parse_json3, parse_vtt

FIXTURES = Path(__file__).parent / "fixtures"

VIDEO_ID = "dQw4w9WgXcQ"
URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
FETCHED_AT = "2026-10-09T12:00:00+00:00"

METADATA = {
    "title": "Burbujas y CAPEX",
    "description": "Una charla sobre ciclos y gasto de capital.",
    "channel": "La Pizarra de Andrés",
    "uploader": "La Pizarra de Andrés",
    "uploader_id": "@lapizarra",
    "upload_date": "20260101",
    "duration": 754,
    "ytpipe_subtitle": {"code": "es", "name": "Spanish", "automatic": True},
}

# The fixture yields two cues: one for ANDRÉS and one for INVITADA.
FIRST_CUE = "Hoy hablamos de burbujas y del gasto de capital."
SECOND_CUE = "El ciclo de tipos no ha roto todavía."
PLAIN_TEXT = f"{FIRST_CUE} {SECOND_CUE}"


def document_from_fixture(metadata: dict | None = None, chunk_chars: int = 1200) -> dict:
    """Build the document of the sample video, from the json3 fixture."""
    raw = (FIXTURES / "sample.json3").read_text(encoding="utf-8")
    cues = parse_json3(raw)
    tagged, speakers = merge_speakers(cues)
    text = cues_to_text(tagged)

    return build_document(
        METADATA if metadata is None else metadata,
        tagged,
        speakers,
        chunk_cues(tagged, text, chunk_chars, " "),
        text,
        "json3",
        VIDEO_ID,
        URL,
        FETCHED_AT,
    )


def document_with(upload_date: object) -> dict:
    """Build a document that only carries an upload date."""
    return build_document(
        {"title": "A video", "upload_date": upload_date},
        [],
        [],
        [],
        "",
        "json3",
        VIDEO_ID,
        URL,
        FETCHED_AT,
    )


def test_upload_date_gets_dashes_between_the_parts() -> None:
    assert document_with("20091025")["source"]["upload_date"] == "2009-10-25"


def test_upload_date_keeps_a_value_that_already_has_dashes() -> None:
    assert document_with("2009-10-25")["source"]["upload_date"] == "2009-10-25"


def test_upload_date_is_empty_when_the_metadata_has_none() -> None:
    assert document_with(None)["source"]["upload_date"] == ""
    assert document_with("")["source"]["upload_date"] == ""


def test_upload_date_is_empty_for_a_malformed_value() -> None:
    assert document_with("not-a-date")["source"]["upload_date"] == ""
    assert document_with("2009102")["source"]["upload_date"] == ""


def test_stats_count_every_part_of_the_sample_document() -> None:
    document = document_from_fixture(chunk_chars=40)

    assert document["stats"] == {
        "segment_count": 2,
        "chunk_count": 2,
        "speaker_count": 2,
        "word_count": 17,
        "character_count": 86,
        "time_span_seconds": 8,
    }


def test_word_count_splits_between_the_two_speakers() -> None:
    document = document_from_fixture()

    assert document["speakers"] == [
        {"id": "speaker-1", "name": None, "label": "ANDRÉS", "word_count": 9},
        {"id": "speaker-2", "name": None, "label": "INVITADA", "word_count": 8},
    ]


def test_chunk_offsets_locate_each_chunk_inside_the_plain_text() -> None:
    chunks = document_from_fixture(chunk_chars=40)["chunks"]

    assert [(chunk["text_start"], chunk["text_end"]) for chunk in chunks] == [(0, 48), (49, 86)]
    assert [chunk["text"] for chunk in chunks] == [FIRST_CUE, SECOND_CUE]


def test_joining_the_chunk_text_with_one_space_gives_the_plain_text() -> None:
    chunks = document_from_fixture(chunk_chars=40)["chunks"]

    assert " ".join(chunk["text"] for chunk in chunks) == PLAIN_TEXT


def test_chunks_carry_the_iso_times_and_the_speakers_of_their_cues() -> None:
    chunks = document_from_fixture(chunk_chars=40)["chunks"]

    assert [(chunk["time_start_iso"], chunk["time_end_iso"]) for chunk in chunks] == [
        ("00:00:00", "00:00:04"),
        ("00:00:04", "00:00:08"),
    ]
    assert [chunk["speakers"] for chunk in chunks] == [["speaker-1"], ["speaker-2"]]


def test_segments_carry_the_citation_fields_and_nothing_else() -> None:
    document = document_from_fixture()

    assert document["segments"] == [
        {"index": 0, "speaker": "speaker-1", "start": 0.0, "end": 4.0, "text": FIRST_CUE},
        {"index": 1, "speaker": "speaker-2", "start": 4.0, "end": 8.5, "text": SECOND_CUE},
    ]


def test_the_document_does_not_repeat_the_text_in_a_full_text_field() -> None:
    document = document_from_fixture()

    assert "full_text" not in document


def test_source_carries_the_video_description() -> None:
    assert document_from_fixture()["source"]["description"] == "Una charla sobre ciclos y gasto de capital."


def test_source_description_is_empty_when_the_metadata_has_none() -> None:
    document = document_from_fixture(metadata={**METADATA, "description": None})

    assert document["source"]["description"] == ""


def test_source_says_that_the_video_has_speaker_labels() -> None:
    assert document_from_fixture()["source"]["has_speaker_labels"] is True


def test_chapters_carry_the_bounds_of_every_chapter() -> None:
    metadata = {
        **METADATA,
        "chapters": [
            {"start_time": 0.0, "end_time": 120.5, "title": "Introducción"},
            {"start_time": 120.5, "end_time": 400.0, "title": "El ciclo"},
        ],
    }

    assert document_from_fixture(metadata)["chapters"] == [
        {"index": 0, "start": 0.0, "start_iso": "00:00:00", "end": 120.5, "end_iso": "00:02:00", "title": "Introducción"},
        {"index": 1, "start": 120.5, "start_iso": "00:02:00", "end": 400.0, "end_iso": "00:06:40", "title": "El ciclo"},
    ]


def test_a_video_without_chapters_has_no_chapters_key() -> None:
    assert "chapters" not in document_from_fixture()
    assert "chapters" not in document_from_fixture(metadata={**METADATA, "chapters": []})


def test_chapter_bounds_are_zero_when_the_metadata_leaves_them_out() -> None:
    metadata = {**METADATA, "chapters": [{"title": "Sin horas"}]}

    chapter = document_from_fixture(metadata)["chapters"][0]

    assert (chapter["start"], chapter["end"]) == (0.0, 0.0)
    assert chapter["title"] == "Sin horas"


def test_a_transcript_without_labels_has_no_speaker() -> None:
    """No cue carries a label, so no person is invented."""
    cues = parse_vtt((FIXTURES / "sample.vtt").read_text(encoding="utf-8"))
    tagged, speakers = merge_speakers(cues)
    text = cues_to_text(tagged)

    document = build_document(
        METADATA, tagged, speakers, chunk_cues(tagged, text, 1200, " "), text, "vtt", VIDEO_ID, URL, FETCHED_AT
    )

    assert [cue["speaker"] for cue in tagged] == [None, None, None]
    assert "speakers" not in document
    assert document["source"]["has_speaker_labels"] is False
    assert document["stats"]["speaker_count"] == 0
    assert {segment["speaker"] for segment in document["segments"]} == {None}
    assert all(chunk["speakers"] == [] for chunk in document["chunks"])


def test_a_transcript_with_labels_keeps_the_numbered_speakers() -> None:
    document = document_from_fixture()

    assert [segment["speaker"] for segment in document["segments"]] == ["speaker-1", "speaker-2"]
    assert document["source"]["has_speaker_labels"] is True
    assert document["stats"]["speaker_count"] == 2


def test_a_speaker_name_survives_into_the_document() -> None:
    cues = [{"start": 0.0, "end": 1.0, "text": "Hola", "speaker_label": "ANDRÉS"}]
    tagged, speakers = merge_speakers(cues)
    speakers[0]["name"] = "Andrés"
    text = cues_to_text(tagged)

    document = build_document(
        METADATA, tagged, speakers, chunk_cues(tagged, text, 1200, " "), text, "json3", VIDEO_ID, URL, FETCHED_AT
    )

    assert document["speakers"][0]["name"] == "Andrés"


def test_time_span_seconds_uses_the_last_end_of_a_late_transcript() -> None:
    """A transcript that starts at 10:00 and ends at 10:03 spans three minutes."""
    cues = [
        {"start": 600.0, "end": 620.0, "text": "Primera"},
        {"start": 620.0, "end": 663.0, "text": "Segunda"},
    ]
    tagged, speakers = merge_speakers(cues)
    text = cues_to_text(tagged)

    document = build_document(
        METADATA, tagged, speakers, chunk_cues(tagged, text, 1200, " "), text, "json3", VIDEO_ID, URL, FETCHED_AT
    )

    assert document["stats"]["time_span_seconds"] == 663


def test_time_span_seconds_is_zero_for_a_transcript_with_no_cue() -> None:
    assert document_with(None)["stats"]["time_span_seconds"] == 0


@pytest.mark.parametrize(
    ("events", "expected_ends"),
    [
        pytest.param(
            [
                {"tStartMs": 0, "segs": [{"utf8": "Hola"}]},
                {"tStartMs": 3000, "dDurationMs": 1000, "segs": [{"utf8": "Adiós"}]},
            ],
            [3.0, 4.0],
            id="middle_cue_gets_the_next_start",
        ),
        pytest.param(
            [
                {"tStartMs": 1000, "dDurationMs": 500, "segs": [{"utf8": "Hola"}]},
                {"tStartMs": 3000, "segs": [{"utf8": "Adiós"}]},
            ],
            [1.5, 3.0],
            id="last_cue_keeps_its_own_end",
        ),
    ],
)
def test_a_cue_without_a_duration_ends_where_the_next_one_starts(events: list[dict], expected_ends: list[float]) -> None:
    cues = parse_json3(json.dumps({"events": events}))

    assert [cue["end"] for cue in cues] == expected_ends


def test_a_null_duration_does_not_crash_the_json3_parser() -> None:
    raw = json.dumps({"events": [{"tStartMs": None, "dDurationMs": None, "segs": [{"utf8": "Hola"}]}]})

    assert parse_json3(raw) == [{"start": 0.0, "end": 0.0, "text": "Hola"}]


def test_parse_json3_fails_when_the_payload_has_no_cue() -> None:
    with pytest.raises(ValueError, match="json3 payload has no cue"):
        parse_json3(json.dumps({"events": [{"tStartMs": 0, "segs": [{"utf8": "\n"}]}]}))


def test_parse_vtt_fills_a_zero_length_end_from_the_next_cue() -> None:
    raw = "WEBVTT\n\n00:01.000 --> 00:01.000\nPrimera\n\n00:04.000 --> 00:06.000\nSegunda\n"

    cues = parse_vtt(raw)

    assert [(cue["start"], cue["end"]) for cue in cues] == [(1.0, 4.0), (4.0, 6.0)]