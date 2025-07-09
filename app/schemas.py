"""
Pydantic schemas for TaskTracker API.

This module defines the data validation and serialization schemas
using Pydantic. These schemas ensure type safety and automatic
validation for API requests and responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base schema for Task with common attributes."""
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title or description",
        example="Learn FastAPI"
    )


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    
    Inherits from TaskBase and only requires the title field.
    The completed status defaults to False in the database.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    
    All fields are optional to allow partial updates.
    """
    
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated task title",
        example="Learn FastAPI and SQLAlchemy"
    )
    
    completed: Optional[bool] = Field(
        None,
        description="Updated completion status",
        example=True
    )


class TaskResponse(TaskBase):
    """
    Schema for task responses from the API.
    
    Includes all task fields including auto-generated ones
    like id and timestamps.
    """
    
    id: int = Field(
        ...,
        description="Unique task identifier",
        example=1
    )
    
    completed: bool = Field(
        ...,
        description="Task completion status",
        example=False
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp when task was created",
        example="2024-01-15T10:30:00Z"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp when task was last updated",
        example="2024-01-15T10:30:00Z"
    )
    
    # Configure Pydantic to work with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    """
    Schema for paginated task list responses.
    """
    
    tasks: list[TaskResponse] = Field(
        ...,
        description="List of tasks"
    )
    
    total: int = Field(
        ...,
        description="Total number of tasks",
        example=10
    )
    
    completed: int = Field(
        ...,
        description="Number of completed tasks",
        example=3
    )
    
    pending: int = Field(
        ...,
        description="Number of pending tasks",
        example=7
    )


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    
    error: dict = Field(
        ...,
        description="Error details",
        example={
            "code": "TASK_NOT_FOUND",
            "message": "Task with ID 123 does not exist"
        }
    )
