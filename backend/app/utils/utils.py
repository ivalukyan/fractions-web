import re
from backend.app.database.__init__ import Session
from backend.app.database.db import Student, Teacher


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


def question_check(question: str) -> bool:
    valid = r"^[а-яА-Я0-9\s]+$"
    if re.match(valid, question):
        return True
    return False


def name_check(name: str) -> bool:
    valid = r"^[А-Я.][а-я]+$"
    if re.match(valid, name):
        return True
    return False


def username_check(username: str) -> bool:
    valid = r"^[a-zA-Z0-9]+$"
    if re.match(valid, username):
        return True
    return False


def is_exist_student(email: str) -> bool:
    db_session = Session()
    student = db_session.query(Student).filter(Student.email == email).first
    if student is not None and len(student) != 0:
        return True
    return False


if __name__ == '__main__':
    print(username_check("ivalkn70"))
