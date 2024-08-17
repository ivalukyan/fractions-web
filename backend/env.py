import os
from dotenv import load_dotenv


load_dotenv()


class Postgres:
    def __init__(self):

        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.db = os.getenv("POSTGRES_DB")


class Admin:
    def __init__(self):
        self.username = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
