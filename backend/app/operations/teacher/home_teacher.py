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

from app.utils.utils import question_check, answer_check, hashed, equal_password, is_superuser

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


@router.get("/addstudent/{email_teach}")
async def add_student(request: Request, email_teach: str):
    return templates.TemplateResponse("teacher/addstudent.html", {"request": request, 'email_teach': email_teach})


@router.post("/addstudent/{email_teach}")
async def add_student(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()],
                      password: Annotated[str, Form()], class_select: Annotated[str, Form()],
                      email_teacher: Annotated[str, Form()], email_teach: str):
    if email_check(email) and name_check(name):
        if is_exist_student(email):
            exp = "Пользователь уже существует!"
            return templates.TemplateResponse("teacher/addstudent.html",
                                              {'request': request, 'email_teach': email_teach, 'exp': exp})
        else:
            hashandsalt = hashed(password)
            db_session = Session()
            student = Student(name=name, email=email, password=hashandsalt, email_teacher=email_teacher,
                              class_student=class_select)
            test = Test(email=email)

            db_session.add(student)
            db_session.add(test)

            db_session.commit()

            redirect_url = request.url_for("home_teacher", email_teacher=email_teach)
            return RedirectResponse(redirect_url)
    else:
        exp = "Данные введены некорректно!"
        return templates.TemplateResponse("teacher/addstudent.html", {'request': request, 'email_teach': email_teach,
                                                                      'exp': exp})


@router.get("/deletestudent/{email_teacher}")
async def delete_student(request: Request, email_teacher: str):
    return templates.TemplateResponse("teacher/delstudent.html", {"request": request, 'email_teacher': email_teacher})


@router.post("/deletestudent/{email_teacher}")
async def delete_student(request: Request, email_delete: Annotated[str, Form()], email_teacher: str):
    if email_check(email_delete):
        if is_exist_teacher(email_delete):
            db_session = Session()
            student = db_session.query(Student).filter(Student.email == email_delete).first()
            test = db_session.query(Test).filter(Test.email == email_delete).first()
            db_session.delete(student)
            db_session.delete(test)
            db_session.commit()

            redirect_url = request.url_for("home_teacher", email_teacher=email_teacher)
            return RedirectResponse(redirect_url)
        else:
            exp = "Пользователь не существует!"
            return templates.TemplateResponse("teacher/delstudent.html",
                                              {'request': request, 'email_teacher': email_teacher, 'exp': exp})
    else:
        exp = "Данные введены некорректно!"
        return templates.TemplateResponse("teacher/delteacher.html",
                                          {'request': request, 'email_teacher': email_teacher, 'exp': exp})


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


@router.post("/viewteachers/{email}")
async def view_teachers(request: Request, email: str):
    db_session = Session()
    teacher = db_session.query(Teacher).all()

    return templates.TemplateResponse("teacher/viewteachers.html", {'request': request,
                                                                    'email_teacher': email,
                                                                    'data': teacher})


@router.get("/addnewteacher/{email}")
async def add_teacher(request: Request, email: str):
    if is_superuser(email) or email == admin.username:
        return templates.TemplateResponse('teacher/addnewteacher.html', {"request": request, 'email_teacher': email})
    else:
        redirect_url = request.url_for("view_teachers", email=email)
        return RedirectResponse(redirect_url)


@router.post("/addnewteacher/{email_teacher}")
async def add_teacher(request: Request, email_teacher: str, name: Annotated[str, Form()],
                      email: Annotated[str, Form()], password: Annotated[str, Form()],
                      is_superuser: Annotated[bool, Form()]):
    if email_check(email) and name_check(name):
        if is_exist_teacher(email):
            exp = "Пользователь уже существует"
            return templates.TemplateResponse("teacher/addnewteacher.html",
                                              {'request': request, 'email_teacher': email,
                                               'exp': exp})
        else:
            hashandsalt = hashed(password)

            db_session = Session()
            teacher = Teacher(name=name, email=email, password=hashandsalt, is_superuser=is_superuser)
            db_session.add(teacher)
            db_session.commit()

            redirect_url = request.url_for("view_teachers", email=email_teacher)
            return RedirectResponse(redirect_url)
    else:
        exp = "Данные введены некорректно!"
        return templates.TemplateResponse("teacher/addnewteacher.html", {'request': request, 'email_teacher': email_teacher,
                                                                         'exp': exp})


@router.get("/addquestions/{email}")
async def addquestions(request: Request, email: str):
    return templates.TemplateResponse("teacher/addquestions.html", {'request': request, 'email': email})


