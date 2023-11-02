from __future__ import annotations

from typing import Callable
from typing import List


def required_answer_validator(answer):
    if not answer:
        return 'Answer is required.'

    return True


def apply_multiple_validators(validators: List[Callable]):
    def apply_validators(answer):
        for validator in validators:
            result = validator(answer)

            if not result:
                return result

        return True

    return apply_validators
