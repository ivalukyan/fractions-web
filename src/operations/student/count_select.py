from typing import Annotated

from fastapi import Request, Form, APIRouter
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

router = APIRouter(prefix='/count_selection', tags=['count task selection'])

templates = Jinja2Templates(directory="templates")


@router.get('/')
async def count_selection(request: Request):
    return templates.TemplateResponse("count_selection.html", {'request': request})
