from __future__ import annotations

from pathlib import Path

import tomli


def config_file_is_valid(config_file: str | Path) -> bool:
    with open(config_file, mode='rb') as file:
        data = tomli.load(file)

        try:
            data['tool']['commitizen']
            return True
        except KeyError:
            return False


def get_config_file() -> Path:
    config_files = [Path('pyproject.toml'), Path('.cz.toml')]

    for config_file in config_files:
        if config_file_is_valid(config_file=config_file):
            return config_file
    
    raise AttributeError('Missing [tool.commitizen] table on your config file.')


def get_user_prompt_style():
    config_file = get_config_file()

    with open(config_file, mode='rb') as file:
        data = tomli.load(file)

        try:
            style = data['tool']['commitizen']['prompt_style']
        except KeyError:
            style = None

        if style:
            return {'style': [tuple(attr.values()) for attr in style]}
