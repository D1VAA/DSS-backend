from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv

load_dotenv("./src/.env")
database_url = os.getenv("DATABASE_URL")

assert database_url is not None, "DATABASE_URL environment variable not set"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Routes(Base):
    __tablename__ = "routes"
    id = Column(String, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    distance = Column(Float)

Base.metadata.create_all(bind=engine)

# Dependecy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()