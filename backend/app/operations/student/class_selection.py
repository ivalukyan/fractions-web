from typing import Annotated

from fastapi import Request, Form, APIRouter
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from app.database.__init__ import Session
from app.database.db import Questions

router = APIRouter(prefix='/class_selection', tags=['class selection'])

templates = Jinja2Templates(directory="app/templates")


@router.get('/{email}/10')
async def class_selection(request: Request, email: str):
    return templates.TemplateResponse("student/class_selection.html", {'request': request, 'email': email})


@router.get('/{email}/15')
async def class_selection(request: Request, email: str):
    return templates.TemplateResponse("student/class_selection.html", {'request': request, 'email': email})


@router.get('/{email}/20')
async def class_selection(request: Request, email: str):
    return templates.TemplateResponse("student/class_selection.html", {'request': request, 'email': email})


@router.get('/{email}/25')
async def class_selection(request: Request, email: str):
    return templates.TemplateResponse("student/class_selection.html", {'request': request, 'email': email})


@router.post('/{email}/10')
async def class_selection(request: Request, class_id: Annotated[str, Form()], email: str):

    db_session = Session()
    user = db_session.query(Questions).filter(Questions.email == email).first()
    print(user)
    if not user:
        count_tasks = Questions(email=email, count_task=10)
        db_session.add(count_tasks)
        db_session.commit()
    else:
        if not user.email:
            count_tasks = Questions(email=email, count_task=10)
            db_session.add(count_tasks)
            db_session.commit()
        else:
            db_session.query(Questions).filter(Questions.email == email).update({'count_task': 10})
            db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id, email=email)
    return RedirectResponse(redirect_url)


@router.post('/{email}/15')
async def class_selection(request: Request, class_id: Annotated[str, Form()], email: str):

    db_session = Session()
    user = db_session.query(Questions).filter(Questions.email == email).first()
    if not user:
        count_tasks = Questions(email=email, count_task=15)
        db_session.add(count_tasks)
        db_session.commit()
    else:
        if not user.email:
            count_tasks = Questions(email=email, count_task=15)
            db_session.add(count_tasks)
            db_session.commit()
        else:
            db_session.query(Questions).filter(Questions.email == email).update({'count_task': 15})
            db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id, email=email)
    return RedirectResponse(redirect_url)


@router.post('/{email}/20')
async def class_selection(request: Request, class_id: Annotated[str, Form()], email: str):

    db_session = Session()
    user = db_session.query(Questions).filter(Questions.email == email).first()

    if not user:
        count_tasks = Questions(email=email, count_task=20)
        db_session.add(count_tasks)
        db_session.commit()
    else:
        if not user.email:
            count_tasks = Questions(email=email, count_task=20)
            db_session.add(count_tasks)
            db_session.commit()
        else:
            db_session.query(Questions).filter(Questions.email == email).update({'count_task': 20})
            db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id, email=email)
    return RedirectResponse(redirect_url)


@router.post('/{email}/25')
async def class_selection(request: Request, class_id: Annotated[str, Form()], email: str):

    db_session = Session()
    user = db_session.query(Questions).filter(Questions.email == email).first()
    if not user:
        count_tasks = Questions(email=email, count_task=25)
        db_session.add(count_tasks)
        db_session.commit()
    else:
        if not user.email:
            count_tasks = Questions(email=email, count_task=15)
            db_session.add(count_tasks)
            db_session.commit()
        else:
            db_session.query(Questions).filter(Questions.email == email).update({'count_task': 25})
            db_session.commit()

    redirect_url = request.url_for("task_selection", class_id=class_id, email=email)
    return RedirectResponse(redirect_url)
