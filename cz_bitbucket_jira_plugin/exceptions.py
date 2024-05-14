from prompt_toolkit.validation import ValidationError


class RequiredAnswerException(ValidationError):
    def __init__(self):
        super().__init__(cursor_position=0, message='Answer is required.')


class ValueMustBeIntegerException(ValidationError):
    def __init__(self):
        super().__init__(cursor_position=0, message='Value must be integer.')


class AllValuesMustBeIntegerException(ValidationError):
    def __init__(self):
        super().__init__(cursor_position=0, message='All values must be integer.')
