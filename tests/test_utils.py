import pytest


def test_get_config():
    import os
    from list_checker.utils import get_config

    config = get_config()
    assert isinstance(config.get(section="Database", option="ScryfallJsonDataPath"), str)
