"""
Models
"""

from pydantic import BaseModel


class TasksSchema(BaseModel):
    id: int
    class_student: str | None = None
    type_task: str | None = None
    question: str | None = None
    answer: str | None = None

