
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

import os

# Database url
DATABASE_URL = os.getenv("DATABASE_URL")

# Create DB instance
engine = create_engine(DATABASE_URL)

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