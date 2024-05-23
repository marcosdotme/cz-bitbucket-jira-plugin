import pytest

from cz_bitbucket_jira_plugin.exceptions import MinimumLengthException
from cz_bitbucket_jira_plugin.validators import MinimumLengthValidator


def test_answer_should_return_True():
    validator_return = MinimumLengthValidator(minimum_length=10).validate(
        answer='Dracula 2000'
    )

    assert validator_return is True


@pytest.mark.parametrize(
    'answer',
    [(''), ('Dracula')],
    ids=["''", "'Dracula'"],
)
def test_answer_should_raise_MinimumLengthException(answer):
    with pytest.raises(expected_exception=MinimumLengthException):
        MinimumLengthValidator(minimum_length=10).validate(answer=answer)
