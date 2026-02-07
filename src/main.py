from fastapi import FastAPI
from api.routes import card_legality
from configparser import ConfigParser

app = FastAPI()
app.include_router(card_legality.router)


def get_config() -> ConfigParser:
    config: ConfigParser = ConfigParser()
    config.read("src/config.ini")
    return config


def main():
    config = get_config()


if __name__ == "__main__":
    main()
