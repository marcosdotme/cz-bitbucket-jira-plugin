import tomli


def get_user_prompt_style():
    with open('./pyproject.toml', mode='rb') as file:
        data = tomli.load(file)

        try:
            style = data['tool']['commitizen']['prompt_style']
        except KeyError:
            style = None

        if style:
            return {'style': [tuple(attr.values()) for attr in style]}
