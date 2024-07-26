from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import Annotated

router = APIRouter(prefix='/home_teacher', tags=['Home Teacher'])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_teacher(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/")
async def home_teacher(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
