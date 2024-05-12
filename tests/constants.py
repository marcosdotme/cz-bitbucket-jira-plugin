import json


with open('tests/data/test_message_data.txt', mode='r') as file:
    lines = file.readlines()
    content = ''.join(lines[2:])

    ANSWER_AND_EXPECTED_OUTPUT = json.loads(content)
