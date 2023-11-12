import re

subtasks = "1; 2; 3"

def all_values_must_be_int_validator(answer):
    values = [value.strip() for value in answer.split(sep=',')]
    invalid_chars_pattern = re.compile("[^0-9,\s]+")

    for value in values:
        try:
            int(value)
        except ValueError:
            return 'All values must be integer.'
        else:
            continue


print(all_values_must_be_int_validator(answer=subtasks))