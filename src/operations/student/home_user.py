from typing import Annotated

from fastapi import Request, APIRouter, Form
from starlette.templating import Jinja2Templates

from src.operations.student.__init__ import templates

router = APIRouter(prefix='/home_user', tags=['Home User'])


@router.get("/{email}/")
async def home_user(request: Request, email: str):
    return templates.TemplateResponse("home_user.html", {"request": request, 'email': email})


@router.post("/")
async def home_user(request: Request, email_student: Annotated[str, Form()]):
    return templates.TemplateResponse("home_user.html", {"request": request, 'email': email_student})


@router.get("/account/{email}/")
async def account_user(request: Request, email: str):
    return templates.TemplateResponse('account.html', {"request": request, 'email': email})
