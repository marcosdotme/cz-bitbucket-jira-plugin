from setuptools import setup
from setuptools import find_packages


setup(
    name="CzBitbucketJiraPlugin",
    version="0.1.0",
    license="MIT",
    long_description="this is a long description",
    install_requires=["commitizen"],
    packages=["cz_bitbucket_jira_plugin"], #find_packages(),
    entry_points={
        "commitizen.plugin": [
            "cz_bitbucket_jira_plugin = cz_bitbucket_jira_plugin.main:CzBitbucketJiraPlugin"
        ]
    },
)
