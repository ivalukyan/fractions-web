import re


def answer_check(answer: str) -> bool:
    valid = r"^([А-ЯЁ]*[а-яё]*|\s*|[0-9]*)$"
    if re.match(valid, answer):
        return True
    return False


def email_check(email: str) -> bool:
    valid = r"^[a-zA-Z0-9_.+-]+@[a-z]+\.[a-z]+$"
    if re.match(valid, email):
        return True
    return False


def password_check(password: str) -> bool:
    valid = r"^[-#&!$@a-zA-Z0-9]+$"
    if re.match(valid, password):
        return True
    return False
