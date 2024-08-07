"""
Models
"""
import uuid

from fastapi import Form
from pydantic import BaseModel
from typing import Annotated


class TasksSchema(BaseModel):
    id: int
    class_student: str | None = None
    type_task: str | None = None
    question: str | None = None
    url: str | None = None
    var_ans: str | None = None
    answer: str | None = None
    explanation: str | None = None


class StudentSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    password: str
    class_student: str | None = None
    all_times_tasks: int | None = None
    all_is_correct: int | None = None
    all_is_uncorrect: int | None = None
    count_bronze: int | None = None
    count_silver: int | None = None
    count_gold: int | None = None


class AddStudentSchema(BaseModel):
    name: Annotated[str, Form()]
    email: Annotated[str, Form()]
    password: Annotated[str, Form()]
    class_select: Annotated[str, Form()]
    email_teacher: Annotated[str, Form()]
