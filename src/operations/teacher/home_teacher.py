from typing import Annotated

from fastapi import Request, APIRouter, Form
from starlette.responses import RedirectResponse

from database.__init__ import Session
from database.db import Student, Test, Task
from src.operations.teacher.__init__ import templates
from src.operations.utils.utils import academic_performance, completed_tasks, gold_stars

router = APIRouter(prefix='/home_teacher', tags=['Home Teacher'])


@router.get("/{email_teacher}")
async def home_teacher(request: Request, email_teacher: str):

    db_session = Session()
    students = db_session.query(Student).all()

    academic_percent = await academic_performance()

    completed_task = await completed_tasks()

    gold_star = await gold_stars()

    return templates.TemplateResponse("teacher/home.html", {"request": request,
                                                            'data': students,
                                                            'email_teacher': email_teacher,
                                                            'academic_percent': academic_percent,
                                                            'completed_tasks': completed_task,
                                                            'gold_stars': gold_star})


@router.post("/{email_teacher}")
async def home_teacher(request: Request, email_teacher: str):

    db_session = Session()
    students = db_session.query(Student).all()

    academic_percent = await academic_performance()

    completed_task = await completed_tasks()

    gold_star = await gold_stars()

    return templates.TemplateResponse("teacher/home.html", {"request": request,
                                                            'data': students,
                                                            'email_teacher': email_teacher,
                                                            'academic_percent': academic_percent,
                                                            'completed_task': completed_task,
                                                            'gold_stars': gold_star})


@router.get("/{email_teach}/addstudent/")
async def add_student(request: Request, email_teach: str):
    return templates.TemplateResponse("teacher/addstudent.html", {"request": request, 'email_teach': email_teach})


@router.post("/{email_teach}/addstudent/")
async def add_student(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()],
                      password: Annotated[str, Form()], class_select: Annotated[str, Form()],
                      email_teacher: Annotated[str, Form()], email_teach: str):

    db_session = Session()
    student = Student(name=name, email=email, password=password, email_teacher=email_teacher, class_student=class_select)
    test = Test(email=email)

    db_session.add(student)
    db_session.add(test)

    db_session.commit()

    redirect_url = request.url_for("home_teacher", email_teacher=email_teach)
    return RedirectResponse(redirect_url)


@router.get("/{email_teacher}/deletestudent/")
async def delete_student(request: Request, email_teacher: str):
    return templates.TemplateResponse("teacher/delstudent.html", {"request": request, 'email_teacher': email_teacher})


@router.post("/{email_teacher}/deletestudent/")
async def delete_student(request: Request, email_delete: Annotated[str, Form()], email_teacher: str):

    db_session = Session()
    student = db_session.query(Student).filter_by(email=email_delete).first()
    db_session.delete(student)
    db_session.commit()

    redirect_url = request.url_for("home_teacher", email_teacher=email_teacher)
    return RedirectResponse(redirect_url)


@router.get("/viewquestions/{email}")
async def view_questions(request: Request, email: str):

    db_session = Session()
    data = db_session.query(Task).all()

    return templates.TemplateResponse("teacher/viewquestions.html", {"request": request, 'email_teacher': email,
                                                                     'data': data})
