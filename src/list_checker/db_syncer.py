import os
import sqlite3
import sqlalchemy


def init_db(file_path: str):
    engine = sqlalchemy.create_engine(f"sqlite:///{file_path}")
    return engine
