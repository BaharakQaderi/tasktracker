"""
SQLAlchemy models for TaskTracker application.

This module defines the database models using SQLAlchemy ORM.
Models represent the structure of database tables and their relationships.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base


class Task(Base):
    """
    Task model representing a task in the task tracker.
    
    Attributes:
        id (int): Primary key, auto-incrementing task ID
        title (str): Task title/description (max 200 characters)
        completed (bool): Whether the task is completed (default: False)
        created_at (datetime): Timestamp when task was created
        updated_at (datetime): Timestamp when task was last updated
    """
    
    __tablename__ = "tasks"
    
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Unique identifier for the task"
    )
    
    title = Column(
        String(200), 
        nullable=False,
        comment="Task title or description"
    )
    
    completed = Column(
        Boolean, 
        default=False, 
        nullable=False,
        comment="Task completion status"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when task was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when task was last updated"
    )
    
    def __repr__(self):
        """String representation of the Task object."""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
    
    def __str__(self):
        """Human-readable string representation."""
        status = "✅" if self.completed else "⏳"
        return f"{status} {self.title}"
