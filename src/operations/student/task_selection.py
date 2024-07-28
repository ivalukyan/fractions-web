from datetime import datetime

from fastapi import Request, APIRouter
from starlette.templating import Jinja2Templates

from database.db import Questions
from database.__init__ import Session

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix='/task_selection', tags=['task selection'])


@router.post('/{class_id}')
async def task_selection(request: Request, class_id: str):
    task_id = 0
    correct = 0
    count_task = 0

    db_session = Session()
    db_session.query(Questions).filter(Questions.start_time == None).update({'start_time': datetime.now()})
    db_session.commit()

    return templates.TemplateResponse("task_selection.html", {'request': request, 'class_id': class_id,
                                                              'task_id': task_id, 'correct': correct,
                                                              'count_task': count_task})
