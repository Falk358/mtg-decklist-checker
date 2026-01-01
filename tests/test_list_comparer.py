import pytest


@pytest.mark.parametrize(
    "card_title_decklist, card_title_banlist",
    [
        ("Sol Ring", "Sol Ring"),
        ("Sol Ring", "sol ring"),
        ("Sol Ring", "sol Ring"),
        (" Sol Ring  ", "Sol Ring"),
        ("Sol   Ring", "Sol Ring"),
        ("Tajic, Blade of the Legion", "Tajic, Blade of the Legion"),
    ],
)
def test_card_title_matches(card_title_decklist: str, card_title_banlist: str):
    import list_checker.list_comparer as list_comparer

    assert list_comparer.card_title_matches(card_title_decklist, card_title_banlist)


@pytest.mark.parametrize(
    "card_title_decklist, card_title_banlist",
    [
        ("Reconers Bargain", "Sol Ring"),
        ("Writ of Passage", "Rite of Passage"),
        ("Tajic, Blade of the Legion", "Tajic, Legion's Edge"),
    ],
)
def test_card_title_does_not_match(card_title_decklist: str, card_title_banlist: str):
    import list_checker.list_comparer as list_comparer

    assert not list_comparer.card_title_matches(card_title_decklist, card_title_banlist)


@pytest.fixture()
def pauper_decklist() -> str:
    import list_checker.list_parser as list_parser

    return list_parser.read_file_to_string("tests/test_resources/test_list_mono_red.txt")


@pytest.fixture()
def pauper_banlist() -> str:
    import list_checker.list_parser as list_parser

    return list_parser.read_file_to_string("tests/test_resources/pauper_banlist_2025_12_25.txt")


def test_legal_list_pauper(pauper_decklist: str, pauper_banlist: str):
    import list_checker.list_comparer as list_comparer

    assert list_comparer.list_is_legal_according_to_banlist(pauper_decklist, pauper_banlist)
