from __future__ import annotations

import inspect
import re
from typing import Callable
from typing import List

from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator

from .exceptions import AllValuesMustBeIntegerException
from .exceptions import MinimumLengthException
from .exceptions import RequiredAnswerException
from .exceptions import ValueMustBeIntegerException


def apply_multiple_validators(validators: List[Callable]):
    def apply_validators(answer):
        for validator in validators:
            if inspect.isclass(validator):
                result = validator.validate(answer)
            else:
                result = validator(answer)

            if result != True:  # noqa: E712
                return result

        return True

    return apply_validators


class RequiredAnswerValidator(Validator):
    @classmethod
    def validate(cls, answer):
        if isinstance(answer, Document):
            answer = answer.text

        if not answer:
            raise RequiredAnswerException

        return True


class ValueMustBeIntegerValidator(Validator):
    @classmethod
    def validate(cls, answer):
        if isinstance(answer, Document):
            answer = answer.text

        if answer in ['', None]:
            return True

        try:
            int(answer)
        except ValueError:
            raise ValueMustBeIntegerException

        return True


class AllValuesMustBeIntegerValidator(Validator):
    @classmethod
    def validate(cls, answer):
        if isinstance(answer, Document):
            answer = answer.text

        if answer in ['', None]:
            return True

        # Anything that is not a number, comma or whitespace character
        pattern = re.compile(r'[^0-9,\s]+')
        invalid_chars = pattern.findall(str(answer))

        if invalid_chars:
            raise AllValuesMustBeIntegerException

        return True


class MinimumLengthValidator(Validator):
    def __init__(self, minimum_length: int) -> None:
        self.minimum_length = minimum_length

    def validate(self, answer):
        if isinstance(answer, Document):
            answer = answer.text

        if len(answer) < self.minimum_length:
            raise MinimumLengthException(minimum_length=self.minimum_length)

        return True
