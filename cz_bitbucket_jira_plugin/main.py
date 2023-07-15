from commitizen.config.base_config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions
from .validators import required_answer_validator


class CzBitbucketJiraPlugin(BaseCommitizen):
    def __init__(self, config: BaseConfig):
        self.config = config
        self.cfg_project_prefix = self.config.settings.get('jira_project_issue_prefix')
        self.config.update(
            {
                "style": [
                    ("qmark", "fg:#ff5555"),
                    ("question", "fg:#bd93f9"),
                    ("answer", "fg:#f8f8f2 nobold"),
                    ("pointer", "fg:#ff9d00"),
                    ("highlighted", "fg:#ff9d00"),
                    ("selected", "fg:#cc5454"),
                    ("separator", "fg:#cc5454"),
                    ("instruction", "fg:#858585 nobold"),
                    ("text", "fg:#ffffff"),
                    ("disabled", "fg:#858585 italic"),
                ]
            }
        )

        super().__init__(self.config)


    def questions(self) -> Questions:
        if self.cfg_project_prefix:
            instruction_issue_prefix = f"[{self.cfg_project_prefix}]:"
        else:
            instruction_issue_prefix = '\n '

        instruction_multiple_items = "(if more than one use comma ',' to separate them) [press enter to skip]\n "
        instruction_multiline = '(Aperte [enter] para inserir uma nova linha ou [alt + enter] para terminar)\n>'

        questions = [
            {
                "type": "input",
                "name": "issue_prefix",
                "message": f"What's the jira prefix?",
                "instruction": instruction_issue_prefix,
                "qmark": " "
            },
            {
                "type": "input",
                "name": "issue_epic_number",
                "message": "Issue epic number:\n ",
                "qmark": "\n "
            },
            {
                "type": "input",
                "name": "issue_number",
                "message": "Issue number:\n ",
                "validate": required_answer_validator(answer_title='Issue number'),
                "qmark": "\n*"
            },
            {
                "type": "input",
                "name": "issue_subtask",
                "message": "Issue subtask number:\n",
                "instruction": instruction_multiple_items,
                "qmark": "\n "
            },
            {
                "type": "input",
                "name": "issue_related_task",
                "message": "Issue related task number:\n",
                "instruction": instruction_multiple_items,
                "qmark": "\n "
            },
            {
                "type": "input",
                "name": "issue_title",
                "message": "Issue title:\n ",
                "validate": required_answer_validator(answer_title='Issue title'),
                "qmark": "\n*"
            },
            {
                "type": "input",
                "multiline": True,
                "instruction": instruction_multiline,
                "name": "issue_description",
                "message": "Issue description:\n",
                "qmark": "\n "
            }
        ]
        return questions


    def message(self, answers: dict) -> str:
        issue_prefix = str(answers.get('issue_prefix') or self.cfg_project_prefix or '')
        if issue_prefix:
            issue_prefix += '-'

        issue_title = answers.get('issue_title')
        issue_number = answers.get('issue_number')
        issue_description = answers.get('issue_description')
        issue_epic_number = answers.get('issue_epic_number')
        issue_subtask = answers.get('issue_subtask')
        issue_related_task = answers.get('issue_related_task')

        message = f"{issue_title} [#{issue_prefix}{issue_number}]"

        if issue_description:
            message += f"\n\n{issue_description}"

        if issue_epic_number:
            message += f"\n\nissue epic: [#{issue_prefix}{issue_epic_number}]"
        
        if issue_subtask:
            message += f"\nissue subtask: [#{issue_prefix}{issue_subtask}]"
        
        if issue_related_task:
            message += f"\nissue related task: [#{issue_prefix}{issue_related_task}]"

        return message


    def example(self) -> str:
        """Provide an example to help understand the style (OPTIONAL)

        Used by `cz example`.
        """
        return "Problem with user (#321)"


    def schema(self) -> str:
        """Show the schema used (OPTIONAL)

        Used by `cz schema`.
        """
        return "<title> (<issue>)"


    def info(self) -> str:
        """Explanation of the commit rules. (OPTIONAL)

        Used by `cz info`.
        """
        return "We use this because is useful"
