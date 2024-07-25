"""
Models
"""

from pydantic import BaseModel


class TasksSchema(BaseModel):
    id: int
    class_student: str | None = None
    type_task: str | None = None
    question: str | None = None
    url: str | None = None
    var_ans: str | None = None
    answer: str | None = None
    explanation: str | None = None

