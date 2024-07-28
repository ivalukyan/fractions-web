from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi import Request, Form
from starlette.responses import RedirectResponse

from database.db import Task, Questions
from src.operations.student.__init__ import templates
from database.__init__ import Session

router = APIRouter(tags=['geometry'])


@router.get('/task_selection/{class_id}/geometry/{task_id}/{correct}/{count_task}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int, count_task: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'geometry').all()

        cnt_tsk = db_session.query(Questions).first()

    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')

    if len(db_task) > task_id and task_id is not None and cnt_tsk.count_task >= count_task:

        task = db_task[task_id]

        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')

        else:
            if task.url is None and task.var_ans is None:

                return templates.TemplateResponse("completions/arithmetic.html", {
                    'request': request,
                    'class_id': class_id,
                    'arithmetic_operations': 'Геометрия',
                    'task': task.question,
                    'task_id': task_id,
                    'correct': correct,
                    'count_task': count_task,
                })
            else:

                list_ans = task.var_ans.split()

                return templates.TemplateResponse("completions/geometry.html", {'request': request,
                                                                                'class_id': class_id,
                                                                                'arithmetic_operations': 'Геометрия',
                                                                                'task': task.question,
                                                                                'task_id': task_id,
                                                                                'correct': correct,
                                                                                'url': task.url,
                                                                                'list_ans': list_ans,
                                                                                'count_task': count_task})
    else:

        db_session.query(Questions).filter(Questions.end_time == None).update({'end_time': datetime.now()})
        db_session.commit()

        redirect_url = request.url_for('statistic', task_type='geometry', count_correct=correct)
        return RedirectResponse(redirect_url)


@router.post('/task_selection/{class_id}/geometry/{task_id}/{correct}/{count_task}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int, count_task: int):
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
                count_task += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'correct_answer': task.answer,
                                                   'title': 'Геометрия',
                                                   'type_task': 'geometry',
                                                   'explanation': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'count_task': count_task})
            else:
                ans = 'Неправильно'
                explanation = task.explanation
                task_id += 1
                count_task += 1
                return templates.TemplateResponse("completions/answer_page.html",
                                                  {'request': request,
                                                   'class_id': class_id,
                                                   'answer': ans,
                                                   'correct_answer': task.answer,
                                                   'title': 'Геометрия',
                                                   'type_task': 'geometry',
                                                   'exp': explanation,
                                                   'task_id': task_id,
                                                   'correct': correct,
                                                   'count_task': count_task})
    else:
        redirect_url = request.url_for('statistic', task_type='geometry', count_correct=correct)
        return RedirectResponse(redirect_url)
