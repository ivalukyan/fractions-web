from math import floor

from fastapi import Request, HTTPException, APIRouter
from starlette.templating import Jinja2Templates

from database.db import Session, Task, Questions

router = APIRouter(prefix='/statistic', tags=['statistic'])

templates = Jinja2Templates(directory="templates")


@router.get('/{task_type}/count/{count_correct}')
async def statistic(request: Request, task_type: str, count_correct: int):
    try:
        db_session = Session()
        if task_type == 'mixed_tasks':
            db_task = db_session.query(Task).all()
        else:
            db_task = db_session.query(Task).filter(Task.type_task == task_type).all()

        db_question = db_session.query(Questions).first()
    except HTTPException:
        raise HTTPException(status_code=400, detail="Bad Request")

    total_count = len(db_task)

    hour = db_question.end_time.hour - db_question.start_time.hour
    minute = db_question.end_time.minute - db_question.start_time.minute
    second = db_question.end_time.second - db_question.start_time.second

    average_time_second = round((hour * 3600 + minute * 60 + second) / total_count)
    hour_ = floor(average_time_second / 3600)
    minute_ = floor((average_time_second - hour_ * 3600) / 60)
    second_ = average_time_second - minute_ * 60

    average_time = f'{hour_} : {minute_} : {second_}'

    percent = round(count_correct * 100 / total_count)

    if task_type == 'arithmetic_operation':
        if 90 < percent <= 100:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Арифметические задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznw6',
                                                                      'color': '#32CD32'})
        elif 60 < percent <= 89:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Арифметические задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznx9',
                                                                      'color': '#652f27'})
        else:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Арифметические задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznxr',
                                                                      'color': '#652f27'})
    elif task_type == 'equations':
        if 90 < percent <= 100:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Уравнения',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznw6',
                                                                      'color': '#32CD32'})
        elif 60 < percent <= 89:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Уравнения',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznx9',
                                                                      'color': '#652f27'})
        else:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Уравнения',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznxr',
                                                                      'color': '#652f27'})
    elif task_type == 'text_tasks':
        if 90 < percent <= 100:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Текстовые задачи',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznw6',
                                                                      'color': '#32CD32'})
        elif 60 < percent <= 89:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Текстовые задачи',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznx9',
                                                                      'color': '#652f27'})
        else:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Текстовые задачи',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznxr',
                                                                      'color': '#652f27'})
    elif task_type == 'task_increased_complexity':
        if 90 < percent <= 100:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Задания повышенной сложности',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznw6',
                                                                      'color': '#32CD32'})
        elif 60 < percent <= 89:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Задания повышенной сложности',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznx9',
                                                                      'color': '#652f27'})
        else:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Задания повышенной сложности',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznxr',
                                                                      'color': '#652f27'})

    elif task_type == 'mixed_tasks':
        if 90 < percent <= 100:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Смешанные задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznw6',
                                                                      'color': '#32CD32'})
        elif 60 < percent <= 89:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Смешанные задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznx9',
                                                                      'color': '#652f27'})
        else:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Смешанные задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznxr',
                                                                      'color': '#652f27'})

