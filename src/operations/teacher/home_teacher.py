from typing import Annotated

from fastapi import Request, APIRouter, Form
from starlette.responses import RedirectResponse

from database.__init__ import Session
from database.db import Student
from src.operations.teacher.__init__ import templates

router = APIRouter(prefix='/home_teacher', tags=['Home Teacher'])


@router.get("/")
async def home_teacher(request: Request):

    db_session = Session()
    students = db_session.query(Student).all()

    return templates.TemplateResponse("home.html", {"request": request, 'data': students})


@router.post("/")
async def home_teacher(request: Request):

    db_session = Session()
    students = db_session.query(Student).all()

    return templates.TemplateResponse("home.html", {"request": request, 'data': students})


@router.get("/addstudent/")
async def add_student(request: Request):
    return templates.TemplateResponse("addstudent.html", {"request": request})


@router.post("/addstudent/")
async def add_student(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()],
                      password: Annotated[str, Form()], class_select: Annotated[str, Form()],
                      email_teacher: Annotated[str, Form()]):

    db_session = Session()
    student = Student(name=name, email=email, password=password, email_teacher=email_teacher, class_student=class_select)
    db_session.add(student)
    db_session.commit()

    redirect_url = request.url_for("home_teacher")
    return RedirectResponse(redirect_url)


@router.get("/deletestudent/")
async def delete_student(request: Request):
    return templates.TemplateResponse("delstudent.html", {"request": request})


@router.post("/deletestudent/")
async def delete_student(request: Request, email_delete: Annotated[str, Form()]):

    db_session = Session()
    student = db_session.query(Student).filter_by(email=email_delete).first()
    db_session.delete(student)
    db_session.commit()

    redirect_url = request.url_for("home_teacher")
    return RedirectResponse(redirect_url)
