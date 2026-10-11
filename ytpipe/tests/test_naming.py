from __future__ import annotations

import pytest

from ytpipe.naming import folder_name, slugify, transcript_filename


def test_slugify_strips_accents() -> None:
    assert slugify("Añadir información útil") == "anadir-informacion-util"


def test_slugify_lowercases_mixed_case() -> None:
    assert slugify("La Pizarra de Andrés") == "la-pizarra-de-andres"


def test_slugify_replaces_punctuation_with_one_hyphen() -> None:
    assert slugify("Burbujas, concentración; y CAPEX... ¿en el S&P 500?", max_words=9) == (
        "burbujas-concentracion-y-capex-en-el-s-p-500"
    )


def test_slugify_keeps_ten_words_by_default() -> None:
    assert slugify("Burbujas, concentración; y CAPEX... ¿en el S&P 500?") == (
        "burbujas-concentracion-y-capex-en-el-s-p-500"
    )


def test_slugify_keeps_only_the_first_max_words() -> None:
    assert slugify("uno dos tres cuatro cinco seis siete", max_words=3) == "uno-dos-tres"


def test_slugify_drops_a_trailing_connector() -> None:
    assert slugify("El mercado de la vivienda en España de") == "el-mercado-de-la-vivienda-en-espana"


def test_slugify_drops_the_trailing_connector_left_by_the_word_budget() -> None:
    assert slugify("El mercado de la vivienda en España de", max_words=4) == "el-mercado"


def test_slugify_drops_a_run_of_three_trailing_connectors() -> None:
    assert slugify("Burbujas en el sector de la vivienda y en el") == (
        "burbujas-en-el-sector-de-la-vivienda"
    )


def test_slugify_keeps_one_word_from_a_title_of_only_connectors() -> None:
    assert slugify("de la el y o en") == "de"


def test_slugify_keeps_one_word_when_the_budget_leaves_a_connector() -> None:
    assert slugify("El mercado de", max_words=1) == "el"


def test_slugify_returns_empty_for_input_without_letters_or_digits() -> None:
    assert slugify("!!! ¿¿ ...") == ""


def test_folder_name_joins_a_good_date_and_a_slug() -> None:
    assert folder_name("2026-10-09", "la-pizarra-burbujas") == "2026-10-09-la-pizarra-burbujas"


def test_folder_name_fails_on_a_bad_date() -> None:
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        folder_name("09-10-2026", "la-pizarra-burbujas")


def test_transcript_filename_joins_a_channel_and_a_topic() -> None:
    assert transcript_filename("La Pizarra de Andrés", "Burbujas y CAPEX") == (
        "invest-la-pizarra-burbujas-y-capex.txt"
    )


def test_transcript_filename_fails_on_an_empty_slug() -> None:
    with pytest.raises(ValueError, match="channel_slug"):
        transcript_filename("!!!", "Burbujas")

    with pytest.raises(ValueError, match="topic_slug"):
        transcript_filename("La Pizarra", "???")


def test_transcript_filename_drops_the_connector_the_channel_cut_leaves() -> None:
    assert transcript_filename("La Pizarra de Andrés Vega", "IA") == (
        "invest-la-pizarra-ia.txt"
    )


def test_transcript_filename_keeps_more_than_six_topic_words() -> None:
    name = transcript_filename(
        "El Arte de Invertir",
        "SpaceX: ¿Vale 2 trillones o es el IPO más caro de la historia?",
    )

    assert name == "invest-el-arte-spacex-vale-2-trillones-o-es-el-ipo-mas-caro.txt"

    topic_words = name.removeprefix("invest-el-arte-").removesuffix(".txt").split("-")
    assert len(topic_words) > 6