import re
from collections import OrderedDict

from commitizen import git
from commitizen.config.base_config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions

from .defaults import BUMP_MAP
from .defaults import BUMP_PATTERN
from .defaults import CHANGE_TYPE_MAP
from .defaults import CHANGE_TYPE_ORDER
from .defaults import CHANGELOG_PATTERN
from .defaults import DEFAULT_COMMIT_TYPES
from .defaults import DEFAULT_PROMPT_STYLE
from .defaults import JIRA_URL_EXAMPLE
from .defaults import JIRA_URL_PATTERN
from .exceptions import IncorrectConfigException
from .exceptions import RequiredConfigException
from .functions import get_user_prompt_style
from .validators import AllValuesMustBeIntegerValidator
from .validators import apply_multiple_validators
from .validators import MinimumLengthValidator
from .validators import RequiredAnswerValidator
from .validators import ValueMustBeIntegerValidator


class CzBitbucketJiraPlugin(BaseCommitizen):
    def __init__(self, config: BaseConfig):
        self.config = config

        self.user_jira_url = self.config.settings.get('jira_url')

        if not self.user_jira_url:
            raise RequiredConfigException(config_name='jira_url')

        try:
            self.jira_base_url = re.search(
                pattern=JIRA_URL_PATTERN, string=self.user_jira_url
            ).group()
        except AttributeError:
            # fmt: off
            raise IncorrectConfigException(
                f"Config `jira_url` seems wrong. It must be like: '{JIRA_URL_EXAMPLE}'"
            )
            # fmt: on

        self.user_jira_project_key = self.config.settings.get('jira_project_key')
        self.user_commit_types = self.config.settings.get('commit_types')
        self.user_prompt_style = get_user_prompt_style()
        self.user_minimum_length = self.config.settings.get(
            'commit_message_minimum_length'
        )
        self.user_change_type_map = self.config.settings.get('change_type_map')
        self.user_change_type_order = self.config.settings.get('change_type_order')

        self.bump_pattern = BUMP_PATTERN
        self.bump_map = BUMP_MAP

        self.changelog_pattern = CHANGELOG_PATTERN
        self.change_type_map = self.user_change_type_map or CHANGE_TYPE_MAP
        self.change_type_order = self.user_change_type_order or CHANGE_TYPE_ORDER

        self.commit_types = self.user_commit_types or DEFAULT_COMMIT_TYPES
        piped_commit_types = '|'.join(
            [d.get('value') for d in self.commit_types] + ['BREAKING CHANGE']
        )
        # fmt: off
        self.commit_parser = (
            fr"^((?P<change_type>{piped_commit_types})"
            r'(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?|\w+!):\s(?P<message>.*)?'
        )
        # fmt: on

        self.minimum_length = self.user_minimum_length or 32

        self.config.update(self.user_prompt_style or DEFAULT_PROMPT_STYLE)

        super().__init__(self.config)

    def questions(self) -> Questions:
        if self.user_jira_project_key:
            default_jira_project_key = f"(default: {self.user_jira_project_key})\n "  # fmt: skip
        else:
            default_jira_project_key = '\n '

        multiple_items_instruction = (
            'if more than one, use comma to separate them. (press [enter] to skip)\n '
        )
        multiline_instruction = (
            '(press [enter] to insert a new line OR [alt + enter] to finish)\n>'
        )
        select_instruction = '(use arrow keys to select and press [enter])\n'
        optional_instruction = '(press [enter] to skip)\n '
        confirm_instruction = '(y/n)\n  '

        questions = [
            {
                'type': 'input',
                'name': 'jira_project_key',
                'message': "What's the Jira project key?",
                'instruction': default_jira_project_key,
                'validate': (
                    RequiredAnswerValidator if not self.user_jira_project_key else None
                ),
                'qmark': ' ' if self.user_jira_project_key else '\n*',
            },
            {
                'type': 'input',
                'name': 'issue_epic_number',
                'message': 'Issue epic number:\n ',
                'validate': ValueMustBeIntegerValidator,
                'qmark': '\n ',
            },
            {
                'type': 'input',
                'name': 'issue_number',
                'message': 'Issue number:\n ',
                'validate': apply_multiple_validators(
                    validators=[
                        RequiredAnswerValidator,
                        ValueMustBeIntegerValidator,
                    ]
                ),
                'qmark': '\n*',
            },
            {
                'type': 'input',
                'name': 'issue_subtasks',
                'message': 'Issue subtask number:\n',
                'instruction': multiple_items_instruction,
                'validate': AllValuesMustBeIntegerValidator,
                'qmark': '\n ',
            },
            {
                'type': 'input',
                'name': 'issue_related_tasks',
                'message': 'Issue related task number:\n',
                'instruction': multiple_items_instruction,
                'validate': AllValuesMustBeIntegerValidator,
                'qmark': '\n ',
            },
            {
                'type': 'select',
                'name': 'commit_type',
                'message': 'Select the type of change you are committing:\n ',
                'choices': self.commit_types,
                'pointer': '>',
                'instruction': select_instruction,
                'validator': RequiredAnswerValidator,
                'qmark': '\n*',
            },
            {
                'type': 'input',
                'name': 'commit_scope',
                'message': "What's the scope of this change?",
                'instruction': optional_instruction,
                'qmark': '\n ',
            },
            {
                'type': 'input',
                'name': 'commit_title',
                'message': 'Commit title:\n ',
                'validate': MinimumLengthValidator(minimum_length=self.minimum_length),
                'qmark': '\n*',
            },
            {
                'type': 'input',
                'multiline': True,
                'instruction': multiline_instruction,
                'name': 'commit_description',
                'message': 'Commit description:\n',
                'qmark': '\n ',
            },
            {
                'type': 'confirm',
                'name': 'is_breaking_change',
                'message': 'Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer?',
                'default': False,
                'instruction': confirm_instruction,
                'auto_enter': False,
                'qmark': '\n*',
            },
            {
                'type': 'input',
                'multiline': True,
                'instruction': f'\n  {multiline_instruction}',
                'name': 'footer',
                'message': (
                    'Footer. Information about Breaking Changes, '
                    'Bitbucket Smart Commits syntax or whatever you want.'
                ),
                'qmark': '\n ',
            },
        ]
        return questions

    def message(self, answers: dict) -> str:
        jira_project_key = str(
            answers.get('jira_project_key') or self.user_jira_project_key or ''
        )

        if jira_project_key:
            jira_project_key += '-'

        issue_epic_number = answers.get('issue_epic_number')
        issue_number = answers.get('issue_number')
        issue_subtasks = answers.get('issue_subtasks')
        issue_related_tasks = answers.get('issue_related_tasks')

        commit_type = answers.get('commit_type')
        commit_scope = answers.get('commit_scope', '').strip()

        commit_title = answers.get('commit_title')
        commit_title = commit_title[:1].lower() + commit_title[1:]
        commit_title = commit_title.strip().rstrip('.')

        commit_description = answers.get('commit_description')
        is_breaking_change = answers.get('is_breaking_change')
        footer = answers.get('footer')

        breaking_change_sign = '!' if is_breaking_change else ''
        breaking_change_text = 'BREAKING CHANGE' if is_breaking_change else ''

        # fmt: off
        if commit_scope:
            commit_message = (
                f"{commit_type}({commit_scope}){breaking_change_sign}: "
                f"{commit_title} [{jira_project_key}{issue_number}]"
            )
        else:
            commit_message = (
                f"{commit_type}{breaking_change_sign}: "
                f"{commit_title} [{jira_project_key}{issue_number}]"
            )
        # fmt: on

        if commit_description:
            if is_breaking_change:
                commit_message += f"\n\n{breaking_change_text}: {commit_description}"  # fmt: skip
            else:
                commit_message += f"\n\n{commit_description}"  # fmt: skip
        else:
            commit_message += f"\n\n{breaking_change_text}"  # fmt: skip

        if issue_epic_number:
            commit_message += f"\n\nissue epic: [{jira_project_key}{issue_epic_number}]"  # fmt: skip

        if issue_subtasks:
            issue_subtasks = [task.strip() for task in issue_subtasks.split(',')]
            issue_subtasks = list(OrderedDict.fromkeys(issue_subtasks))
            subtasks_list = [f"{jira_project_key}{task.strip()}" for task in issue_subtasks]  # fmt: skip

            if issue_epic_number:
                commit_message += f"\nissue subtasks: [{', '.join(subtasks_list)}]"  # fmt: skip
            else:
                commit_message += f"\n\nissue subtasks: [{', '.join(subtasks_list)}]"  # fmt: skip

        if issue_related_tasks:
            issue_related_tasks = [
                task.strip() for task in issue_related_tasks.split(',')
            ]
            issue_related_tasks = list(OrderedDict.fromkeys(issue_related_tasks))
            related_tasks_list = [f"{jira_project_key}{task.strip()}" for task in issue_related_tasks]  # fmt: skip

            if issue_epic_number or issue_subtasks:
                commit_message += f"\nissue related tasks: [{', '.join(related_tasks_list)}]"  # fmt: skip
            else:
                commit_message += f"\n\nissue related tasks: [{', '.join(related_tasks_list)}]"  # fmt: skip

        if footer:
            commit_message += f"\n\n{footer}"  # fmt: skip

        return commit_message.rstrip()

    def example(self) -> str:
        """Provide an example to help understand the style (OPTIONAL)

        Used by `cz example`.
        """
        return (
            'feat: create `apply_multiple_validators` function [CZ-1032]\n'
            '\n'
            'Allow us to apply multiple validators to a single question\n'
            '\n'
            'issue epic: [CZ-959]\n'
            'issue subtasks: [CZ-1033, CZ-1034]\n'
            'issue related tasks: [CZ-1005]\n'
            '\n'
            'CZ-1032 #done'
        )

    def schema(self) -> str:
        """Show the schema used (OPTIONAL)

        Used by `cz schema`.
        """
        return (
            '<commit_type>: <commit_title> [<jira_project_key>-<jira_issue_number>]\n'
            '<BLANK LINE>\n'
            '<commit_description>\n'
            '<BLANK LINE>\n'
            'issue epic: [<jira_project_key>-<jira_issue_epic_number>]\n'
            'issue subtasks: [<jira_project_key>-<jira_issue_subtasks_number>]\n'
            'issue related tasks: [<jira_project_key>-<jira_issue_related_tasks_number>]\n'
            '<BLANK LINE>\n'
            '<footer>'
        )

    def info(self) -> str:
        """Explanation of the commit rules. (OPTIONAL)

        Used by `cz info`.
        """
        return 'We use this because is useful'

    def changelog_message_builder_hook(self, parsed_message: dict, commit: git.GitCommit):
        if parsed_message.get('change_type') == 'BREAKING CHANGE':
            return False

        if parsed_message.get('breaking'):
            parsed_message['change_type'] = 'BREAKING CHANGE'

        issue_id_pattern = re.compile(r'\[([^\[\]]*)\](?!.*\[)')

        commit_hash = commit.rev[:7]
        message = parsed_message.get('message')
        message_without_issue_id = issue_id_pattern.sub('', message).strip()

        issue_id = issue_id_pattern.search(message).group(1)

        # fmt: off
        parsed_message['message'] = (
            f"{message_without_issue_id} "
            f"[{issue_id}]({self.jira_base_url}/browse/{issue_id}) ({commit_hash})"
        )
        # fmt: on

        return parsed_message
