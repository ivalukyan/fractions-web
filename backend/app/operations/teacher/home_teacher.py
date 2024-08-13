import uuid
from typing import Annotated

from fastapi import Request, APIRouter, Form
from starlette.responses import RedirectResponse

from app.database.__init__ import Session
from app.database.db import Student, Test, Task, Teacher
from app.operations.teacher import templates
from app.operations.utils.utils import academic_performance, completed_tasks, gold_stars
from app.utils.utils import email_check, password_check, name_check, username_check, is_exist_teacher, is_exist_student

from env import Admin

from app.utils.utils import question_check, answer_check

router = APIRouter(prefix='/home_teacher', tags=['Home Teacher'])

admin = Admin()


@router.get("/{email_teacher}")
async def home_teacher(request: Request, email_teacher: str):
    academic_percent = await academic_performance(email_teacher)

    completed_task = await completed_tasks(email_teacher)

    gold_star = await gold_stars(email_teacher)

    if email_teacher in admin.username:
        db_session = Session()
        students = db_session.query(Student).all()

        return templates.TemplateResponse("teacher/home.html", {"request": request,
                                                                'data': students,
                                                                'email_teacher': email_teacher,
                                                                'academic_percent': academic_percent,
                                                                'completed_task': completed_task,
                                                                'gold_stars': gold_star})
    else:
        db_session = Session()
        students = db_session.query(Student).filter(Student.email_teacher == email_teacher).all()

        return templates.TemplateResponse("teacher/home.html", {"request": request,
                                                                'data': students,
                                                                'email_teacher': email_teacher,
                                                                'academic_percent': academic_percent,
                                                                'completed_task': completed_task,
                                                                'gold_stars': gold_star})


@router.post("/{email_teacher}")
async def home_teacher(request: Request, email_teacher: str):
    academic_percent = await academic_performance(email_teacher)

    completed_task = await completed_tasks(email_teacher)

    gold_star = await gold_stars(email_teacher)

    if email_teacher in admin.username:
        db_session = Session()
        students = db_session.query(Student).all()

        return templates.TemplateResponse("teacher/home.html", {"request": request,
                                                                'data': students,
                                                                'email_teacher': email_teacher,
                                                                'academic_percent': academic_percent,
                                                                'completed_task': completed_task,
                                                                'gold_stars': gold_star})
    else:
        db_session = Session()
        students = db_session.query(Student).filter(Student.email_teacher == email_teacher).all()

        return templates.TemplateResponse("teacher/home.html", {"request": request,
                                                                'data': students,
                                                                'email_teacher': email_teacher,
                                                                'academic_percent': academic_percent,
                                                                'completed_task': completed_task,
                                                                'gold_stars': gold_star})


@router.get("/{email_teach}/addstudent/")
async def add_student(request: Request, email_teach: str):
    return templates.TemplateResponse("teacher/addstudent.html", {"request": request, 'email_teach': email_teach})


@router.post("/{email_teach}/addstudent/")
async def add_student(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()],
                      password: Annotated[str, Form()], class_select: Annotated[str, Form()],
                      email_teacher: Annotated[str, Form()], email_teach: str):
    if email_check(email) and password_check(password) and name_check(name):
        if is_exist_student(email):

            db_session = Session()
            student = Student(name=name, email=email, password=password, email_teacher=email_teacher,
                              class_student=class_select)
            test = Test(email=email)

            db_session.add(student)
            db_session.add(test)

            db_session.commit()

            redirect_url = request.url_for("home_teacher", email_teacher=email_teach)
            return RedirectResponse(redirect_url)
        else:
            return templates.TemplateResponse("teacher/addstudent.html",
                                              {'request': request, 'email_teach': email_teach})
    else:
        return templates.TemplateResponse("teacher/addstudent.html", {'request': request, 'email_teach': email_teach})


@router.get("/{email_teacher}/deletestudent/")
async def delete_student(request: Request, email_teacher: str):
    return templates.TemplateResponse("teacher/delstudent.html", {"request": request, 'email_teacher': email_teacher})


@router.post("/{email_teacher}/deletestudent/")
async def delete_student(request: Request, email_delete: Annotated[str, Form()], email_teacher: str):
    if email_check(email_delete):
        if is_exist_teacher(email_delete):
            return templates.TemplateResponse("teacher/delstudent.html",
                                              {'request': request, 'email_teacher': email_teacher})
        else:
            db_session = Session()
            student = db_session.query(Student).filter_by(email=email_delete).first()
            db_session.delete(student)
            db_session.commit()

            redirect_url = request.url_for("home_teacher", email_teacher=email_teacher)
            return RedirectResponse(redirect_url)
    else:
        return templates.TemplateResponse("teacher/delteacher.html",
                                          {'request': request, 'email_teacher': email_teacher})


@router.get("/viewquestions/{email}")
async def view_questions(request: Request, email: str):
    db_session = Session()
    data = db_session.query(Task).all()

    return templates.TemplateResponse("teacher/viewquestions.html", {"request": request, 'email_teacher': email,
                                                                     'data': data})


