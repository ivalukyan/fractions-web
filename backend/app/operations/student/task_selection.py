from datetime import datetime

from fastapi import Request, APIRouter
from starlette.templating import Jinja2Templates

from app.database.db import Questions
from app.database.__init__ import Session

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix='/task_selection', tags=['task selection'])


@router.post('/{email}/{class_id}')
async def task_selection(request: Request, class_id: str, email: str):
    task_id = 0
    correct = 0
    count_task = 0

    db_session = Session()
    db_session.query(Questions).filter(Questions.email == email).update({'start_time': datetime.now()})
    db_session.commit()

    return templates.TemplateResponse("student/task_selection.html", {'request': request, 'class_id': class_id,
                                                                      'task_id': task_id, 'correct': correct,
                                                                      'count_task': count_task,
                                                                      'email': email})
