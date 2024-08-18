"""
Database module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from env import Postgres


Base = declarative_base()

postgres = Postgres()

db_url = f"postgresql://{postgres.user}:{postgres.password}@{postgres.host}/{postgres.db}"

engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)

# engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