@router.get("/viewteachers/{email}")
async def view_teachers(request: Request, email: str):
    db_session = Session()
    teacher = db_session.query(Teacher).all()

    return templates.TemplateResponse('teacher/viewteachers.html', {"request": request, 'email_teacher': email,
                                                                    'data': teacher})


@router.get("/addnewteacher/{email}")
async def add_teacher(request: Request, email: str):
    return templates.TemplateResponse('teacher/addnewteacher.html', {"request": request, 'email_teacher': email})


@router.post("/addnewteacher/{email_teacher}")
async def add_teacher(request: Request, email_teacher: str, username: Annotated[str, Form()],
                      email: Annotated[str, Form()], password: Annotated[str, Form()],
                      is_superuser: Annotated[bool, Form()]):
    if email_check(email) and password_check(password) and username_check(username):
        if is_exist_teacher(email):

            db_session = Session()
            teacher = Teacher(name=username, email=email, password=password, is_superuser=is_superuser)
            db_session.add(teacher)
            db_session.commit()

            redirect_url = request.url_for("home_teacher", email_teacher=email_teacher)
            return RedirectResponse(redirect_url)
        else:
            return templates.TemplateResponse("teacher/addnewteacher.html",
                                              {'request': request, 'email_teacher': email})
    else:
        return templates.TemplateResponse("teacher/addnewteacher.html", {'request': request, 'email_teacher': email})


@router.get("/addquestions/{email}")
async def addquestions(request: Request, email: str):
    return templates.TemplateResponse("teacher/addquestions.html", {'request': request, 'email': email})


@router.post("/addquestions/{email}")
async def addquestions(request: Request, email: str, class_student: Annotated[str, Form()],
                       type_task: Annotated[str, Form()],
                       question: Annotated[str, Form()], url: Annotated[str, Form()] | None = "",
                       var_ans: Annotated[str, Form()] | None = "", answer: Annotated[str, Form()] = "",
                       explanation: Annotated[str, Form()] = ""):
    if question_check(question) and answer_check(var_ans) and answer_check(answer) and question_check(explanation):

        db_session = Session()
        new_task = Task(class_student=class_student, type_task=type_task, question=question, url=url, var_ans=var_ans,
                        answer=answer, explanation=explanation)
        db_session.add(new_task)
        db_session.commit()

        data = db_session.query(Task).all()

        return templates.TemplateResponse("teacher/viewquestions.html", {'request': request,
                                                                         'email_teacher': email,
                                                                         'data': data})
    else:
        return templates.TemplateResponse("teacher/addquestions.html", {'request': request, 'email': email})


@router.get("/delquestions/{email}/{id}")
async def delete_question(request: Request, email: str, id: str):
    db_session = Session()
    question = db_session.query(Task).filter(Task.id == id).first()
    db_session.delete(question)
    db_session.commit()
    data = db_session.query(Task).all()

    return templates.TemplateResponse("teacher/viewquestions.html", {'request': request, 'email_teacher': email,
                                                                     'data': data})


@router.get("/refactor/{email}/{id}")
async def refactoring_question(request: Request, email: str, id: str):
    db_session = Session()
    task = db_session.query(Task).filter(Task.id == id).first()

    return templates.TemplateResponse("teacher/refactorquestion.html", {'request': request, 'email': email,
                                                                        'id': id, 'task': task})


@router.post("/refactor/{email}/{id}")
async def refactoring_question(request: Request, email: str, id: str,
                               question: Annotated[str, Form()], url: Annotated[str, Form()] | None = "",
                               var_ans: Annotated[str, Form()] | None = "", answer: Annotated[str, Form()] = "",
                               explanation: Annotated[str, Form()] = ""):
    db_session = Session()
    db_session.query(Task).filter(Task.id == id).update({'question': question,
                                                         'url': url,
                                                         'var_ans': var_ans,
                                                         'answer': answer,
                                                         'explanation': explanation})
    db_session.commit()

    data = db_session.query(Task).all()

    return templates.TemplateResponse("teacher/viewquestions.html", {'request': request,
                                                                     'email_teacher': email,
                                                                     'data': data})


@router.get("/refactorstudent/{email}/{id}")
async def refactoring_student(request: Request, email: str, id: str):
    db_session = Session()
    student = db_session.query(Student).filter(Student.id == id).first()

    return templates.TemplateResponse("teacher/refactorstudent.html", {'request': request,
                                                                       'email': email,
                                                                       'id': id,
                                                                       'student': student})


@router.post("/refactorstudent/{email}/{id}")
async def refactoring_student(request: Request, email: str, id: str, name: Annotated[str, Form()],
                              email_student: Annotated[str, Form()],
                              password: Annotated[str, Form()], class_select: Annotated[str, Form()],
                              email_teacher: Annotated[str, Form()]):

    db_session = Session()
    db_session.query(Student).filter(Student.id == id).update({'name': name,
                                                               'email': email_student,
                                                               'password': password,
                                                               'class_student': class_select,
                                                               'email_teacher': email_teacher})
    db_session.commit()

    redirect_url = request.url_for("home_teacher", email_teacher=email)
    return RedirectResponse(redirect_url)
