import os

import pytest
from sqlalchemy.orm import Session

from list_checker.db_syncer import CardLegality, CardLegalityObj


@pytest.fixture
def db_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), "test_resources/test.db")


def test_db_initated(db_file_path: str):
    from list_checker.db_syncer import init_db

    engine = init_db(db_file_path)
    try:
        conn = engine.connect()
        assert conn
        import sqlalchemy

        needed_column_names = ["id", "name", "game_changer", "legalities"]
        insp = sqlalchemy.inspect(engine)
        assert insp.has_table("card_legalities")
        for curr_col in insp.get_columns("card_legalities"):
            assert curr_col["name"] in needed_column_names
    finally:
        conn.close()
        os.remove(db_file_path)
    assert not os.path.exists(db_file_path)


@pytest.fixture
def card_info_test_example() -> CardLegalityObj:
    return CardLegalityObj(
        id="3d69a3e0-6a2e-475a-964e-0affed1c017d",
        name="Birds of Paradise",
        game_changer=False,
        legalities={
            "standard": "not_legal",
            "future": "not_legal",
            "historic": "legal",
            "timeless": "legal",
            "gladiator": "legal",
            "pioneer": "not_legal",
            "modern": "legal",
            "legacy": "legal",
            "pauper": "not_legal",
            "vintage": "legal",
            "penny": "legal",
            "commander": "legal",
            "oathbreaker": "legal",
            "standardbrawl": "not_legal",
            "brawl": "legal",
            "alchemy": "not_legal",
            "paupercommander": "not_legal",
            "duel": "legal",
            "oldschool": "not_legal",
            "premodern": "legal",
            "predh": "legal",
        },
    )


def test_insert_card_info_db(db_file_path: str, card_info_test_example: CardLegalityObj):
    from list_checker.db_syncer import init_db
    from list_checker.db_syncer import insert_card_info_single

    engine = init_db(db_file_path)
    try:
        insert_card_info_single(engine, card_info_test_example)
        with Session(engine) as session:
            result = session.get(CardLegality, card_info_test_example.id)
            assert result
            assert result.id == card_info_test_example.id
            assert result.name == "Birds of Paradise"

    finally:
        os.remove(db_file_path)
    assert not os.path.exists(db_file_path)


@pytest.fixture
def json_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), "test_resources/test_card_list.json")


def test_read_from_json(json_file_path: str):
    from list_checker.db_syncer import read_from_json_file

    result: list[CardLegalityObj] = read_from_json_file(json_file_path)
    for item in result:
        assert isinstance(item, CardLegalityObj)
        assert len(item.legalities.keys()) == 21


def test_read_json_insert_card_info_batched(json_file_path: str, db_file_path: str):
    from list_checker.db_syncer import read_from_json_file, init_db, insert_card_info_batched

    data_batch: list[CardLegalityObj] = read_from_json_file(json_file_path)
    try:
        engine = init_db(file_path=db_file_path)
        insert_card_info_batched(engine, data_batch)
        with Session(engine) as session:
            from list_checker.db_syncer import CardLegality

            res = session.query(CardLegality).all()
            assert len(res) > 0
            assert len(res) == len(data_batch)
            for item in res:
                assert isinstance(item, CardLegality)
                assert item.id in [data.id for data in data_batch]
    finally:
        os.remove(db_file_path)


def test_read_card_info_not_in_db(json_file_path: str, db_file_path: str):
    from list_checker.db_syncer import read_from_json_file, init_db, insert_card_info_batched, get_card_info_by_name

    data_batch: list[CardLegalityObj] = read_from_json_file(json_file_path)
    try:
        engine = init_db(file_path=db_file_path)
        insert_card_info_batched(engine, data_batch)
        card_name_invalid = "bla bla"
        fetched_card_legalities: CardLegality = get_card_info_by_name(engine, card_name_invalid)
        assert fetched_card_legalities.name == card_name_invalid
        assert not fetched_card_legalities.game_changer
        assert fetched_card_legalities.id == "-1"
        for record in fetched_card_legalities.legalities.values():
            assert record == "card_not_in_db"

    finally:
        os.remove(db_file_path)


class MockScryFallResponse:

    def raise_for_status(self):
        pass

    @staticmethod
    def json():
        return {
            "object": "list",
            "has_more": False,
            "data": [
                {
                    "object": "bulk_data",
                    "id": "1",
                    "type": "oracle_cards",
                    "download_uri": "https://incorrect.entry.url",
                },
                {
                    "object": "bulk_data",
                    "id": "2",
                    "type": "default_cards",
                    "download_uri": "https://correct.entry.url",
                },
            ],
        }


def test_fetch_bulk_data_url(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockScryFallResponse()

    monkeypatch.setattr("requests.get", mock_get)
    from list_checker.db_syncer import fetch_bulk_data_url

    url = fetch_bulk_data_url(
        "https://api.scryfall.com/bulk-data",
    )
    assert url == "https://correct.entry.url"


class MockScryFallIndexError:

    def raise_for_status(self):
        pass

    @staticmethod
    def json():
        return {
            "object": "list",
            "has_more": False,
            "data": [
                {
                    "object": "bulk_data",
                    "id": "1",
                    "type": "oracle_cards",
                    "download_uri": "https://incorrect.entry.url",
                },
                {
                    "object": "bulk_data",
                    "id": "2",
                    "type": "dasf",
                    "download_uri": "https://correct.entry.url",
                },
            ],
        }


def test_fetch_bulk_data_url_fails(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockScryFallIndexError()

    monkeypatch.setattr("requests.get", mock_get)

    from list_checker.db_syncer import fetch_bulk_data_url

    with pytest.raises(IndexError):

        url = fetch_bulk_data_url(
            "https://api.scryfall.com/bulk-data",
        )
