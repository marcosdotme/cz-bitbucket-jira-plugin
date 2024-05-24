import itertools

import pytest

from cz_bitbucket_jira_plugin.main import CzBitbucketJiraPlugin
from tests.constants import ANSWER_AND_EXPECTED_OUTPUT


@pytest.mark.parametrize(
    ('answers', 'expected_output'),
    [
        pytest.param(test_case.get('params'), test_case.get('expected_output'))
        for test_case in ANSWER_AND_EXPECTED_OUTPUT
    ],
    ids=itertools.count(start=1),
)
def test_commit_output(setup_tmpdir, default_config, answers, expected_output):
    cz = CzBitbucketJiraPlugin(config=default_config)
    output = cz.message(answers=answers)

    assert output == expected_output
