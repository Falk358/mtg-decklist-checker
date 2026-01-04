import os

from requests import RequestException
from sqlalchemy import Column, String, JSON, create_engine, Table, MetaData, Boolean, Uuid
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, Session


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, str]: JSON}


class CardLegality(Base):
    __tablename__ = "card_legalities"

    id: Mapped[str] = MappedColumn(primary_key=True)
    name: Mapped[str] = MappedColumn(index=True)
    game_changer: Mapped[bool] = MappedColumn()
    legalities: Mapped[dict[str, str]] = MappedColumn()


def init_db(file_path: str):
    if os.path.exists(file_path):
        raise FileExistsError(f"[ERROR] DB: {file_path} already exists; skipping init")
    engine = create_engine(f"sqlite:///{file_path}")
    CardLegality.metadata.create_all(engine)
    return engine


def insert_card_info_single(engine: Engine, card_info_obj: dict):
    card_orm_obj = CardLegality(**card_info_obj)
    with Session(engine) as session:
        session.add(card_orm_obj)
        session.commit()


def insert_card_info_batched(engine: Engine, card_info_list: list[dict]):
    card_orm_obj_list = [CardLegality(**card_info) for card_info in card_info_list]
    with Session(engine) as session:
        session.add_all(card_orm_obj_list)
        session.commit()


def get_card_info_by_name(engine: Engine, name: str) -> CardLegality:
    legalities_not_found: dict = {
        "standard": "card_not_in_db",
        "future": "card_not_in_db",
        "historic": "card_not_in_db",
        "timeless": "card_not_in_db",
        "gladiator": "card_not_in_db",
        "pioneer": "card_not_in_db",
        "modern": "card_not_in_db",
        "legacy": "card_not_in_db",
        "pauper": "card_not_in_db",
        "vintage": "card_not_in_db",
        "penny": "card_not_in_db",
        "commander": "card_not_in_db",
        "oathbreaker": "card_not_in_db",
        "standardbrawl": "card_not_in_db",
        "brawl": "card_not_in_db",
        "alchemy": "card_not_in_db",
        "paupercommander": "card_not_in_db",
        "duel": "card_not_in_db",
        "oldschool": "card_not_in_db",
        "premodern": "card_not_in_db",
        "predh": "card_not_in_db",
    }
    with Session(engine) as session:
        card_orm_obj: CardLegality | None = session.query(CardLegality).filter_by(name=name).first()
        if card_orm_obj is None:
            card_orm_obj = CardLegality()
            card_orm_obj.name = name
            card_orm_obj.id = "-1"
            card_orm_obj.game_changer = False
            card_orm_obj.legalities = legalities_not_found
            print(f"[INFO] card identified by name: {name} not found in database; returning dummy object")
            return card_orm_obj
        return card_orm_obj


def read_from_json_file(file_path: str) -> list[dict]:
    import ijson

    list_of_cards: list[dict] = []
    with open(file_path) as json_file:
        for record in ijson.items(json_file, "item"):
            record_processed: dict = {
                "id": record["id"],
                "name": record["name"],
                "game_changer": record["game_changer"],
                "legalities": record["legalities"],
            }
            list_of_cards.append(record_processed)
    return list_of_cards


def fetch_bulk_data_url(scryfall_url: str) -> str:
    """
    :param scryfall_url: api endpoint to retrieve bulk data
    :return: download url for default_cards bulk data
    """
    import requests

    response = requests.get(scryfall_url)
    response.raise_for_status()
    data = response.json()["data"]
    for record in data:
        if record["type"] == "default_cards":
            return record["download_uri"]
    raise IndexError(f"[ERROR] download uri for default_cards bulk data could not be found in data: {data}")


def fetch_bulk_data(bulk_data_url: str, file_target_path: str, filename: str):
    # Make GET request to the API endpoint
    import requests

    response = requests.get(bulk_data_url)
    response.raise_for_status()
    print("[INFO] downloading of bulk data completed... saving to file")
    import json

    # Save JSON response to file
    target_file: str = os.path.join(file_target_path, filename)
    with open(target_file, "w") as f:
        json.dump(response.json(), f, indent=4)
    print(f"[INFO] saved bulk data to {target_file}")
