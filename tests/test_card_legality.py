from typing import Any, Generator, LiteralString

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Engine, create_engine, Column, String, Integer, text
from sqlalchemy.orm import sessionmaker
import os

import configparser
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def test_client():
    client = TestClient(app, raise_server_exceptions=True)
    yield client


def test_cardname_endpoint_responds_with_200(test_client: TestClient):
    response = test_client.post(url="/cardlegality", json={"card_name": "Sol Ring"})
    print(response.json())
    assert response.status_code == 200


@pytest.fixture
def db_filepath(request):
    db_filepath: LiteralString | str | bytes = os.path.join(
        os.path.dirname(__file__), "test_resources/test_card_api_routes_card_legality.db"
    )

    return db_filepath


@pytest.fixture
def db_engine(request, db_filepath) -> Generator[Engine, Any, None]:

    def finalizer():
        if os.path.isfile(db_filepath):
            os.remove(db_filepath)
            print(f"deleting {db_filepath} in finalizer of {__name__}")
        else:
            print(f"db file {db_filepath} does not exist in finalizer of {__name__}")

    engine: Engine = create_engine(f"sqlite:///{db_filepath}")
    # init with base table
    Base = declarative_base()

    class TestEntry(Base):
        __tablename__ = "test_table"
        id = Column(Integer, primary_key=True)
        value = Column(String)

    Base.metadata.create_all(engine)

    test_entry: TestEntry = TestEntry(id=0, value="already_exists")
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(test_entry)
    session.commit()
    session.close()
    request.addfinalizer(finalizer)
    yield engine


def test_open_db_when_db_file_already_exists_yields_existing_db(db_filepath: str, db_engine: Engine, monkeypatch):
    top_directory_of_db_file: str = os.path.dirname(db_filepath)
    db_file_name: str = os.path.basename(db_filepath)

    assert db_file_name in os.listdir(top_directory_of_db_file)

    def mock_config_file(myself: object, field: str, subfield: str) -> str:
        return db_filepath

    monkeypatch.setattr(configparser.ConfigParser, "get", mock_config_file)

    from api.routes.card_legality import open_db

    res = open_db()
    assert isinstance(res, Engine)
    with res.connect() as conn:
        result = conn.execute(text("SELECT value FROM test_table WHERE id = 0"))
        for row in result:
            assert row[0] == "already_exists"
