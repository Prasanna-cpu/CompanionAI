import os
import sqlmodel
from sqlmodel import SQLModel

DATABASE_URL = os.environ["DATABASE_URL"]

if not DATABASE_URL or DATABASE_URL == "":
    raise ValueError("DATABASE_URL is not set")

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)

def get_session():
    with sqlmodel.Session(engine) as session:
        yield session



