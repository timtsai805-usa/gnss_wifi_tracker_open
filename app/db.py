
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

load_dotenv()

DB1 = os.getenv("DATABASE_URL")
DB2 = os.getenv("D2")

# Get DATABASE_URL
DATABASE_URL = DB1

# Create DB instance
if DATABASE_URL != DB1:
    engine = create_engine(
        DB2,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DB1)

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