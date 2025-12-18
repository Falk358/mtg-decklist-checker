import pytest

import list_checker.list_parser as list_parser


ERR = (-1, "ERR")


@pytest.fixture
def parse_line_in_file_incorrect():
    return "44fdafad"


@pytest.fixture
def parse_line_in_file_correct():
    return "38 Mountain"


def test_each_line_starts_with_number(parse_line_in_file_correct: str):
    assert list_parser.check_starts_with_count(parse_line_in_file_correct)


def test_incorrect_line_fails(parse_line_in_file_incorrect):
    assert not list_parser.check_starts_with_count(parse_line_in_file_incorrect)


@pytest.fixture
def file_path_mono_red_list() -> str:
    return "tests/test_data/test_list_mono_red.txt"


def test_read_file(file_path_mono_red_list: str):
    list_as_string: str = list_parser.read_file_to_string(file_path_mono_red_list)
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

    lines: list[str] = list_parser.parse_into_lines(test_list_mono_r)
    assert lines is not None
    assert type(lines) == list
    for index, line in enumerate(lines):
        assert type(line) == str
        assert line != "" and len(line) > 0


@pytest.fixture
def pauper_banlist_entry() -> str:
    return "1 _____-o-saurus"


def test_parse_pauper_banlist(pauper_banlist_entry: str):
    import list_checker.list_parser as list_parser

    parsed_lines: list[str] = list_parser.parse_into_lines(pauper_banlist_entry)
    final: tuple = list_parser.parse_line_to_count_and_card_title(parsed_lines[0])
    assert final[0] == 1
    assert final[1] == "_____-o-saurus"


@pytest.mark.parametrize(
    "line_for_parsing_incorrect", ["44fda5ad", "333 Relic of Progenitus", "fda 3333fdsaff adfaf f"]
)
def test_line_parses_with_incorrect_data_to_none(line_for_parsing_incorrect: str):

    should_be_None = list_parser.parse_line_to_count_and_card_title(line_for_parsing_incorrect)
    assert should_be_None == ERR


@pytest.fixture()
def line_for_parsing_correct() -> str:
    return "3 Relic of Progenitus"


def test_line_parses_to_count_and_card_title(line_for_parsing_correct: str):

    line_parsed: tuple[int, str] = list_parser.parse_line_to_count_and_card_title(line_for_parsing_correct)
    assert line_parsed is not None
    assert type(line_parsed) == tuple
    assert line_parsed[0] == 3
    assert line_parsed[1] == "Relic of Progenitus"


def test_file_parsed_to_count_and_card_title(test_list_mono_r: str):
    import list_checker.list_parser as list_parser

    list_parsed_tuples: list[tuple] = list_parser.parse_string_to_count_and_card_title(test_list_mono_r)
    for curr_tuple in list_parsed_tuples:
        assert curr_tuple[0] != ERR[0]
        assert curr_tuple[1] != ERR[1]
