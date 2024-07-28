from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import Annotated

router = APIRouter(prefix='/home_user', tags=['Home User'])

templates = Jinja2Templates(directory="templates")


@router.get("/{email}/")
async def home_user(request: Request, email: str):
    return templates.TemplateResponse("home_user.html", {"request": request, 'email': email})


@router.post("/")
async def home_user(request: Request, email_student: Annotated[str, Form()]):
    return templates.TemplateResponse("home_user.html", {"request": request, 'email': email_student})


@router.get("/account/{email}/")
async def account_user(request: Request, email: str):
    return templates.TemplateResponse('account.html', {"request": request, 'email': email})
