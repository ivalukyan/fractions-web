from datetime import datetime
from typing import Annotated

from database.db import Task, Questions
from database.__init__ import Session

from fastapi import Request, HTTPException, Form, APIRouter

from starlette.responses import RedirectResponse

from src.operations.student.__init__ import templates

router = APIRouter(tags=['equations'])


@router.get('/task_selection/{email}/{class_id}/equations/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int, email: str):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'equations').all()
    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')

    if len(db_task) > task_id and task_id is not None:

        task = db_task[task_id]

        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        return templates.TemplateResponse("student/completions/arithmetic.html", {'request': request,
                                                                                  'class_id': class_id,
                                                                                  'arithmetic_operations': 'Уравнение',
                                                                                  'task': task.question,
                                                                                  'task_id': task_id,
                                                                                  'correct': correct,
                                                                                  'email': email})
    else:

        db_session.query(Questions).filter(Questions.end_time == None).update({'end_time': datetime.now()})
        db_session.commit()

        redirect_url = request.url_for('statistic', task_type='equations', count_correct=correct, email=email)
        return RedirectResponse(redirect_url)


@router.post('/task_selection/{email}/{class_id}/equations/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int, email: str):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'equations').all()
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
                                                   'title': 'Уравнения',
                                                   'type_task': 'equations',
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
                                                   'title': 'Уравнения',
                                                   'type_task': 'equations',
                                                   'exp': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'email': email})
    else:
        redirect_url = request.url_for('statistic', task_type='equations', count_correct=correct)
        return RedirectResponse(redirect_url)
