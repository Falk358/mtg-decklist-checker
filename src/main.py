from fastapi import FastAPI
from api.routes import card_legality

from list_checker.utils import get_config

app = FastAPI()
app.include_router(card_legality.router)


def main():
    config = get_config()


if __name__ == "__main__":
    main()
