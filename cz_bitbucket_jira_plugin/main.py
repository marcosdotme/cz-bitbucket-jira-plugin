from collections import OrderedDict

from commitizen.config.base_config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions

from .constants import DEFAULT_COMMIT_TYPES
from .constants import DEFAULT_PROMPT_STYLE
from .functions import get_user_prompt_style
from .validators import all_values_must_be_integer_validator
from .validators import apply_multiple_validators
from .validators import must_be_integer_validator
from .validators import required_answer_validator


class CzBitbucketJiraPlugin(BaseCommitizen):
    def __init__(self, config: BaseConfig):
        self.config = config

        self.project_prefix = self.config.settings.get('jira_project_issue_prefix')
        self.user_commit_types = self.config.settings.get('commit_types')
        self.user_prompt_style = get_user_prompt_style()

        self.commit_types = self.user_commit_types or DEFAULT_COMMIT_TYPES
        self.config.update(self.user_prompt_style or DEFAULT_PROMPT_STYLE)

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
                'qmark': ' ' if self.project_prefix else '\n*'
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
        issue_subtasks = [task.strip() for task in issue_subtasks.split(',')]
        issue_subtasks = list(OrderedDict.fromkeys(issue_subtasks))

        issue_related_tasks = answers.get('issue_related_tasks')
        issue_related_tasks = [task.strip() for task in issue_related_tasks.split(',')]
        issue_related_tasks = list(OrderedDict.fromkeys(issue_related_tasks))

        commit_title = answers.get('commit_title')
        commit_title = commit_title[:1].lower() + commit_title[1:]
        commit_title = commit_title.strip().rstrip('.')

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
            subtasks_list = [f"{issue_prefix}{task.strip()}" for task in issue_subtasks]
            commit_message += f"\nissue subtasks: [{', '.join(subtasks_list)}]"

        if issue_related_tasks:
            related_tasks_list = [f"{issue_prefix}{task.strip()}" for task in issue_related_tasks]
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
