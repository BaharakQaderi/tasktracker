"""
Database configuration and session management for TaskTracker.

This module handles:
- Database connection setup
- SQLAlchemy engine configuration
- Session management for database operations
- Database URL configuration from environment variables
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variable or default for development
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost:5432/tasktracker"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    # Connection pool settings for better performance
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    echo=False  # Set to True for SQL query logging in development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session.
    
    This function is used with FastAPI's dependency injection system.
    It ensures that database sessions are properly created and closed.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/tasks")
        def get_tasks(db: Session = Depends(get_db)):
            return crud.get_tasks(db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables.
    
    This function should be called when the application starts
    to ensure all tables exist in the database.
    """
    Base.metadata.create_all(bind=engine)
