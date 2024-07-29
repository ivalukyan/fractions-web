from datetime import datetime
from typing import Annotated

from fastapi import Request, HTTPException, Form, APIRouter
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from database.db import Task, Questions
from database.__init__ import Session

from src.operations.student.__init__ import templates

router = APIRouter(tags=['mixed tasks'])


@router.get('/task_selection/{email}/{class_id}/mixed_tasks/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int, email: str):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id).all()
    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')

    if len(db_task) > task_id and task_id is not None:

        task = db_task[task_id]

        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        return templates.TemplateResponse("student/completions/arithmetic.html", {'request': request,
                                                                                  'class_id': class_id,
                                                                                  'arithmetic_operations': 'Смешанные задания',
                                                                                  'task': task.question,
                                                                                  'task_id': task_id,
                                                                                  'correct': correct,
                                                                                  'email': email})
    else:

        db_session.query(Questions).filter(Questions.end_time == None).update({'end_time': datetime.now()})
        db_session.commit()

        redirect_url = request.url_for('statistic', task_type='mixed_tasks', count_correct=correct, email=email)
        return RedirectResponse(redirect_url)


@router.post('/task_selection/{email}/{class_id}/mixed_tasks/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int, email: str):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id).all()
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
                return templates.TemplateResponse("student/completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'title': 'Смешанные задания',
                                                   'type_task': 'mixed_tasks',
                                                   'explanation': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'email': email})
            else:
                ans = 'Неправильно'
                explanation = task.explanation
                task_id += 1
                return templates.TemplateResponse("student/completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'title': 'Смешанные задания',
                                                   'type_task': 'mixed_tasks',
                                                   'exp': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'email': email})
    else:
        redirect_url = request.url_for('statistic', task_type='mixed_tasks', count_correct=correct)
        return RedirectResponse(redirect_url)
