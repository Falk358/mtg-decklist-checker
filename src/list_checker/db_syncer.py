import os
import sqlite3
from sqlalchemy import Column, Integer, String, JSON, create_engine, Table, MetaData, Boolean


def init_db(file_path: str):
    if os.path.exists(file_path):
        raise FileExistsError(f"[ERROR] DB: {file_path} already exists; skipping init")
    engine = create_engine(f"sqlite:///{file_path}")
    table_schema = Table(
        "card_legalities",
        MetaData(),
        Column("id", Integer, primary_key=True),
        Column("name", String(125), nullable=False),
        Column("game_changer", Boolean),
        Column("legalities", JSON),
    )
    with engine.connect() as conn:
        table_schema.create(conn)
        conn.commit()
    return engine
