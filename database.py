import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Debugging: Print the DATABASE_URL to check if it is loaded correctly
print("DATABASE_URL:", DATABASE_URL)

# Ensure the database URL is correct
if not DATABASE_URL or "postgresql" not in DATABASE_URL:
    raise ValueError("Invalid DATABASE_URL. Check your .env file.")

# Create database engine
engine = create_engine(DATABASE_URL)

# ORM session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()
