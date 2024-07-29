from typing import Annotated

from fastapi import Request, Form, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic
from starlette.responses import RedirectResponse

from src.operations.auth import templates

from pydantic import BaseModel


router = APIRouter(tags=["auth"])

security = HTTPBasic()


class AuthForm(BaseModel):
    username: str | None = None
    password: str | None = None


@router.get("/")
async def auth(request: Request):
    return templates.TemplateResponse("auth/auth.html", {'request': request})


@router.post("/auth_student")
async def auth_student(request: Request, user: Annotated[AuthForm, Depends(security)]):

    unauth_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )

    if user.username == 'example@gmail.com' and user.password == 'admin':
        redirect_url = request.url_for('home_user', email_student=user.username)
        return RedirectResponse(redirect_url)


@router.post("/auth_teacher")
async def auth_teacher(request: Request, user: Annotated[AuthForm, Depends(security)]):
    unauth_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )

    if user.username == 'example@gmail.com' and user.password == 'admin':
        redirect_url = request.url_for('home_teacher', email_teacher=user.username)
        return RedirectResponse(redirect_url)







# async def auth(request: Request, email_teacher: Annotated[str, Form()] = None,
#                password_teacher: Annotated[str, Form()] = None,
#                email_student: Annotated[str, Form()] = None,
#                password_student: Annotated[str, Form()] = None):
#
#
#     if await authenticate(model_first):
#         redirect_url = request.url_for('home_teacher', email_teacher=email_teacher)
#         return RedirectResponse(redirect_url)
#     elif await authenticate(model_second):
#         redirect_url = request.url_for('home_user', email_student=email_student)
#         return RedirectResponse(redirect_url)
#     else:
#         msg = 'Invalid email or password'
#         return templates.TemplateResponse("auth/auth.html", {'request': request, 'msg': msg})

