import pytest

from cz_bitbucket_jira_plugin.exceptions import AllValuesMustBeIntegerException
from cz_bitbucket_jira_plugin.validators import AllValuesMustBeIntegerValidator


@pytest.mark.parametrize(
    'answer',
    [
        (2000),
        ('2000'),
        ('2000,3000'),
        ('2000, 3000'),
        (''),
        (None),
    ],
    ids=[
        2000,
        "'2000'",
        "'2000,3000'",
        "'2000, 3000'",
        "''",
        None,
    ],
)
def test_answer_should_return_True(answer):
    """This validator checks if an value is an integer or can be coverted
    to it. But it not apply the 'required' rule, so, empty or None values
    also returns `True`."""
    validator_return = AllValuesMustBeIntegerValidator().validate(answer=answer)

    assert validator_return is True


def test_string_answer_should_raise_AllValuesMustBeIntegerException():
    with pytest.raises(AllValuesMustBeIntegerException):
        AllValuesMustBeIntegerValidator().validate(answer='Dracula 2000')
