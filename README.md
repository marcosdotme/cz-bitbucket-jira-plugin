# cz-bitbucket-jira-plugin

> A [Commitizen](https://github.com/commitizen-tools/commitizen) plugin that links your Bitbucket commits with your Jira issues.

![GIF](https://vhs.charm.sh/vhs-duzp35l3XRQoHAoMLX6wA.gif)

## Installation
```shell
pip install cz-bitbucket-jira-plugin
```

## Configuration

Theres 2 possible configuration files: `pyproject.toml` and `cz.toml`. It's up to you.

> [!TIP]
> If you already have a `pyproject.toml` in your project, use it. If not, create a `cz.toml`.

The only **required** configurations are:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
jira_url = "https://<project name>.atlassian.net"
```

This tells Commitizen which plugin you want to use and what is your Jira url, to properly link issues on commit messages and Changelog.

### Jira project key (_optional_)

To avoid the need to type your **Jira project key** for every commit, you can set this up in your chosen configuration file:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
jira_project_key = "DEV"
```

Now every time you execute `cz commit`, Commitizen will use the **cz-bitbucket-jira-plugin** and use "DEV" as your default **Jira project key**.

### Minimum length for commit messages (_optional_)

You can set a minimum length for commit messages to prevent things like `"fix"`, `"wip"`, `"test"`, `"aaa"`, and so on...

To do this, set this up in your chosen configuration file:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
commit_message_minimum_length = 32
```

The default value for this config is `32`.

## Usage
As it is a [Commitizen](https://github.com/commitizen-tools/commitizen) plugin, you can:

```shell
cz
```

## Customization
You can change some defaults of the plugin:

### Prompt style
To change the default **prompt style** which is:

```toml
prompt_style = [
    { identifier = "qmark", style = "fg:#FF5555" },
    { identifier = "question", style = "fg:#BD93F9" },
    { identifier = "answer", style = "fg:#F8F8F2 nobold" },
    { identifier = "pointer", style = "fg:#50FA7B nobold" },
    { identifier = "highlighted", style = "fg:#50FA7B" },
    { identifier = "selected", style = "fg:#50FA7B" },
    { identifier = "separator", style = "fg:#858585" },
    { identifier = "instruction", style = "fg:#858585 nobold" },
    { identifier = "text", style = "fg:#F8F8F2" },
    { identifier = "disabled", style = "fg:#858585 italic" },
]
```

You can create the `prompt_style` key in your config file. This key must be an [*array of inline tables*](https://toml.io/en/v1.0.0#inline-table). Each inline table must have two pair of key/value.

Example:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
prompt_style = [
    { identifier = "question", style = "fg:#50FA7B bold" },
    { identifier = "answer", style = "fg:#F8F8F2 nobold" }
]
```

The available identifiers are:

- qmark
- question
- answer
- pointer
- highlighted
- selected
- separator
- instruction
- text
- disabled

> You can check this also on https://questionary.readthedocs.io/en/stable/pages/advanced.html#themes-styling

For the complete styling documentation check https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/styling.html

### Commit types
To change the default **commit types** which is:

```toml
commit_types = [
    { value = "init", name = "init: initial commit to set up your repository" },
    { value = "feat", name = "feat: introduce a new feature" },
    { value = "fix", name = "fix: fix a bug" },
    { value = "docs", name = "docs: add or update documentation" },
    { value = "typo", name = "typo: fix typos" },
    { value = "refactor", name = "refactor: code refactoring" },
    { value = "perf", name = "perf: code refactoring that improves performance" },
    { value = "delete", name = "delete: code or file deletion" },
    { value = "test", name = "test: add or update tests" },
    { value = "misc", name = "misc: changes that do not affect the code itself (e.g.: add .gitignore)" },
    { value = "style", name = "style: changes on code styling (e.g.: formatting, white-spaces)" }
]
```

You can create the `commit_types` key in your config file. This key must be an [*array of inline tables*](https://toml.io/en/v1.0.0#inline-table). Each inline table must have two pair of key/value, and the key names must be: **value** and **name**. Must be these names (at least for now).

Example:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
commit_types = [
    { value = "feat", name = "feat: introduce a new feature" },
    { value = "fix", name = "fix: fix a bug" },
    { value = "refactor", name = "refactor: code refactoring" }
]
```

> [!IMPORTANT]
> If you change the default commit types you will also need to declare two other keys: `change_type_map` and `change_type_order`.

#### Change type map

[*Array of inline tables*](https://toml.io/en/v1.0.0#inline-table) that have an key map for each commit type. Using the commit types on the example above:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
change_type_map = [
    { value = "feat", name = "New features" },
    { value = "fix", name = "Bug fixes" },
    { value = "refactor", name = "Code refactoring" }
]
```

The `value` are the commit type and `name` are the long name that will appear in the Changelog.


#### Change type order

[*Array*](https://toml.io/en/v1.0.0#array) containing the order you want to show in the Changelog.

If you think that bug fixes are more important than new features you can show them first on Changelog:

```toml
[tool.commitizen]
name = "cz-bitbucket-jira-plugin"
change_type_order = [
    "Bug fixes",
    "New features",
    "Code refactoring"
]
```
