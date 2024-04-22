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
        self.project_prefix = self.config.settings.get('jira_project_issue_prefix')
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

        questions = [
            {
                'type': 'input',
                'name': 'issue_prefix',
                'message': "What's the jira prefix?",
                'instruction': default_prefix,
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
                'name': 'issue_subtask',
                'message': 'Issue subtask number:\n',
                'instruction': multiple_items_instruction,
                'validate': all_values_must_be_integer_validator,
                'qmark': '\n '
            },
            {
                'type': 'input',
                'name': 'issue_related_task',
                'message': 'Issue related task number:\n',
                'instruction': multiple_items_instruction,
                'validate': all_values_must_be_integer_validator,
                'qmark': '\n '
            },
            {
                'type': 'input',
                'name': 'issue_title',
                'message': 'Issue title:\n ',
                'validate': required_answer_validator,
                'qmark': '\n*'
            },
            {
                'type': 'input',
                'multiline': True,
                'instruction': multiline_instruction,
                'name': 'issue_description',
                'message': 'Issue description:\n',
                'qmark': '\n '
            }
        ]
        return questions

    def message(self, answers: dict) -> str:
        issue_prefix = str(answers.get('issue_prefix') or self.project_prefix or '')

        if issue_prefix:
            issue_prefix += '-'

        issue_title = answers.get('issue_title')
        issue_number = answers.get('issue_number')
        issue_description = answers.get('issue_description')
        issue_epic_number = answers.get('issue_epic_number')
        issue_subtasks = answers.get('issue_subtask')
        issue_related_tasks = answers.get('issue_related_task')

        commit_message = f"{issue_title} [{issue_prefix}{issue_number}]"

        if issue_description:
            commit_message += f"\n\n{issue_description}"

        if issue_epic_number:
            commit_message += f"\n\nissue epic: [{issue_prefix}{issue_epic_number}]"

        if issue_subtasks:
            subtasks_list = [
                f"{issue_prefix}{subtask.strip()}"
                for subtask in issue_subtasks.split(',')
            ]
            commit_message += f"\nissue subtask: [{', '.join(subtasks_list)}]"

        if issue_related_tasks:
            related_tasks_list = [
                f"{issue_prefix}{related_task.strip()}"
                for related_task in issue_related_tasks.split(',')
            ]
            commit_message += f"\nissue related task: [{', '.join(related_tasks_list)}]"

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
