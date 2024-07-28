from fastapi import Request, APIRouter, Form, HTTPException
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typing import Annotated


router = APIRouter(tags=["auth"])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def auth(request: Request):
    return templates.TemplateResponse("auth.html", {'request': request})


@router.post("/")
async def auth(request: Request, email_teacher: Annotated[str, Form()] = None,
               password_teacher: Annotated[str, Form()] = None,
               email_student: Annotated[str, Form()] = None,
               password_student: Annotated[str, Form()] = None):

    if email_teacher == 'example@gmail.com' and password_teacher == 'admin':
        redirect_url = request.url_for('home_teacher')
        return RedirectResponse(redirect_url)
    elif email_student == 'example@gmail.com' and password_student == 'admin':
        redirect_url = request.url_for('home_user')
        return RedirectResponse(redirect_url)
    else:
        msg = 'Invalid email or password'
        return templates.TemplateResponse("auth.html", {'request': request, 'msg': msg})

