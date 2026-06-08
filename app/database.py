from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor  
import time
from .config import settings

DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#while True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='chikodiri2667amos', cursor_factory=RealDictCursor)
#        cursor= conn.cursor()
#        print("Database connection was successful")
#        break
#    except Exception as error:
#        print("Connection to database failed")
#        print("Error: ", error) 
#       time.sleep(2)


