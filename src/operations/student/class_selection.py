from typing import Annotated

from fastapi import Request, Form, APIRouter
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from database.__init__ import Session
from database.db import Questions

router = APIRouter(prefix='/class_selection', tags=['class selection'])

templates = Jinja2Templates(directory="templates")


@router.get('/10')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@router.get('/15')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@router.get('/20')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@router.get('/25')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@router.post('/10')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):

    db_session = Session()
    count_tasks = Questions(count_task=10)
    db_session.add(count_tasks)
    db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)


@router.post('/15')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):

    db_session = Session()
    count_tasks = Questions(count_task=15)
    db_session.add(count_tasks)
    db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)


@router.post('/20')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):

    db_session = Session()
    count_tasks = Questions(count_task=20)
    db_session.add(count_tasks)
    db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)


@router.post('/25')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):

    db_session = Session()
    count_tasks = Questions(count_task=25)
    db_session.add(count_tasks)
    db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)
