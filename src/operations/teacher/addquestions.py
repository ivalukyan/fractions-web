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
                       question: Annotated[str, Form()], url: Annotated[str, Form()] | None = None,
                       var_ans: Annotated[str, Form()] | None = None, answer: Annotated[str, Form()] = None,
                       explanation: Annotated[str, Form()] = None):
    db_session = Session()
    new_task = Task(class_student=class_student, type_task=type_task, question=question, url=url, var_ans=var_ans,
                    answer=answer, explanation=explanation)
    db_session.add(new_task)
    db_session.commit()

    return templates.TemplateResponse("home.html", {'request': request})
