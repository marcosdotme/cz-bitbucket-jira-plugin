import pytest
from commitizen.config import BaseConfig


@pytest.fixture()
def default_config():
    return BaseConfig()
