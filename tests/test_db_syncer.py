import os

import pytest
from sqlalchemy.orm import Session

from list_checker.db_syncer import CardLegality


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
def card_info_test_example() -> dict:
    return {
        "id": "3d69a3e0-6a2e-475a-964e-0affed1c017d",
        "name": "Birds of Paradise",
        "game_changer": False,
        "legalities": {
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
    }


def test_insert_card_info_db(db_file_path: str, card_info_test_example: dict):
    from list_checker.db_syncer import init_db
    from list_checker.db_syncer import insert_card_info_db

    engine = init_db(db_file_path)
    try:
        insert_card_info_db(engine, card_info_test_example)
        with Session(engine) as session:
            result = session.get(CardLegality, card_info_test_example["id"])
            assert result
            assert result.id == card_info_test_example["id"]
            assert result.name == "Birds of Paradise"

    finally:
        os.remove(db_file_path)
    assert not os.path.exists(db_file_path)


@pytest.fixture
def json_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), "test_resources/test_card_list.json")


def test_read_from_json(json_file_path: str):
    from list_checker.db_syncer import read_from_json

    result: list[dict] = read_from_json(json_file_path)
    assert len(result) == 3
    for item in result:
        assert type(item) == dict
        assert "id" in item.keys()
        assert "name" in item.keys()
        assert "game_changer" in item.keys()
        assert "legalities" in item.keys()
        assert type(item["name"]) == str
        assert type(item["game_changer"]) == bool
        assert type(item["legalities"]) == dict
        assert len(item["legalities"].keys()) == 21
        assert len(item.keys()) == 4


def test_read_json_insert_card_info_batched(json_file_path: str, db_file_path: str):
    from list_checker.db_syncer import read_from_json, init_db, insert_card_info_batched

    data_batch: list[dict] = read_from_json(json_file_path)
    assert len(data_batch) == 3
    try:
        engine = init_db(file_path=db_file_path)
        insert_card_info_batched(engine, data_batch)
        with Session(engine) as session:
            from list_checker.db_syncer import CardLegality

            res = session.query(CardLegality).all()
            assert len(res) > 0
            assert len(res) == len(data_batch)
            for item in res:
                assert type(item) == CardLegality
                assert item.id in [data["id"] for data in data_batch]
    finally:
        os.remove(db_file_path)
