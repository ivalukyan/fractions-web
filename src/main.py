from typing import Annotated

from django.http import HttpResponseRedirect
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from database.db import Session, Task

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory='static'), name='static')


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {'request': request})


@app.get('/class_selection')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@app.post('/class_selection')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):
    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)


@app.post('/task_selection/{class_id}')
async def task_selection(request: Request, class_id: str):
    task_id = 0
    correct = 0
    return templates.TemplateResponse("task_selection.html", {'request': request, 'class_id': class_id,
                                                              'task_id': task_id, 'correct': correct})


@app.get('/task_selection/{class_id}/arithmetic_operations/{task_id}/{correct}')
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


@app.post('/task_selection/{class_id}/arithmetic_operations/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int, correct: int):

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


@app.get('/task_selection/{class_id}/text_tasks/{task_id}/{correct}')
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


@app.post('/task_selection/{class_id}/text_tasks/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int, correct: int):

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


@app.get('/task_selection/{class_id}/equations/{task_id}/{correct}')
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


@app.post('/task_selection/{class_id}/equations/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int, correct: int):

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


@app.get('/task_selection/{class_id}/geometry/{task_id}/{correct}')
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


@app.post('/task_selection/{class_id}/geometry/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int, correct: int):

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


@app.get('/task_selection/{class_id}/task_increased_complexity/{task_id}/{correct}')
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


@app.post('/task_selection/{class_id}/task_increased_complexity/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int, correct: int):

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


@app.get('/task_selection/{class_id}/mixed_tasks/{task_id}/{correct}')
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


@app.post('/task_selection/{class_id}/mixed_tasks/{task_id}/{correct}')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()], task_id: int, correct: int):

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


@app.get('/statistic/{task_type}/count/{count_correct}')
async def statistic(request: Request, task_type: str, count_correct: int):

    try:
        db_session = Session()
        db_task = db_session.query(Task).filter(Task.type_task == task_type).all()
    except HTTPException:
        raise HTTPException(status_code=400, detail="Bad Request")

    total_count = len(db_task) - 1

    percent = count_correct * 100 / total_count

    if task_type == 'arithmetic_operation':
        return templates.TemplateResponse("statistic_page.html", {'request': request,
                                                                  'task_type': 'Арифметические задания',
                                                                  'total_count': total_count,
                                                                  'percent': percent,
                                                                  'correct_count': count_correct})
