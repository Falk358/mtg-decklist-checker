from sqlalchemy import Engine

from list_checker.db_syncer import get_card_info_by_name
from list_checker.db_syncer import CardLegality


def fetch_legalities(card_name: str, engine: Engine) -> dict:
    card_legality: CardLegality = get_card_info_by_name(engine, card_name)
    return card_legality.legalities
