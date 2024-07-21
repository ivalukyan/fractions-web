"""
 router Text Tasks
"""
from typing import Annotated

from fastapi import Request, HTTPException, Form
from starlette.responses import RedirectResponse

from src.database.db import Session, Task
from src.main import text_tasks_router, templates


@text_tasks_router.get('/task_selection/{class_id}/text_tasks/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int):
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
        return templates.TemplateResponse("completions/arithmetic.html", {'request': request,
                                                                          'class_id': class_id,
                                                                          'arithmetic_operations': 'Арифметические задания',
                                                                          'task': task.question,
                                                                          'task_id': task_id,
                                                                          'correct': correct})
    else:
        redirect_url = request.url_for('statistic', task_type='arithmetic_operation', count_correct=correct)
        return RedirectResponse(redirect_url)


@text_tasks_router.post('/task_selection/{class_id}/text_tasks/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int):
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
                ans = 'Правильно'
                explanation = ''
                task_id += 1
                correct += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'arithmetic_operations': 'Арифметические задания',
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
                                                   'arithmetic_operations': 'Арифметические задания',
                                                   'exp': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct})
    else:
        redirect_url = request.url_for('statistic', task_type='arithmetic_operation', count_correct=correct)
        return RedirectResponse(redirect_url)
