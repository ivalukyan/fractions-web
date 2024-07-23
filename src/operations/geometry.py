from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi import Request, Form
from starlette.responses import RedirectResponse

from database.db import Session, Task, Questions
from starlette.templating import Jinja2Templates

router = APIRouter(tags=['geometry'])

templates = Jinja2Templates(directory="templates")



@router.get('/task_selection/{class_id}/geometry/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'geometry').all()
    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')
    
    if len(db_task) > task_id and task_id is not None:
        
        task = db_task[task_id]
        
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        return templates.TemplateResponse("completions/geometry.html", {'request': request,
                                                                          'class_id': class_id,
                                                                          'arithmetic_operations': 'Геометрия',
                                                                          'task': task.question,
                                                                          'task_id': task_id,
                                                                          'correct': correct})
    else:
        redirect_url = request.url_for('statistic', task_type='geometry', count_correct=correct)
        return RedirectResponse(redirect_url)


@router.post('/task_selection/{class_id}/geometry/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'geometry').all()
    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')
    
    if len(db_task) > task_id and task_id is not None:
        
        task = db_task[task_id]
        
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        else:
            
            if answer == task.answer:
                ans = 'Правильно'
                explanation = ''
                task_id += 1
                correct += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'arithmetic_operations': 'Геометрия',
                                                   'explanation': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct})
            else:
                ans = 'Неправильно'
                explanation = task.explanation
                task_id += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'arithmetic_operations': 'Геометрия',
                                                   'exp': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct})
    else:
        redirect_url = request.url_for('statistic', task_type='geometry', count_correct=correct)
        return RedirectResponse(redirect_url)
