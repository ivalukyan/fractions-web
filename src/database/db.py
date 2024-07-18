from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from env import Postgres

Base = declarative_base()

postgres = Postgres()

engine = create_engine(f'postgresql://{postgres.user}:{postgres.password}@{postgres.host}/{postgres.db}')
Session = sessionmaker(bind=engine)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    class_student = Column(String, nullable=True)
    type_task = Column(String, nullable=True)
    question = Column(String, nullable=True)
    answer = Column(String, nullable=True)
    explanation = Column(String, nullable=True)


Base.metadata.create_all(engine)
