from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory='static'), name='static')


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {'request': request})


@app.get("/class_selection")
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


# @app.post("/class_selection")
# async def class_selection_form(request: Request, class_id: Annotated[str, Form()]):
#     return templates.TemplateResponse('task_selection.html', {'request': request, 'class_id': class_id})
#
#
# @app.get("/task_selection/{class_id}")
# async def task_selection(request: Request):
#     return templates.TemplateResponse('task_selection.html', {'request': request})
