from typing import Annotated

from fastapi import Request, Form, APIRouter
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

router = APIRouter(prefix='/class_selection', tags=['class selection'])

templates = Jinja2Templates(directory="templates")


@router.get('/')
async def class_selection(request: Request):
    return templates.TemplateResponse("class_selection.html", {'request': request})


@router.post('/')
async def class_selection(request: Request, class_id: Annotated[str, Form()]):
    redirect_url = request.url_for("task_selection", class_id=class_id)
    return RedirectResponse(redirect_url)
