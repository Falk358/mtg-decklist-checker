from list_checker.utils import get_config
from sqlalchemy import Engine, create_engine

from list_checker.db_syncer import init_db


from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter(
    prefix="/cardlegality",
)


class CardName(BaseModel):
    card_name: str


def open_db():

    config = get_config()
    db_file_path: str = config.get("Database", "SqliteDbFilePath")
    try:
        db = init_db(db_file_path)
    except FileExistsError:
        print(f"database file {db_file_path} already exists; opening Engine on existing file instead")
        db: Engine = create_engine("sqlite:///" + db_file_path)

    return db


@router.post("/")
def card_name(card_name: CardName) -> dict[str, str]:
    """
    :param card_name: name of the card for which to retrieve card legality info (which format legal)
    :return: dict with structure [format, legality_for_format]
    """
    return {"pauper": "legal"}
