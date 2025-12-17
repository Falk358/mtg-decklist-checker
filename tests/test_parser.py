import re

import pytest

import list_parser


@pytest.fixture
def parse_line_in_file_incorrect():
    return "44fdafad"


@pytest.fixture
def parse_line_in_file_correct():
    return "38 Mountain"


def test_each_line_starts_with_number(parse_line_in_file_correct: str):
    deck_list_entry_regex = re.compile(r"^[0-9]{1,2}\s.*$")
    match: re.Match = deck_list_entry_regex.match(parse_line_in_file_correct)
    assert match is not None


def test_incorrect_line_fails(parse_line_in_file_incorrect):
    deck_list_entry_regex = re.compile(r"^[0-9]{1,2}\s.*$")
    match: re.Match[str] | None = deck_list_entry_regex.match(parse_line_in_file_incorrect)
    assert match is None


@pytest.fixture
def file_path_test_list() -> str:
    return "tests/test_data/test_list_mono_red.txt"


def test_read_file(file_path_test_list: str):
    import src.list_parser

    list_as_string: str = list_parser.read_file_to_string(file_path_test_list)
    assert list_as_string is not None
    assert type(list_as_string) == str
    assert len(list_as_string) > 0


@pytest.fixture
def test_list_mono_r() -> str:
    return """4 Faithless Looting
4 Fiery Temper
3 Fireblast
4 Grab the Prize
3 Guttersnipe
4 Highway Robbery
4 Kessig Flamebreather
4 Lava Dart
4 Lightning Bolt
18 Mountain
4 Sneaky Snacker
4 Voldaren Epicure

1 Flaring Pain
4 Pyroblast
4 Red Elemental Blast
3 Relic of Progenitus
3 Searing Blaze
"""


def test_split_lines(test_list_mono_r: str):
    import src.list_parser

    lines: list[str] = list_parser.parse_into_lines(test_list_mono_r)
    assert lines is not None
    assert type(lines) == list
    for index, line in enumerate(lines):
        assert type(line) == str
        assert line != "" and len(line) > 0
