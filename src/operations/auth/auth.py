from typing import Annotated

from fastapi import Request, APIRouter, HTTPException, status, Form
from starlette.responses import RedirectResponse

from database.__init__ import Session
from database.db import Student
from src.operations.auth import templates

router = APIRouter(tags=["auth"])


@router.get("/")
async def auth(request: Request):
    return templates.TemplateResponse("auth/auth.html", {'request': request})


@router.post("/auth_student")
async def auth_student(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):

    db_session = Session()
    student = db_session.query(Student).filter(Student.email == email).first()
    is_password = db_session.query(Student).filter(Student.email == email).first().password

    unauth = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid email or password')

    if student is None:
        raise unauth
    else:
        if password in is_password:
            redirect_url = request.url_for('home_user', email_student=email)
            return RedirectResponse(redirect_url)
        else:
            raise unauth


@router.post("/auth_teacher")
async def auth_teacher(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):

    unauth = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid email or password')

    if email == 'example@gmail.com' and password == 'admin':
        redirect_url = request.url_for('home_teacher', email_teacher=email)
        return RedirectResponse(redirect_url)
    else:
        raise unauth
