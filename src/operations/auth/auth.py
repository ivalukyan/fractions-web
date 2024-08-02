from typing import Annotated

from fastapi import Request, APIRouter, HTTPException, status, Form
from starlette.responses import RedirectResponse

from database.__init__ import Session
from database.db import Student, Teacher
from src.operations.auth import templates

from env import Admin

router = APIRouter(tags=["auth"])

admin = Admin()


@router.get("/")
async def auth(request: Request):
    return templates.TemplateResponse("auth/auth.html", {'request': request})


@router.post("/auth_student")
async def auth_student(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):

    db_session = Session()
    student = db_session.query(Student).filter(Student.email == email).first()

    unauth = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
    msg = 'Ivalid email or password'

    if student is not None:
        if password in student.password:
            redirect_url = request.url_for('home_user', email_student=email)
            return RedirectResponse(redirect_url)
        else:
            return templates.TemplateResponse("auth/auth.html", {'request': request, 'msg': msg})
    else:
        raise unauth


@router.post("/auth_teacher")
async def auth_teacher(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):

    db_session = Session()
    teacher = db_session.query(Teacher).filter(Teacher.email == email).first()

    unauth = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
    msg = 'Ivalid email or password'

    if email in admin.username and password in admin.password:
        redirect_url = request.url_for('home_teacher', email_teacher=email)
        return RedirectResponse(redirect_url)
    else:
        if teacher is not None:

            if password in teacher.password:
                redirect_url = request.url_for('home_teacher', email_teacher=email)
                return RedirectResponse(redirect_url)
            else:
                return templates.TemplateResponse('auth/auth.html', {'request': request, 'msg': msg})
        else:
            raise unauth
