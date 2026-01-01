import os

import pytest


@pytest.fixture
def db_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), "test_resources/test.db")


def test_db_initated(db_file_path: str):
    print(f"file_path from fixture: {db_file_path}")
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
