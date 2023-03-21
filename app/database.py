import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', password='24122004U',
#                                 cursor_factory=RealDictCursor)        # CONNECTION to DATABASE
#         cursor = conn.cursor()      # EXECUTOR of commands
#         print("Database connection was successful.")
#         break
#     except Exception as error:
#         print("Connecting to database fail.", error)
#         time.sleep(3)
