from __future__ import annotations

import re
from typing import Callable
from typing import List


def required_answer_validator(answer):
    if not answer:
        return 'Answer is required.'

    return True


def must_be_integer_validator(answer):
    if not answer:
        return True

    try:
        int(answer)
    except ValueError:
        return 'Value must be integer.'

    return True


def all_values_must_be_integer_validator(answer):
    # Anything that is not a number, comma or whitespace character
    invalid_chars_pattern = re.compile("[^0-9,\s]+")
    invalid_chars = invalid_chars_pattern.findall(answer)

    if invalid_chars:
        return 'All values must be integer.'

    return True


def apply_multiple_validators(validators: List[Callable]):
    def apply_validators(answer):
        for validator in validators:
            result = validator(answer)

            if not result:
                return result

        return True

    return apply_validators
