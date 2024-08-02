from fastapi import Request, APIRouter

from src import templates

from database import Session
from database.db import Student, Test

router = APIRouter(prefix='/home_user', tags=['Home User'])


@router.get("/{email}/")
async def home_user(request: Request, email: str):
    return templates.TemplateResponse("student/home_user.html", {"request": request, 'email': email})


@router.post("/{email_student}")
async def home_user(request: Request, email_student: str):
    return templates.TemplateResponse("student/home_user.html", {"request": request, 'email': email_student})


@router.get("/account/{email}/")
async def account_user(request: Request, email: str):
    db_session = Session()

    student = db_session.query(Student).filter(Student.email == email).first()
    test = db_session.query(Test).filter(Test.email == email).first()

    if test is not None:

        # Arithmetic Operations
        arithmetic_operation = db_session.query(Test).filter(Test.email == email,
                                                             Test.type_task == 'arithmetic_operation').first()
        if arithmetic_operation is not None:
            percent_arith = round(arithmetic_operation.is_correct / arithmetic_operation.count_task * 100)
        else:
            percent_arith = 0

        # Equations Operations
        equations = db_session.query(Test).filter(Test.email == email,
                                                  Test.type_task == 'equations').first()
        if equations is not None:
            percent_equ = round(equations.is_correct / equations.count_task * 100)
        else:
            percent_equ = 0

        # Text tasks Operations
        text_tasks = db_session.query(Test).filter(Test.email == email,
                                                   Test.type_task == 'text_tasks').first()
        if text_tasks is not None:
            percent_text_task = round(text_tasks.is_correct / text_tasks.count_task * 100)
        else:
            percent_text_task = 0

        # Task Increased Complexity
        task_increased_complexity = db_session.query(Test).filter(Test.email == email,
                                                                  Test.type_task == 'task_increased_complexity').first()
        if task_increased_complexity is not None:
            percent_task_increased = round(task_increased_complexity.is_correct / task_increased_complexity.count_task
                                           * 100)
        else:
            percent_task_increased = 0

        # Mixed Tasks
        mixed_tasks = db_session.query(Test).filter(Test.email == email,
                                                    Test.type_task == 'mixed_tasks').first()
        if mixed_tasks is not None:
            percent_mixed = round(mixed_tasks.is_correct / mixed_tasks.count_task * 100)
        else:
            percent_mixed = 0

        # Geometry
        geometry = db_session.query(Test).filter(Test.email == email,
                                                 Test.type_task == 'geometry').first()
        if geometry is not None:
            percent_geometry = round(geometry.is_correct / geometry.count_task * 100)
        else:
            percent_geometry = 0

        return templates.TemplateResponse('student/account.html', {"request": request,
                                                                   'email': email,
                                                                   'username': student.name,
                                                                   'all_is_correct': student.all_is_correct,
                                                                   'count_gold': student.count_gold,
                                                                   'count_silver': student.count_silver,
                                                                   'count_bronze': student.count_bronze,
                                                                   'arithmetic_operation': arithmetic_operation,
                                                                   'equations': equations,
                                                                   'text_tasks': text_tasks,
                                                                   'task_increased_complexity': task_increased_complexity,
                                                                   'mixed_tasks': mixed_tasks,
                                                                   'geometry': geometry,
                                                                   'percent_arith': percent_arith,
                                                                   'percent_equ': percent_equ,
                                                                   'percent_text_task': percent_text_task,
                                                                   'percent_task_increased': percent_task_increased,
                                                                   'percent_mixed': percent_mixed,
                                                                   'percent_geometry': percent_geometry,
                                                                   'percent': student.percent})
    else:
        exp = 'Недостаточно данных, для составления статистики пройдите все виды тестов по одному разу'
        return templates.TemplateResponse('student/home_user.html', {"request": request, 'email': email, 'exp': exp})
