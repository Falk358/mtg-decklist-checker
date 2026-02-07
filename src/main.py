from fastapi import FastAPI
from api.routes import card_legality

app = FastAPI()
app.include_router(card_legality.router)


def main():
    pass
