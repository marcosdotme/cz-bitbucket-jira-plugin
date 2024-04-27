from commitizen.config.base_config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions

from .validators import all_values_must_be_integer_validator
from .validators import apply_multiple_validators
from .validators import must_be_integer_validator
from .validators import required_answer_validator


class CzBitbucketJiraPlugin(BaseCommitizen):
    def __init__(self, config: BaseConfig):
        self.config = config
        self.config.update(
            {
                'style': [
                    ('qmark', 'fg:#ff5555'),
                    ('question', 'fg:#bd93f9'),
                    ('answer', 'fg:#f8f8f2 nobold'),
                    ('pointer', 'fg:#ff9d00'),
                    ('highlighted', 'fg:#ff9d00'),
                    ('selected', 'fg:#cc5454'),
                    ('separator', 'fg:#cc5454'),
                    ('instruction', 'fg:#858585 nobold'),
                    ('text', 'fg:#ffffff'),
                    ('disabled', 'fg:#858585 italic'),
                ]
            }
        )
        self.project_prefix = self.config.settings.get('jira_project_issue_prefix')
        self.commit_types = [
            {'value': 'init', 'name': 'init: initial commit to set up your repository'},
            {'value': 'feat', 'name': 'feat: introduce a new feature'},
            {'value': 'fix', 'name': 'fix: fix a bug'},
            {'value': 'docs', 'name': 'docs: add or update documentation'},
            {'value': 'typo', 'name': 'typo: fix typos'},
            {'value': 'refactor', 'name': 'refactor: code refactoring'},
            {'value': 'perf', 'name': 'perf: code refactoring that improves performance'},
            {'value': 'delete', 'name': 'delete: code or file deletion'},
            {'value': 'test', 'name': 'test: add or update tests'},
            {'value': 'misc', 'name': 'misc: changes that do not affect the code itself (e.g.: add .gitignore)'},
            {'value': 'style', 'name': 'style: changes on code styling (e.g.: formatting, white-spaces)'}
        ]

        super().__init__(self.config)

    def questions(self) -> Questions:
        if self.project_prefix:
            default_prefix = f"(default: {self.project_prefix})\n "
        else:
            default_prefix = '\n '

        multiple_items_instruction = (
            f"if more than one, use comma to separate them."
            f" (press [enter] to skip)\n "
        )
        multiline_instruction = (
            '(press [enter] to insert a new line OR [alt + enter] to finish)\n>'
        )
        select_instruction = '(use arrow keys to select and press [enter])\n'

        questions = [
            {
                'type': 'input',
                'name': 'issue_prefix',
                'message': "What's the jira prefix?",
                'instruction': default_prefix,
                'validate': required_answer_validator if not self.project_prefix else None,
                'qmark': ' '
            },
            {
                'type': 'input',
                'name': 'issue_epic_number',
                'message': 'Issue epic number:\n ',
                'validate': must_be_integer_validator,
                'qmark': '\n '
            },
            {
                'type': 'input',
                'name': 'issue_number',
                'message': 'Issue number:\n ',
                'validate': apply_multiple_validators(
                    validators=[
                        required_answer_validator,
                        must_be_integer_validator
                    ]
                ),
                'qmark': '\n*'
            },
            {
                'type': 'input',
                'name': 'issue_subtasks',
                'message': 'Issue subtask number:\n',
                'instruction': multiple_items_instruction,
                'validate': all_values_must_be_integer_validator,
                'qmark': '\n '
            },
            {
                'type': 'input',
                'name': 'issue_related_tasks',
                'message': 'Issue related task number:\n',
                'instruction': multiple_items_instruction,
                'validate': all_values_must_be_integer_validator,
                'qmark': '\n '
            },
            {
                'type': 'select',
                'name': 'commit_type',
                'message': 'Select the commit type:\n ',
                'choices': self.commit_types,
                'pointer': '>',
                'instruction': select_instruction,
                'qmark': '\n*'
            },
            {
                'type': 'input',
                'name': 'commit_title',
                'message': 'Commit title:\n ',
                'validate': required_answer_validator,
                'qmark': '\n*'
            },
            {
                'type': 'input',
                'multiline': True,
                'instruction': multiline_instruction,
                'name': 'commit_description',
                'message': 'Commit description:\n',
                'qmark': '\n '
            }
        ]
        return questions

    def message(self, answers: dict) -> str:
        issue_prefix = str(answers.get('issue_prefix') or self.project_prefix or '')

        if issue_prefix:
            issue_prefix += '-'

        issue_number = answers.get('issue_number')
        issue_epic_number = answers.get('issue_epic_number')
        issue_subtasks = answers.get('issue_subtasks')
        issue_related_tasks = answers.get('issue_related_tasks')

        commit_title = answers.get('commit_title')
        commit_title = commit_title[:1].lower() + commit_title[1:]

        commit_description = answers.get('commit_description')
        commit_type = answers.get('commit_type')

        commit_message = (
            f"{commit_type}: {commit_title} [{issue_prefix}{issue_number}]" if commit_type
            else f"{commit_title} [{issue_prefix}{issue_number}]"
        )

        if commit_description:
            commit_message += f"\n\n{commit_description}"

        if issue_epic_number:
            commit_message += f"\n\nissue epic: [{issue_prefix}{issue_epic_number}]"

        if issue_subtasks:
            subtasks_list = [
                f"{issue_prefix}{subtask.strip()}"
                for subtask in issue_subtasks.split(',')
            ]
            commit_message += f"\nissue subtasks: [{', '.join(subtasks_list)}]"

        if issue_related_tasks:
            related_tasks_list = [
                f"{issue_prefix}{related_task.strip()}"
                for related_task in issue_related_tasks.split(',')
            ]
            commit_message += f"\nissue related tasks: [{', '.join(related_tasks_list)}]"

        return commit_message

    def example(self) -> str:
        """Provide an example to help understand the style (OPTIONAL)

        Used by `cz example`.
        """
        return 'Problem with user (#321)'

    def schema(self) -> str:
        """Show the schema used (OPTIONAL)

        Used by `cz schema`.
        """
        return '<title> (<issue>)'

    def info(self) -> str:
        """Explanation of the commit rules. (OPTIONAL)

        Used by `cz info`.
        """
        return 'We use this because is useful'
