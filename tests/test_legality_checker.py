import os

import pytest
from sqlalchemy import Engine


@pytest.fixture
def db_engine(request):
    filepath = os.path.join(os.path.dirname(__file__), "test_resources/test_legality_fetcher.db")
    jsonpath = os.path.join(os.path.dirname(__file__), "test_resources/test_card_list.json")
    from list_checker.db_syncer import read_from_json_file, init_db, insert_card_info_batched

    engine: Engine = init_db(filepath)
    data_batch: list[dict] = read_from_json_file(jsonpath)
    insert_card_info_batched(engine, data_batch)

    def finalizer():
        os.remove(filepath)

    request.addfinalizer(finalizer)  # request from pytest: add clean up hook
    return engine


@pytest.fixture
def legality_dict() -> dict:
    from test_db_syncer import CardLegality

    return {
        "standard": "not_legal",
        "future": "not_legal",
        "historic": "banned",
        "timeless": "restricted",
        "gladiator": "legal",
        "pioneer": "not_legal",
        "modern": "not_legal",
        "legacy": "banned",
        "pauper": "not_legal",
        "vintage": "restricted",
        "penny": "not_legal",
        "commander": "legal",
        "oathbreaker": "legal",
        "standardbrawl": "not_legal",
        "brawl": "banned",
        "alchemy": "not_legal",
        "paupercommander": "not_legal",
        "duel": "legal",
        "oldschool": "not_legal",
        "premodern": "not_legal",
        "predh": "legal",
    }


def test_fetch_legalities(db_engine: Engine, legality_dict: dict):
    example_card_name = "Demonic Tutor"
    from list_checker.legality_checker import fetch_legalities

    legalities_fetched: dict = fetch_legalities(engine=db_engine, card_name=example_card_name)
    assert legalities_fetched == legality_dict


def test_fetch_legalities_card_not_in_db(db_engine: Engine):
    card_not_in_db = "Tom Bombadil"
    from list_checker.legality_checker import fetch_legalities

    res = fetch_legalities(engine=db_engine, card_name=card_not_in_db)
    for key, value in res.items():
        assert value == "card_not_in_db"
