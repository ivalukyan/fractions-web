from typing import Annotated

from fastapi import Request, APIRouter, Form
from starlette.responses import RedirectResponse

from database.__init__ import Session
from database.db import Student
from src.operations.teacher.__init__ import templates

router = APIRouter(prefix='/home_teacher', tags=['Home Teacher'])


@router.get("/{email_teacher}")
async def home_teacher(request: Request, email_teacher: str):

    db_session = Session()
    students = db_session.query(Student).all()

    return templates.TemplateResponse("teacher/home.html", {"request": request, 'data': students, 'email_teacher': email_teacher})


@router.post("/{email_teacher}")
async def home_teacher(request: Request, email_teacher: str):

    db_session = Session()
    students = db_session.query(Student).all()

    return templates.TemplateResponse("teacher/home.html", {"request": request, 'data': students, 'email_teacher': email_teacher})


@router.get("/{email_teach}/addstudent/")
async def add_student(request: Request, email_teach: str):
    return templates.TemplateResponse("teacher/addstudent.html", {"request": request, 'email_teach': email_teach})


@router.post("/{email_teach}/addstudent/")
async def add_student(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()],
                      password: Annotated[str, Form()], class_select: Annotated[str, Form()],
                      email_teacher: Annotated[str, Form()], email_teach: str):

    db_session = Session()
    student = Student(name=name, email=email, password=password, email_teacher=email_teacher, class_student=class_select)
    db_session.add(student)
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
