from sqlalchemy import create_engine, Column, Integer, String, DateTime, UUID, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.env import Postgres

from uuid import uuid4

Base = declarative_base()

postgres = Postgres()

engine = create_engine(f'postgresql://{postgres.user}:{postgres.password}@{postgres.host}/{postgres.db}')
Session = sessionmaker(bind=engine)


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
    all_times_tasks = Column(Integer, nullable=True)
    all_is_correct = Column(Integer, nullable=True)
    all_is_uncorrect = Column(Integer, nullable=True)
    count_bronze = Column(Integer, nullable=True)
    count_silver = Column(Integer, nullable=True)
    count_gold = Column(Integer, nullable=True)
    email_teacher = Column(String, nullable=False)


class Test(Base):
    __tablename__ = 'tests'
    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, nullable=False)
    type_task = Column(String, nullable=True)
    count_task = Column(Integer, nullable=True)
    is_correct = Column(Integer, nullable=True)


Base.metadata.create_all(engine)
