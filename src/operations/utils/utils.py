import asyncio

from database.db import Test, Student
from database.__init__ import Session


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


async def academic_performance():

    db_session = Session()
    percent = db_session.query(Student.percent).all()

    count = 0

    for _ in percent:
        count += _[0]

    return round(count / len(percent))


async def completed_tasks():

    db_session = Session()
    all_the_time = db_session.query(Student.all_times_tasks).all()

    count = 0

    for _ in all_the_time:
        count += _[0]

    return round(round(count / len(all_the_time)) / count * 100)


async def gold_stars():

    db_session = Session()
    all_gold_stars = db_session.query(Student.count_gold).all()

    print(all_gold_stars)

    count = 0

    for _ in all_gold_stars:
        count += _[0]

    return round(round(count / len(all_gold_stars)) / count * 100)
