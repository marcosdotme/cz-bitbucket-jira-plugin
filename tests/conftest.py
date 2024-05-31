import os

import pytest
from commitizen.config import BaseConfig
from commitizen.config import TomlConfig

from cz_bitbucket_jira_plugin.defaults import JIRA_URL_EXAMPLE


@pytest.fixture()
def default_config():
    config = BaseConfig()
    config.update({'jira_url': JIRA_URL_EXAMPLE})

    return config


@pytest.fixture
def setup_tmpdir(tmpdir):
    with tmpdir.as_cwd():
        path = tmpdir.mkdir('commitizen')
        file_path = path.join('cz.toml')
        toml_config = TomlConfig(data='', path=file_path)
        toml_config.init_empty_config_content()

        os.chdir(path)

        yield path
