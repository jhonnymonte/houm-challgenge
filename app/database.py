# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://yourusername:yourpassword@db:5432/yourdbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



TEST_DATABASE_URL = "sqlite:///:memory:"

TestingEngine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestingEngine)
Base = declarative_base()

def get_testing_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()