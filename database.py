from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

DB_URL = f'mysql://{os.environ["_USERNAME"]}:{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/{os.environ["DATABASE"]}'

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
