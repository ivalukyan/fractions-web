from typing import Annotated


from fastapi import Request, Form, APIRouter

from app.database.db import Task
from app.database.__init__ import Session

from app.operations.teacher.__init__ import templates

router = APIRouter(prefix='/addquestions', tags=['addquestions'])


@router.get("/{email}")
async def addquestions(request: Request, email: str):
    return templates.TemplateResponse("teacher/addquestions.html", {'request': request, 'email': email})


@router.post("/{email}")
async def addquestions(request: Request, email: str, class_student: Annotated[str, Form()], type_task: Annotated[str, Form()],
                       question: Annotated[str, Form()], url: Annotated[str, Form()] | None = None,
                       var_ans: Annotated[str, Form()] | None = None, answer: Annotated[str, Form()] = None,
                       explanation: Annotated[str, Form()] = None):
    db_session = Session()
    new_task = Task(class_student=class_student, type_task=type_task, question=question, url=url, var_ans=var_ans,
                    answer=answer, explanation=explanation)
    db_session.add(new_task)
    db_session.commit()

    return templates.TemplateResponse("teacher/home.html", {'request': request, 'email_teacher': email})
