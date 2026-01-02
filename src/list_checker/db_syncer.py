import os
import uuid

from sqlalchemy import Column, String, JSON, create_engine, Table, MetaData, Boolean, Uuid
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, Session


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, str]: JSON}


class CardLegality(Base):
    __tablename__ = "card_legalities"

    id: Mapped[uuid.UUID] = MappedColumn(primary_key=True)
    name: Mapped[str] = MappedColumn()
    game_changer: Mapped[bool] = MappedColumn()
    legalities: Mapped[dict[str, str]] = MappedColumn()


def init_db(file_path: str):
    if os.path.exists(file_path):
        raise FileExistsError(f"[ERROR] DB: {file_path} already exists; skipping init")
    engine = create_engine(f"sqlite:///{file_path}")
    CardLegality.metadata.create_all(engine)
    return engine


def insert_card_info_db(engine: Engine, card_info_obj: dict):
    card_orm_obj = CardLegality(**card_info_obj)
    with Session(engine) as session:
        session.add(card_orm_obj)
        session.commit()
