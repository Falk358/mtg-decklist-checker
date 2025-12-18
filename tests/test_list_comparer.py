import pytest


# @pytest.fixture
# def card_title_banlist() -> str:
#    return "Sol Ring"
#
#
# @pytest.fixture
# def card_title_decklist() -> str:
#    return "sol Ring"


@pytest.mark.parametrize(
    "card_title_decklist, card_title_banlist",
    [
        ("Sol Ring", "Sol Ring"),
        ("Sol Ring", "sol ring"),
        ("Sol Ring", "sol Ring"),
        (" Sol Ring  ", "Sol Ring"),
        ("Sol   Ring", "Sol Ring"),
    ],
)
def test_card_title_matches(card_title_decklist: str, card_title_banlist: str):
    import list_checker.list_comparer as list_comparer

    assert list_comparer.card_title_matches(card_title_decklist, card_title_banlist)
