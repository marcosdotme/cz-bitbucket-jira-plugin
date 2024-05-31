from commitizen.cz.exceptions import CzException
from prompt_toolkit.validation import ValidationError


class RequiredConfigException(CzException):
    # fmt: off
    def __init__(self, config_name: str):
        super().__init__(f"Config `{config_name}` is required.")
    # fmt: on


class IncorrectConfigException(CzException):
    # fmt: off
    def __init__(self, message: str):
        super().__init__(message)
    # fmt: on


class RequiredAnswerException(ValidationError):
    def __init__(self):
        super().__init__(cursor_position=0, message='Answer is required.')


class ValueMustBeIntegerException(ValidationError):
    def __init__(self):
        super().__init__(cursor_position=0, message='Value must be integer.')


class AllValuesMustBeIntegerException(ValidationError):
    def __init__(self):
        super().__init__(cursor_position=0, message='All values must be integer.')


class MinimumLengthException(ValidationError):
    # fmt: off
    def __init__(self, minimum_length: int):
        super().__init__(
            cursor_position=0,
            message=f"Minimum length for this field is {minimum_length}"
        )
    # fmt: on
