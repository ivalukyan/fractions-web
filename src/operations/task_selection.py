from datetime import datetime

from fastapi import Request, APIRouter
from starlette.templating import Jinja2Templates

from database.db import Questions, Session

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix='/task_selection', tags=['task_selection'])


@router.post('/{class_id}')
async def task_selection(request: Request, class_id: str):
    task_id = 0
    correct = 0

    db_session = Session()
    new_question = Questions(start_time=datetime.now())
    db_session.add(new_question)
    db_session.commit()

    return templates.TemplateResponse("task_selection.html", {'request': request, 'class_id': class_id,
                                                              'task_id': task_id, 'correct': correct})
