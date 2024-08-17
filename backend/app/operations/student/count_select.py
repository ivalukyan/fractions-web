from fastapi import Request, APIRouter

from app.operations.student.__init__ import templates

router = APIRouter(prefix='/count_selection', tags=['count task selection'])


@router.get('/{email}')
async def count_selection(request: Request, email: str):
    return templates.TemplateResponse("student/count_selection.html", {'request': request, 'email': email})
