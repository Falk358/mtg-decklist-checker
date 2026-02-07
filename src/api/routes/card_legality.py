from list_checker.db_syncer import CardLegality
from list_checker.db_syncer import init_db

from list_checker.legality_checker import get_card_info_by_name

from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter(
    prefix="/cardlegality",
)


class CardName(BaseModel):
    card_name: str


def init_and_load_db():
    """WIP: from main import get_config

    config = get_config()
    db_file_path: str = config.get("Database", "SqliteDbFilePath")
    db = init_db(db_file_path)
    """
    pass


@router.post("/")
def card_name(card_name: CardName) -> dict[str, str]:
    """
    :param card_name: name of the card for which to retrieve card legality info (which format legal)
    :return: dict with structure [format, legality_for_format]
    """
    return {"pauper": "legal"}
