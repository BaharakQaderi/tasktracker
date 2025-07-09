"""
CRUD operations for TaskTracker application.

This module contains all database operations (Create, Read, Update, Delete)
for tasks. It acts as the repository layer, separating business logic
from database implementation details.
"""

from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """
    Retrieve a single task by ID.
    
    Args:
        db: Database session
        task_id: ID of the task to retrieve
        
    Returns:
        Task object if found, None otherwise
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    completed: Optional[bool] = None
) -> List[models.Task]:
    """
    Retrieve a list of tasks with pagination and optional filtering.
    
    Args:
        db: Database session
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return
        completed: Filter by completion status (None = all tasks)
        
    Returns:
        List of Task objects
    """
    query = db.query(models.Task)
    
    # Apply completion filter if specified
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    
    # Apply pagination and ordering
    return query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()


def get_task_statistics(db: Session) -> dict:
    """
    Get task statistics (total, completed, pending).
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with task counts
    """
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.completed == True).count()
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """
    Create a new task in the database.
    
    Args:
        db: Database session
        task: Task data from request
        
    Returns:
        Created Task object with generated ID and timestamps
        
    Raises:
        SQLAlchemyError: If database operation fails
    """
    db_task = models.Task(
        title=task.title,
        completed=False  # New tasks are always incomplete
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Get the generated ID and timestamps
    
    return db_task


def update_task(
    db: Session, 
    task_id: int, 
    task_update: schemas.TaskUpdate
) -> Optional[models.Task]:
    """
    Update an existing task.
    
    Args:
        db: Database session
        task_id: ID of the task to update
        task_update: Updated task data
        
    Returns:
        Updated Task object if found, None otherwise
    """
    db_task = get_task(db, task_id)
    
    if db_task is None:
        return None
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    # Explicitly update the timestamp
    db_task.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(db_task)
    
    return db_task


def complete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """
    Mark a task as completed.
    
    Args:
        db: Database session
        task_id: ID of the task to complete
        
    Returns:
        Updated Task object if found, None otherwise
    """
    db_task = get_task(db, task_id)
    
    if db_task is None:
        return None
    
    db_task.completed = True
    
    # Explicitly update the timestamp  
    db_task.updated_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(db_task)
    
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task from the database.
    
    Args:
        db: Database session
        task_id: ID of the task to delete
        
    Returns:
        True if task was deleted, False if not found
    """
    db_task = get_task(db, task_id)
    
    if db_task is None:
        return False
    
    db.delete(db_task)
    db.commit()
    
    return True
