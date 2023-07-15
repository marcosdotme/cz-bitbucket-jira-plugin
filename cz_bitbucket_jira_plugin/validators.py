def required_answer_validator(answer_title):
    def has_answer(answer):
        if not answer:
            return f"'{answer_title}' is required."

        return True

    return has_answer
