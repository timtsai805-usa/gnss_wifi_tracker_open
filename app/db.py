
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

load_dotenv()
AWS_RDS = os.getenv("AWS_RDS_URL")
POSTGRES = os.getenv("POSTGRES_URL")
SQLITE = os.getenv("SQLITE_URL")


# Get DATABASE_URL
DATABASE_URL = AWS_RDS

# Create DB instance
if DATABASE_URL == SQLITE:
    engine = create_engine(
        SQLITE,
        connect_args={"check_same_thread": False}
    )
elif DATABASE_URL == POSTGRES:
    engine = create_engine(POSTGRES)

elif DATABASE_URL == AWS_RDS:
    engine = create_engine(AWS_RDS)


# Create DB session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Define table Obj
Base = declarative_base()

## Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]