import os

import pytest
from commitizen.config import BaseConfig
from commitizen.config import TomlConfig


@pytest.fixture()
def default_config():
    return BaseConfig()


@pytest.fixture
def setup_tmpdir(tmpdir):
    with tmpdir.as_cwd():
        path = tmpdir.mkdir('commitizen')
        file_path = path.join('cz.toml')
        toml_config = TomlConfig(data='', path=file_path)
        toml_config.init_empty_config_content()

        os.chdir(path)

        yield path
