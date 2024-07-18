from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

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
    return templates.TemplateResponse("task_selection.html", {'request': request, 'class_id': class_id})


@app.get('/task_selection/{class_id}/arithmetic_operations')
async def arithmetic_operations(request: Request, class_id: str):
    return templates.TemplateResponse("completions/arithmetic.html", {'request': request, 'class_id': class_id,
                                                                      'arithmetic_operations': 'Арифметические задания'})


@app.post('/task_selection/{class_id}/arithmetic_operations')
async def arithmetic_operations(request: Request, class_id: str, answer: Annotated[str, Form()]):
    if answer == '1':
        ans = 'Правильно'
        explanation = ''
        return templates.TemplateResponse("completions/answer_page.html",
                                          {'request': request,
                                           'class_id': class_id,
                                           'answer': ans,
                                           'arithmetic_operations': 'Арифметические задания',
                                           'explanation': explanation})
    else:
        ans = 'Неправильно'
        explanation = 'Правильный ответ - 7/10, потому что..'
        return templates.TemplateResponse("completions/answer_page.html",
                                          {'request': request,
                                           'class_id': class_id,
                                           'answer': ans,
                                           'arithmetic_operations': 'Арифметические задания',
                                           'exp': explanation})


@app.get('/task_selection/{class_id}/text_tasks')
async def arithmetic_operations(request: Request, class_id: str):
    return templates.TemplateResponse("completions/arithmetic.html", {'request': request, 'class_id': class_id})


@app.get('/task_selection/{class_id}/equations')
async def arithmetic_operations(request: Request, class_id: str):
    return templates.TemplateResponse("completions/arithmetic.html", {'request': request, 'class_id': class_id})


@app.get('/task_selection/{class_id}/geometry')
async def arithmetic_operations(request: Request, class_id: str):
    return templates.TemplateResponse("completions/geometry.html", {'request': request, 'class_id': class_id})


@app.get('/task_selection/{class_id}/task_increased_complexity')
async def arithmetic_operations(request: Request, class_id: str):
    return templates.TemplateResponse("completions/arithmetic.html", {'request': request, 'class_id': class_id})


@app.get('/task_selection/{class_id}/mixed_tasks')
async def arithmetic_operations(request: Request, class_id: str):
    return templates.TemplateResponse("completions/arithmetic.html", {'request': request, 'class_id': class_id})
