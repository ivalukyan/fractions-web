from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, UUID, Boolean

from database.__init__ import Base, engine


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID, primary_key=True, default=uuid4)
    class_student = Column(String, nullable=True)
    type_task = Column(String, nullable=True)
    question = Column(String, nullable=True)
    url = Column(String, nullable=True)
    var_ans = Column(String, nullable=True)
    answer = Column(String, nullable=True)
    explanation = Column(String, nullable=True)


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(UUID, primary_key=True, default=uuid4)
    count_task = Column(Integer, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)


class Student(Base):
    __tablename__ = 'students'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    class_student = Column(String, nullable=True)
    percent = Column(Integer, nullable=True, default=0)
    all_times_tasks = Column(Integer, nullable=True, default=0)
    all_is_correct = Column(Integer, nullable=True, default=0)
    all_is_uncorrect = Column(Integer, nullable=True, default=0)
    count_bronze = Column(Integer, nullable=True, default=0)
    count_silver = Column(Integer, nullable=True, default=0)
    count_gold = Column(Integer, nullable=True, default=0)
    email_teacher = Column(String, nullable=False)


class Test(Base):
    __tablename__ = 'tests'
    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, nullable=False)
    type_task = Column(String, nullable=True)
    count_task = Column(Integer, nullable=True, default=0)
    is_correct = Column(Integer, nullable=True, default=0)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(engine)
