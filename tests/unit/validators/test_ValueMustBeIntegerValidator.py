import pytest

from cz_bitbucket_jira_plugin.exceptions import ValueMustBeIntegerException
from cz_bitbucket_jira_plugin.validators import ValueMustBeIntegerValidator


@pytest.mark.parametrize(
    'answer',
    [
        (2000),
        ('2000'),
        (''),
        (None),
    ],
    ids=[
        2000,
        "'2000'",
        "''",
        None,
    ],
)
def test_answer_should_return_True(answer):
    """This validator checks if an value is an integer or can be coverted
    to it. But it not apply the 'required' rule, so, empty or None values
    also returns `True`."""
    validator_return = ValueMustBeIntegerValidator().validate(answer=answer)

    assert validator_return is True


def test_string_answer_should_raise_ValueMustBeIntegerException():
    with pytest.raises(ValueMustBeIntegerException):
        ValueMustBeIntegerValidator().validate(answer='Dracula 2000')
