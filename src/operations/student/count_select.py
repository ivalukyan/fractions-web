from fastapi import Request, APIRouter

from src.operations.student.__init__ import templates

router = APIRouter(prefix='/count_selection', tags=['count task selection'])


@router.get('/')
async def count_selection(request: Request):
    return templates.TemplateResponse("count_selection.html", {'request': request})
