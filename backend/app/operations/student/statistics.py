from math import floor

from fastapi import Request, HTTPException, APIRouter

from app.database.__init__ import Session
from app.database.db import Task, Questions, Student
from app.operations.student.__init__ import templates

from app.operations.utils.utils import add_test

router = APIRouter(prefix='/statistic', tags=['statistic'])


@router.get('/{email}/{task_type}/count/{count_correct}/{total_count}')
async def statistic(request: Request, task_type: str, count_correct: int, email: str, total_count: int):
    try:
        db_session = Session()
        if task_type == 'mixed_tasks':
            db_task = db_session.query(Task).all()
        else:
            db_task = db_session.query(Task).filter(Task.type_task == task_type).all()

        db_question = db_session.query(Questions).filter(Questions.email == email).first()
    except HTTPException:
        raise HTTPException(status_code=400, detail="Bad Request")

    all_count = db_question.count_task

    hour = db_question.end_time.hour - db_question.start_time.hour
    minute = db_question.end_time.minute - db_question.start_time.minute
    second = db_question.end_time.second - db_question.start_time.second

    average_time_second = round((hour * 3600 + minute * 60 + second) / total_count)
    hour_ = floor(average_time_second / 3600)
    minute_ = floor((average_time_second - hour_ * 3600) / 60)
    second_ = average_time_second - minute_ * 60

    average_time = f'{hour_} ч : {minute_} мин : {second_} сек'

    percent = round(count_correct * 100 / total_count)

    if task_type == 'arithmetic_operation':
        if 90 < percent <= 100:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                gold_stars = student.count_gold + 1

                db_session.query(Student).filter(Student.email == email).update({'count_gold': gold_stars})
                db_session.commit()

            await add_test(email, 'arithmetic_operation', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Арифметические задания',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznw6',
                                                                              'color': '#32CD32',
                                                                              'email': email})
        elif 60 < percent <= 89:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                silver_stars = student.count_silver + 1

                db_session.query(Student).filter(Student.email == email).update({'count_silver': silver_stars})
                db_session.commit()

            await add_test(email, 'arithmetic_operation', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Арифметические задания',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznx9',
                                                                              'color': '#652f27',
                                                                              'email': email})
        else:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                bronze_stars = student.count_bronze + 1

                db_session.query(Student).filter(Student.email == email).update({'count_bronze': bronze_stars})
                db_session.commit()

            await add_test(email, 'arithmetic_operation', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Арифметические задания',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznxr',
                                                                              'color': '#652f27',
                                                                              'email': email})
    elif task_type == 'equations':
        if 90 < percent <= 100:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                gold_stars = student.count_gold + 1

                db_session.query(Student).filter(Student.email == email).update({'count_gold': gold_stars})
                db_session.commit()

            await add_test(email, 'equations', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Уравнения',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznw6',
                                                                              'color': '#32CD32',
                                                                              'email': email})
        elif 60 < percent <= 89:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                silver_stars = student.count_silver + 1

                db_session.query(Student).filter(Student.email == email).update({'count_silver': silver_stars})
                db_session.commit()

            await add_test(email, 'equations', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Уравнения',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznx9',
                                                                              'color': '#652f27',
                                                                              'email': email})
        else:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                bronze_stars = student.count_bronze + 1

                db_session.query(Student).filter(Student.email == email).update({'count_bronze': bronze_stars})
                db_session.commit()

            await add_test(email, 'equations', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Уравнения',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznxr',
                                                                              'color': '#652f27',
                                                                              'email': email})
    elif task_type == 'text_tasks':
        if 90 < percent <= 100:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                gold_stars = student.count_gold + 1

                db_session.query(Student).filter(Student.email == email).update({'count_gold': gold_stars})
                db_session.commit()

            await add_test(email, 'text_tasks', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Текстовые задачи',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznw6',
                                                                              'color': '#32CD32',
                                                                              'email': email})
        elif 60 < percent <= 89:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                silver_stars = student.count_silver + 1

                db_session.query(Student).filter(Student.email == email).update({'count_silver': silver_stars})
                db_session.commit()

            await add_test(email, 'text_tasks', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Текстовые задачи',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznx9',
                                                                              'color': '#652f27',
                                                                              'email': email})
        else:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                bronze_stars = student.count_bronze + 1

                db_session.query(Student).filter(Student.email == email).update({'count_bronze': bronze_stars})
                db_session.commit()

            await add_test(email, 'text_tasks', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Текстовые задачи',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznxr',
                                                                              'color': '#652f27',
                                                                              'email': email})
    elif task_type == 'task_increased_complexity':
        if 90 < percent <= 100:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                gold_stars = student.count_gold + 1

                db_session.query(Student).filter(Student.email == email).update({'count_gold': gold_stars})
                db_session.commit()

            await add_test(email, 'task_increased_complexity', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Задания повышенной сложности',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznw6',
                                                                              'color': '#32CD32',
                                                                              'email': email})
        elif 60 < percent <= 89:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                silver_stars = student.count_silver + 1

                db_session.query(Student).filter(Student.email == email).update({'count_silver': silver_stars})
                db_session.commit()

            await add_test(email, 'task_increased_complexity', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Задания повышенной сложности',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznx9',
                                                                              'color': '#652f27',
                                                                              'email': email})
        else:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                bronze_stars = student.count_bronze + 1

                db_session.query(Student).filter(Student.email == email).update({'count_bronze': bronze_stars})
                db_session.commit()

            await add_test(email, 'task_increased_complexity', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Задания повышенной сложности',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznxr',
                                                                              'color': '#652f27',
                                                                              'email': email})

    elif task_type == 'mixed_tasks':
        if 90 < percent <= 100:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                gold_stars = student.count_gold + 1

                db_session.query(Student).filter(Student.email == email).update({'count_gold': gold_stars})
                db_session.commit()

            await add_test(email, 'mixed_tasks', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Смешанные задания',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznw6',
                                                                              'color': '#32CD32',
                                                                              'email': email})
        elif 60 < percent <= 89:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                silver_stars = student.count_silver + 1

                db_session.query(Student).filter(Student.email == email).update({'count_silver': silver_stars})
                db_session.commit()

            await add_test(email, 'mixed_tasks', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Смешанные задания',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznx9',
                                                                              'color': '#652f27',
                                                                              'email': email})
        else:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                bronze_stars = student.count_bronze + 1

                db_session.query(Student).filter(Student.email == email).update({'count_bronze': bronze_stars})
                db_session.commit()

            await add_test(email, 'mixed_tasks', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Смешанные задания',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznxr',
                                                                              'color': '#652f27',
                                                                              'email': email})

    elif task_type == 'geometry':
        if 90 < percent <= 100:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                gold_stars = student.count_gold + 1

                db_session.query(Student).filter(Student.email == email).update({'count_gold': gold_stars})
                db_session.commit()

            await add_test(email, 'geometry', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Геометрия',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznw6',
                                                                              'color': '#32CD32',
                                                                              'email': email})
        elif 60 < percent <= 89:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                silver_stars = student.count_silver + 1

                db_session.query(Student).filter(Student.email == email).update({'count_silver': silver_stars})
                db_session.commit()

            await add_test(email, 'geometry', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Геометрия',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznx9',
                                                                              'color': '#652f27',
                                                                              'email': email})
        else:

            student = db_session.query(Student).filter(Student.email == email).first()
            if student is not None:

                bronze_stars = student.count_bronze + 1

                db_session.query(Student).filter(Student.email == email).update({'count_bronze': bronze_stars})
                db_session.commit()

            await add_test(email, 'geometry', total_count, count_correct)

            return templates.TemplateResponse("student/statistic_page.html", {'request': request,
                                                                              'task_type': 'Геометрия',
                                                                              'total_count': total_count,
                                                                              'percent': percent,
                                                                              'correct_count': count_correct,
                                                                              'average_time': average_time,
                                                                              'img_url': 'https://clck.ru/3Bznxr',
                                                                              'color': '#652f27',
                                                                              'email': email})
