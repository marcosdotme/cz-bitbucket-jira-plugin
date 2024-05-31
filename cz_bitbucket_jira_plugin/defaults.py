import re

from commitizen import defaults


JIRA_URL_EXAMPLE = 'https://<project name>.atlassian.net'
JIRA_URL_PATTERN = re.compile(r'(http|https)://.*?\.net')

DEFAULT_COMMIT_TYPES = [
    {'value': 'init', 'name': 'init: initial commit to set up your repository'},
    {'value': 'feat', 'name': 'feat: introduce a new feature'},
    {'value': 'fix', 'name': 'fix: fix a bug'},
    {'value': 'docs', 'name': 'docs: add or update documentation'},
    {'value': 'typo', 'name': 'typo: fix typos'},
    {'value': 'refactor', 'name': 'refactor: code refactoring'},
    {'value': 'perf', 'name': 'perf: code refactoring that improves performance'},
    {'value': 'delete', 'name': 'delete: code or file deletion'},
    {'value': 'test', 'name': 'test: add or update tests'},
    {
        'value': 'misc',
        'name': 'misc: changes that do not affect the code itself (e.g.: add .gitignore)',
    },
    {
        'value': 'style',
        'name': 'style: changes on code styling (e.g.: formatting, white-spaces)',
    },
]

DEFAULT_PROMPT_STYLE = {
    'style': [
        ('qmark', 'fg:#FF5555'),
        ('question', 'fg:#BD93F9'),
        ('answer', 'fg:#F8F8F2 nobold'),
        ('pointer', 'fg:#50FA7B nobold'),
        ('highlighted', 'fg:#50FA7B'),
        ('selected', 'fg:#50FA7B'),
        ('separator', 'fg:#858585'),
        ('instruction', 'fg:#858585 nobold'),
        ('text', 'fg:#F8F8F2'),
        ('disabled', 'fg:#858585 italic'),
    ]
}

MAJOR = 'MAJOR'
MINOR = 'MINOR'
PATCH = 'PATCH'

BUMP_MAP = {
    'feat': MINOR,
    'fix': PATCH,
    'perf': PATCH,
    'refactor': PATCH,
    'delete': MAJOR,
    'docs': PATCH,
    'typo': PATCH,
    'test': PATCH,
    'style': PATCH,
    'misc': PATCH,
}

BUMP_PATTERN = defaults.bump_pattern

CHANGELOG_PATTERN = defaults.bump_pattern

CHANGE_TYPE_MAP = {
    'feat': 'New features',
    'fix': 'Bug fixes',
    'perf': 'Performance improvements',
    'refactor': 'Code refactoring',
    'delete': 'Code or file deletions',
    'docs': 'Documentation updates',
    'typo': 'Typographical corrections',
    'test': 'Test additions or updates',
    'style': 'Code style and formatting',
    'misc': 'Miscellaneous',
}

CHANGE_TYPE_ORDER = [
    'BREAKING CHANGE',
    'New features',
    'Bug fixes',
    'Performance improvements',
    'Code refactoring',
    'Code or file deletions',
    'Documentation updates',
    'Typographical corrections',
    'Test additions or updates',
    'Code style and formatting',
    'Miscellaneous',
]
