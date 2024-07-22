from typing import Annotated

from starlette.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter

from database.db import Session, Task

router = APIRouter(prefix='/addquestions', tags=['addquestions'])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def addquestions(request: Request):
    return templates.TemplateResponse("addquestions.html", {'request': request})


@router.post("/")
async def addquestions(request: Request, class_student: Annotated[str, Form()], type_task: Annotated[str, Form()],
                       question: Annotated[str, Form()], answer: Annotated[str, Form()],
                       explanation: Annotated[str, Form()]):
    db_session = Session()
    new_task = Task(class_student=class_student, type_task=type_task, question=question,
                    answer=answer, explanation=explanation)
    db_session.add(new_task)
    db_session.commit()

    return templates.TemplateResponse("home.html", {'request': request})
