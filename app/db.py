
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

load_dotenv()
AWS_RDS_URL = os.getenv("AWS_RDS_URL")
SQLITE_URL = os.getenv("SQLITE_URL")

# Get DATABASE_URL
DATABASE_URL = AWS_RDS_URL

# Create DB instance
if DATABASE_URL.startswith("SQLITE"):
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(AWS_RDS_URL)


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