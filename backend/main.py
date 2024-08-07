import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.operations.auth.auth import router as auth_router
from app.operations.student.arithmetic import router as arithmetic_router
from app.operations.student.class_selection import router as class_selection_router
from app.operations.student.count_select import router as count_select_router
from app.operations.student.equation import router as equation_router
from app.operations.student.geometry import router as geometry_router
from app.operations.student.home_user import router as home_user_router
from app.operations.student.mixed_tasks import router as mixed_tasks_router
from app.operations.student.statistics import router as statistics_router
from app.operations.student.task_incresed_complexity import router as task_incresed_complexity_router
from app.operations.student.task_selection import router as task_selection_router
from app.operations.student.text_task import router as text_task_router
from app.operations.teacher.addquestions import router as addquestions_router
from app.operations.teacher.home_teacher import router as home_teacher_router

app = FastAPI(
    title="Fractions Web API"
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory='app/static'), name='static')

app.include_router(class_selection_router)
app.include_router(task_selection_router)
app.include_router(addquestions_router)
app.include_router(arithmetic_router)
app.include_router(equation_router)
app.include_router(statistics_router)
app.include_router(task_incresed_complexity_router)
app.include_router(text_task_router)
app.include_router(mixed_tasks_router)
app.include_router(geometry_router)
app.include_router(count_select_router)
app.include_router(home_teacher_router)
app.include_router(home_user_router)
app.include_router(auth_router)


from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="app/templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("exception_handler/404.html", {"request": request})

@app.exception_handler(500)
async def custom_500_handler(request, __):
    return templates.TemplateResponse("exception_handler/500.html", {"request": request})

@app.exception_handler(400)
async def custom_400_handler(request, __):
    return templates.TemplateResponse("exception_handler/400.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000, workers=1, log_level='info')
