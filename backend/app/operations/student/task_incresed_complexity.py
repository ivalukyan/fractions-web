from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, Form, Request, APIRouter
from starlette.responses import RedirectResponse

from app.database.__init__ import Session
from app.database.db import Questions, Task, Student
from app.operations.student.__init__ import templates
from app.utils.utils import answer_check

router = APIRouter(tags=['task incresed complexity'])


@router.get('/task_selection/{email}/{class_id}/task_increased_complexity/{task_id}/{correct}/{count_task}')
async def arithmetic_operations(request: Request, class_id: str, task_id: int, correct: int, email: str,
                                count_task: int):
    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'task_increased_complexity').all()
    except HTTPException:
        raise HTTPException(status_code=400, detail='Bad Request')

    if len(db_task) > task_id and task_id is not None:

        task = db_task[task_id]

        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        return templates.TemplateResponse("student/completions/arithmetic.html", {'request': request,
                                                                                  'class_id': class_id,
                                                                                  'arithmetic_operations': 'Задачи повышенной '
                                                                                                           'сложности',
                                                                                  'task': task.question,
                                                                                  'task_id': task_id,
                                                                                  'correct': correct,
                                                                                  'count_task': count_task,
                                                                                  'email': email})
    else:

        db_session.query(Questions).filter(Questions.end_time == None).update({'end_time': datetime.now()})
        db_session.commit()

        student = db_session.query(Student).filter(Student.email == email).first()
        if student is not None:

            cnt_all_tsk = student.all_times_tasks + count_task
            cnt_correct = student.all_is_correct + correct

            percent = round(cnt_correct/cnt_all_tsk * 100)

            db_session.query(Student).filter(Student.email == email).update({'all_times_tasks': cnt_all_tsk,
                                                                             'all_is_correct': cnt_correct,
                                                                             'percent': percent})
            db_session.commit()

        redirect_url = request.url_for('statistic', task_type='task_increased_complexity', count_correct=correct,
                                       email=email)
        return RedirectResponse(redirect_url)


@router.post('/task_selection/{email}/{class_id}/task_increased_complexity/{task_id}/{correct}/{count_task}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int,
                                correct: int, email: str, count_task: int):
    if answer_check(answer):

        try:
            db_session = Session()
            db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                    Task.type_task == 'task_increased_complexity').all()
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
                    return templates.TemplateResponse("student/completions/answer_page.html",
                                                      {'request': request,
                                                       'class_id': class_id,
                                                       'is_correct': is_correct,
                                                       'answer': answer,
                                                       'correct_answer': task.answer,
                                                       'title': 'Задания повышенной сложности',
                                                       'type_task': 'task_increased_complexity',
                                                       'explanation': explanation,
                                                       'task_id': task_id,
                                                       'correct': correct,
                                                       'count_task': count_task,
                                                       'email': email})
                else:
                    is_correct = 'Неправильно'
                    explanation = task.explanation
                    task_id += 1
                    count_task += 1
                    return templates.TemplateResponse("student/completions/answer_page.html",
                                                      {'request': request,
                                                       'class_id': class_id,
                                                       'is_correct': is_correct,
                                                       'answer': answer,
                                                       'correct_answer': task.answer,
                                                       'title': 'Задания повышенной сложности',
                                                       'type_task': 'task_increased_complexity',
                                                       'exp': explanation,
                                                       'task_id': task_id,
                                                       'correct': correct,
                                                       'count_task': count_task,
                                                       'email': email})
        else:
            redirect_url = request.url_for('statistic', task_type='task_increased_complexity', count_correct=correct)
            return RedirectResponse(redirect_url)
    else:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.class_student == class_id,
                                                Task.type_task == 'task_increased_complexity').all()

        task = db_task[task_id]

        return templates.TemplateResponse("student/completions/arithmetic.html", {'request': request,
                                                                                  'class_id': class_id,
                                                                                  'arithmetic_operations': 'Задачи повышенной сложности',
                                                                                  'task': task.question,
                                                                                  'task_id': task_id,
                                                                                  'correct': correct,
                                                                                  'count_task': count_task,
                                                                                  'email': email})
