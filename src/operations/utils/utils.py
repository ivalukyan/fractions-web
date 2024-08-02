import asyncio

from database.db import Test, Student
from database.__init__ import Session

from env import Admin

admin = Admin()


async def add_test(email: str, operation: str, count_task: int, is_correct: int):
    """
    Adds a new test to the database
    """
    try:
        db_session = Session()

        test = db_session.query(Test).filter(Test.email == email, Test.type_task == operation).first()

    except Exception as e:
        raise e

    if test is None:

        result_student = Test(email=email, type_task=operation, count_task=count_task, is_correct=is_correct)
        db_session.add(result_student)
        db_session.commit()

    else:

        new_count_task = test.count_task + count_task
        new_is_correct = test.is_correct + is_correct

        db_session.query(Test).filter(Test.email == email).update({'count_task': new_count_task,
                                                                   'is_correct': new_is_correct})
        db_session.commit()


async def academic_performance(email: str):

    if email in admin.username:
        db_session = Session()
        percent = db_session.query(Student.percent).all()
    else:
        db_session = Session()
        percent = db_session.query(Student.percent).filter(Student.email_teacher == email).all()

    count = 0

    for _ in percent:
        count += _[0]

    if len(percent) == 0:
        return 0

    return round(count / len(percent))


async def completed_tasks(email: str):

    if email in admin.username:
        db_session = Session()
        all_the_time = db_session.query(Student.all_times_tasks).all()
    else:
        db_session = Session()
        all_the_time = db_session.query(Student.all_times_tasks).filter(Student.email_teacher == email).all()

    count = 0

    for _ in all_the_time:
        count += _[0]

    if len(all_the_time) == 0:
        return 0

    return round(round(count / len(all_the_time)) / count * 100)


async def gold_stars(email: str):

    if email in admin.username:
        db_session = Session()
        all_gold_stars = db_session.query(Student.count_gold).all()
    else:
        db_session = Session()
        all_gold_stars = db_session.query(Student.count_gold).filter(Student.email_teacher == email).all()

    count = 0

    for _ in all_gold_stars:
        count += _[0]

    if len(all_gold_stars) == 0:
        return 0

    return round(round(count / len(all_gold_stars)) / count * 100)
