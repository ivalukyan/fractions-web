"""
Database module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from env import Postgres


Base = declarative_base()

postgres = Postgres()

engine = create_engine(f'postgresql://{postgres.user}:{postgres.password}@{postgres.host}/{postgres.db}')
Session = sessionmaker(bind=engine)
