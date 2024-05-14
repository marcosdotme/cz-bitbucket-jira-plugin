import pytest

from cz_bitbucket_jira_plugin.exceptions import RequiredAnswerException
from cz_bitbucket_jira_plugin.validators import RequiredAnswerValidator


def test_non_empty_answer_should_return_True():
    validator_return = RequiredAnswerValidator().validate(answer='Im an answer!')

    assert validator_return is True


@pytest.mark.parametrize(
    'answer',
    [
        (''),
        (None),
    ],
    ids=["''", None],
)
def test_answer_should_raise_RequiredAnswerException(answer):
    with pytest.raises(expected_exception=RequiredAnswerException):
        RequiredAnswerValidator().validate(answer=answer)
