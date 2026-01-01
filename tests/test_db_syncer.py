import os

import pytest


@pytest.fixture
def db_file_path() -> str:
    return os.path.join(os.path.dirname(__file__), "test_resources/test.db")


def test_db_initated(db_file_path: str):
    print(f"file_path from fixture: {db_file_path}")
    from list_checker.db_syncer import init_db

    engine = init_db(db_file_path)
    with engine.connect() as conn:
        assert conn
        assert os.path.exists(db_file_path)
    os.remove(db_file_path)
    assert not os.path.exists(db_file_path)
