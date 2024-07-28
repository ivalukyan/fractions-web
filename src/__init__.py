"""
App module
"""

from src.main import app
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.operations.student.class_selection import router as class_selection_router
from src.operations.student.task_selection import router as task_selection_router
from src.operations.teacher.addquestions import router as addquestions_router
from src.operations.student.arithmetic import router as arithmetic_router
from src.operations.student.equation import router as equation_router
from src.operations.student.statistics import router as statistics_router
from src.operations.student.task_incresed_complexity import router as task_incresed_complexity_router
from src.operations.student.text_task import router as text_task_router
from src.operations.student.mixed_tasks import router as mixed_tasks_router
from src.operations.student.geometry import router as geometry_router
from src.operations.student.count_select import router as count_select_router
from src.operations.teacher.home_teacher import router as home_teacher_router
from src.operations.student.home_user import router as home_user_router
from auth.auth import router as auth_router


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory='static'), name='static')


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