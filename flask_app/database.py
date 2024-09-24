from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root1111@db/db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()
