from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi import Request, Form
from starlette.responses import RedirectResponse

from database.db import Session, Task, Questions
from starlette.templating import Jinja2Templates

router = APIRouter(tags=['arithmetic'])

templates = Jinja2Templates(directory="templates")


@router.get('/task_selection/{class_id}/arithmetic_operation/{task_id}/{correct}/{count_task}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int, count_task: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'arithmetic_operation').all()

        cnt_tsk = db_session.query(Questions).first()

    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')
    
    if len(db_task) > task_id and task_id is not None and cnt_tsk.count_task >= count_task:
        
        task = db_task[task_id]
        
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        return templates.TemplateResponse("completions/arithmetic.html", {'request': request,
                                                                          'class_id': class_id,
                                                                          'arithmetic_operations': 'Арифметические задания',
                                                                          'task': task.question,
                                                                          'task_id': task_id,
                                                                          'correct': correct,
                                                                          'count_task': count_task})
    else:
        
        db_session.query(Questions).filter(Questions.end_time == None).update({'end_time': datetime.now()})
        db_session.commit()
        
        redirect_url = request.url_for('statistic', task_type='arithmetic_operation', count_correct=correct)
        return RedirectResponse(redirect_url)


@router.post('/task_selection/{class_id}/arithmetic_operation/{task_id}/{correct}/{count_task}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int, count_task: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'arithmetic_operation').all()
    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')
    
    if len(db_task) > task_id and task_id is not None:
        
        task = db_task[task_id]
        
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        else:
            
            if answer == task.answer:
                is_correct = 'Правильно'
                explanation = ''
                task_id += 1
                correct += 1
                count_task += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'is_correct': is_correct,
                                                   'answer': answer,
                                                   'correct_answer': task.answer,
                                                   'title': 'Арифметические задания',
                                                   'type_task': 'arithmetic_operation',
                                                   'explanation': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'count_task': count_task})
            else:
                is_correct = 'Неправильно'
                explanation = task.explanation
                task_id += 1
                count_task += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'is_correct': is_correct,
                                                   'answer': answer,
                                                   'correct_answer': task.answer,
                                                   'title': 'Арифметические задания',
                                                   'type_task': 'arithmetic_operation',
                                                   'exp': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'count_task': count_task})
    else:
        redirect_url = request.url_for('statistic', task_type='arithmetic_operation', count_correct=correct)
        return RedirectResponse(redirect_url)