@router.post("/addquestions/{email}")
async def addquestions(request: Request, email: str, class_student: Annotated[str, Form()],
                       type_task: Annotated[str, Form()],
                       question: Annotated[str, Form()], url: Annotated[str, Form()] = " ",
                       variation_answer: Annotated[str, Form()] = " ", answer: Annotated[str, Form()] = "",
                       explanation: Annotated[str, Form()] = ""):
    if question_check(question) and answer_check(variation_answer) and answer_check(answer) and question_check(explanation):

        db_session = Session()
        new_task = Task(class_student=class_student, type_task=type_task, question=question, url=url, var_ans=variation_answer,
                        answer=answer, explanation=explanation)
        db_session.add(new_task)
        db_session.commit()

        data = db_session.query(Task).all()

        return templates.TemplateResponse("teacher/viewquestions.html", {'request': request,
                                                                         'email_teacher': email,
                                                                         'data': data})
    else:
        exp = "Данные введены некорректно!"
        print(variation_answer)
        return templates.TemplateResponse("teacher/addquestions.html", {'request': request, 'email': email, 'exp': exp})


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
    if question_check(question) and answer_check(var_ans) and answer_check(answer) and question_check(explanation):
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
    else:
        exp = "Данные введены некорректно!"
        db_session = Session()
        task = db_session.query(Task).filter(Task.id == id).first()
        return templates.TemplateResponse("teacher/refractorquestion.html", {'request': request,
                                                                             'email': email, 'id': id, 'task': task,
                                                                             'exp': exp})


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
                              password: Annotated[str, Form()],
                              email_teacher: Annotated[str, Form()]):
    if name_check(name) and email_check(email_student) and password_check(password):

        hashandsalt = hashed(password)
        db_session = Session()
        db_session.query(Student).filter(Student.id == id).update({'name': name,
                                                                   'email': email_student,
                                                                   'password': hashandsalt,
                                                                   'email_teacher': email_teacher})
        db_session.commit()

        redirect_url = request.url_for("home_teacher", email_teacher=email)
        return RedirectResponse(redirect_url)
    else:
        exp = "Данные введены некорректно!"
        db_session = Session()
        student = db_session.query(Student).filter(Student.id == id).first()
        return templates.TemplateResponse("teacher/refactorstudent.html", {'request': request,
                                                                           'email': email,
                                                                           'id': id,
                                                                           'student': student,
                                                                           'exp': exp})


@router.get("/delteacher/{email}/{id}")
async def delete_teacher(request: Request, email: str, id: str):

    if is_superuser(email) or email == admin.username:
        db_session = Session()
        teacher = db_session.query(Teacher).filter(Teacher.id == id).first()
        db_session.delete(teacher)
        db_session.commit()

        redirect_url = request.url_for("view_teachers", email=email)
        return RedirectResponse(redirect_url)
    else:
        redirect_url = request.url_for("view_teachers", email=email)
        return RedirectResponse(redirect_url)


@router.get("/refactorteacher/{email}/{id}")
async def refactoring_teacher(request: Request, email: str, id: str):
    db_session = Session()
    teacher = db_session.query(Teacher).filter(Teacher.id == id).first()

    if is_superuser(email) or email == admin.username:

        return templates.TemplateResponse("teacher/refactorteacher.html", {'request': request,
                                                                       'email': email,
                                                                       'id': id,
                                                                       'teacher': teacher})
    else:
        redirect_url = request.url_for("view_teachers", email=email)
        return RedirectResponse(redirect_url)


@router.post("/refactorteacher/{email}/{id}")
async def refactoring_teacher(request: Request, email: str, id: str, name: Annotated[str, Form()],
                              teacher_email: Annotated[str, Form()], password: Annotated[str, Form()]):
    if name_check(name) and email_check(teacher_email) and password_check(password):

        hasandsalt = hashed(password)
        db_session = Session()
        db_session.query(Teacher).filter(Teacher.id == id).update({'name': name,
                                                                   'email': teacher_email,
                                                                   'password': hasandsalt})
        db_session.commit()

        teacher = db_session.query(Teacher).all()

        return templates.TemplateResponse('teacher/viewteachers.html', {"request": request, 'email_teacher': email,
                                                                        'data': teacher})
    else:
        exp = "Данные введены некорретно!"
        db_session = Session()
        teacher = db_session.query(Teacher).filter(Teacher.id == id).first()
        return templates.TemplateResponse("teacher/refactorteacher.html", {'request': request,
                                                                           'email': email,
                                                                           'id': id,
                                                                           'teacher': teacher,
                                                                           'exp': exp})
