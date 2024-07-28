from fastapi import FastAPI, Request, APIRouter, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typing import Annotated

from database.db import Session, Student
from models.models import AddStudentSchema

router = APIRouter(prefix='/home_teacher', tags=['Home Teacher'])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_teacher(request: Request):

    db_session = Session()
    students = db_session.query(Student).all()

    # if not students:
    #     raise HTTPException(status_code=404)
    return templates.TemplateResponse("home.html", {"request": request, 'data': students})


@router.post("/")
async def home_teacher(request: Request):

    db_session = Session()
    students = db_session.query(Student).all()

    # if not students:
    #     raise HTTPException(status_code=404)
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
