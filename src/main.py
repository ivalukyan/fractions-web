from datetime import datetime
from math import floor

from typing import Annotated

from fastapi import FastAPI, Request, Form, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from database.db import Session, Task, Questions

app = FastAPI()

router = APIRouter()

arithmetic_router = APIRouter()
equations_router = APIRouter()
text_tasks_router = APIRouter()
geometry_router = APIRouter()
task_increased_complexity_router = APIRouter()
mixed_tasks_router = APIRouter()

router.include_router(arithmetic_router)
router.include_router(equations_router)
router.include_router(text_tasks_router)
router.include_router(geometry_router)
router.include_router(task_increased_complexity_router)
router.include_router(mixed_tasks_router)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory='static'), name='static')


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {'request': request})


@router.get("/addquestions")
async def addquestions(request: Request):
    return templates.TemplateResponse("addquestions.html", {'request': request})


@router.post("/addquestions")
async def addquestions(request: Request, class_student: Annotated[str, Form()], type_task: Annotated[str, Form()],
                       question: Annotated[str, Form()], answer: Annotated[str, Form()],
                       explanation: Annotated[str, Form()]):
    db_session = Session()
    new_task = Task(class_student=class_student, type_task=type_task, question=question,
                    answer=answer, explanation=explanation)
    db_session.add(new_task)
    db_session.commit()

    return templates.TemplateResponse("home.html", {'request': request})


@router.get('/class_selection')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@router.post('/class_selection')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):
    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)


@router.post('/task_selection/{class_id}')
async def task_selection(request: Request, class_id: str):
    task_id = 0
    correct = 0

    db_session = Session()
    new_question = Questions(start_time=datetime.now())
    db_session.add(new_question)
    db_session.commit()

    return templates.TemplateResponse("task_selection.html", {'request': request, 'class_id': class_id,
                                                              'task_id': task_id, 'correct': correct})


@router.get('/statistic/{task_type}/count/{count_correct}')
async def statistic(request: Request, task_type: str, count_correct: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.type_task == task_type).all()
        
        db_question = db_session.query(Questions).first()
    except HTTPException:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    total_count = len(db_task)
    
    average_time = db_question.end_time - db_question.start_time
    
    hour = db_question.end_time.hour - db_question.start_time.hour
    minute = db_question.end_time.minute - db_question.start_time.minute
    second = db_question.end_time.second - db_question.start_time.second
    
    
    average_time_second = round((hour * 3600 + minute * 60 + second) / total_count)
    hour_ = floor(average_time_second/3600)
    minute_ = floor((average_time_second - hour_ * 3600) / 60)
    second_ = average_time_second - minute_ * 60
    
    average_time = f'{hour_} : {minute_} : {second_}'
    
    percent = round(count_correct * 100 / total_count)
    
    if task_type == 'arithmetic_operation':
        if 90 < percent <= 100:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Арифметические задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznw6',
                                                                      'color': '#32CD32'})
        elif 60 < percent <= 89:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Арифметические задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznx9',
                                                                      'color': '#652f27'})
        else:
            db_session.delete(db_question)
            db_session.commit()
            return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                      'task_type': 'Арифметические задания',
                                                                      'total_count': total_count,
                                                                      'percent': percent,
                                                                      'correct_count': count_correct,
                                                                      'average_time': average_time,
                                                                      'img_url': 'https://clck.ru/3Bznxr',
                                                                      'color': '#652f27'})


