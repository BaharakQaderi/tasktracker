"""
FastAPI application for TaskTracker.

This is the main application file that defines all API endpoints
and configures the FastAPI application with proper error handling,
documentation, and middleware.
"""

from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db, create_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
create_tables()


# Application lifecycle events  
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("🚀 TaskTracker API starting up...")
    logger.info("✅ Database tables created successfully")
    yield
    # Shutdown
    logger.info("🛑 TaskTracker API shutting down...")


# Initialize FastAPI application
app = FastAPI(
    title="TaskTracker API",
    description="A simple task management API built with FastAPI and PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Custom Exception Classes
class TaskNotFoundException(Exception):
    """Exception raised when a task is not found."""
    pass


class TaskValidationError(Exception):
    """Exception raised when task data is invalid."""
    pass


# Exception Handlers
@app.exception_handler(TaskNotFoundException)
async def task_not_found_handler(request, exc):
    """Handle task not found exceptions."""
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "TASK_NOT_FOUND",
                "message": str(exc)
            }
        }
    )


@app.exception_handler(TaskValidationError)
async def task_validation_handler(request, exc):
    """Handle task validation exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "TASK_VALIDATION_ERROR",
                "message": str(exc)
            }
        }
    )


# API Endpoints

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint for health check.
    
    Returns basic information about the API.
    """
    return {
        "message": "Welcome to TaskTracker API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the application and database.
    """
    try:
        # Test database connection
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


@app.get("/tasks", response_model=schemas.TaskList, tags=["Tasks"])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of tasks with optional filtering and pagination.
    
    - **skip**: Number of tasks to skip (default: 0)
    - **limit**: Maximum number of tasks to return (default: 100, max: 1000)
    - **completed**: Filter by completion status (true/false, or omit for all)
    
    Returns a list of tasks with statistics.
    """
    # Validate limit
    if limit > 1000:
        limit = 1000
    
    # Get tasks and statistics
    tasks = crud.get_tasks(db, skip=skip, limit=limit, completed=completed)
    stats = crud.get_task_statistics(db)
    
    return schemas.TaskList(
        tasks=tasks,
        **stats
    )


@app.get("/tasks/stats", response_model=dict, tags=["Statistics"])
async def get_task_statistics(db: Session = Depends(get_db)):
    """
    Get task statistics.
    
    Returns counts of total, completed, and pending tasks.
    """
    return crud.get_task_statistics(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.
    
    - **task_id**: Unique identifier of the task
    
    Returns the task details if found.
    """
    task = crud.get_task(db, task_id=task_id)
    
    if task is None:
        raise TaskNotFoundException(f"Task with ID {task_id} does not exist")
    
    return task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-200 characters)
    
    Returns the created task with auto-generated ID and timestamps.
    """
    try:
        new_task = crud.create_task(db=db, task=task)
        logger.info(f"Created new task: {new_task.id} - {new_task.title}")
        return new_task
    except Exception as e:
        logger.error(f"Failed to create task: {str(e)}")
        raise TaskValidationError(f"Failed to create task: {str(e)}")


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
async def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    - **task_id**: Unique identifier of the task
    - **title**: Updated task title (optional)
    - **completed**: Updated completion status (optional)
    
    Returns the updated task.
    """
    updated_task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    
    if updated_task is None:
        raise TaskNotFoundException(f"Task with ID {task_id} does not exist")
    
    logger.info(f"Updated task: {updated_task.id}")
    return updated_task


@app.post("/tasks/{task_id}/complete", response_model=schemas.TaskResponse, tags=["Tasks"])
async def complete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Mark a task as completed.
    
    - **task_id**: Unique identifier of the task
    
    Returns the updated task with completed status set to true.
    """
    completed_task = crud.complete_task(db=db, task_id=task_id)
    
    if completed_task is None:
        raise TaskNotFoundException(f"Task with ID {task_id} does not exist")
    
    logger.info(f"Completed task: {completed_task.id} - {completed_task.title}")
    return completed_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task.
    
    - **task_id**: Unique identifier of the task
    
    Returns 204 No Content if successful.
    """
    deleted = crud.delete_task(db=db, task_id=task_id)
    
    if not deleted:
        raise TaskNotFoundException(f"Task with ID {task_id} does not exist")
    
    logger.info(f"Deleted task: {task_id}")
    return


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
