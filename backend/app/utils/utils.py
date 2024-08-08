import re


def answer_check(answer: str) -> bool:
    valid = r'^([А-ЯЁ]*[а-яё]*|\s*|[0-9]*)$'
    if re.match(valid, answer):
        return True
    return False


if __name__ == '__main__':
    pass
