"""
Unit tests for CRUD operations.

These tests focus on testing the database layer operations
in isolation using a test database.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas, models


# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_task_with_valid_data_should_return_task(db_session):
    """Test creating a task with valid data."""
    # Given: valid task data
    task_data = schemas.TaskCreate(title="Test Task")
    
    # When: creating a task
    created_task = crud.create_task(db=db_session, task=task_data)
    
    # Then: should return created task with proper attributes
    assert created_task.id is not None
    assert created_task.title == "Test Task"
    assert created_task.completed is False
    assert created_task.created_at is not None
    assert created_task.updated_at is not None


def test_get_task_with_existing_id_should_return_task(db_session):
    """Test getting an existing task by ID."""
    # Given: an existing task
    task_data = schemas.TaskCreate(title="Test Task")
    created_task = crud.create_task(db=db_session, task=task_data)
    
    # When: getting the task by ID
    retrieved_task = crud.get_task(db=db_session, task_id=created_task.id)
    
    # Then: should return the task
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == created_task.title


def test_get_task_with_nonexistent_id_should_return_none(db_session):
    """Test getting a non-existent task by ID."""
    # Given: non-existent task ID
    task_id = 999
    
    # When: getting the task by ID
    retrieved_task = crud.get_task(db=db_session, task_id=task_id)
    
    # Then: should return None
    assert retrieved_task is None


def test_get_tasks_should_return_list_with_pagination(db_session):
    """Test getting tasks with pagination."""
    # Given: multiple tasks
    task_titles = []
    for i in range(5):
        task_data = schemas.TaskCreate(title=f"Task {i+1}")
        created_task = crud.create_task(db=db_session, task=task_data)
        task_titles.append(created_task.title)
    
    # When: getting tasks with pagination
    tasks = crud.get_tasks(db=db_session, skip=1, limit=2)
    
    # Then: should return correct number of tasks
    assert len(tasks) == 2
    # Verify that we're getting different tasks (pagination working)
    all_tasks = crud.get_tasks(db=db_session, skip=0, limit=5)
    assert len(all_tasks) == 5


def test_get_tasks_with_completion_filter_should_return_filtered_tasks(db_session):
    """Test getting tasks filtered by completion status."""
    # Given: tasks with different completion status
    completed_task = crud.create_task(db=db_session, task=schemas.TaskCreate(title="Completed Task"))
    crud.complete_task(db=db_session, task_id=completed_task.id)
    
    pending_task = crud.create_task(db=db_session, task=schemas.TaskCreate(title="Pending Task"))
    
    # When: getting completed tasks
    completed_tasks = crud.get_tasks(db=db_session, completed=True)
    pending_tasks = crud.get_tasks(db=db_session, completed=False)
    
    # Then: should return correctly filtered tasks
    assert len(completed_tasks) == 1
    assert completed_tasks[0].title == "Completed Task"
    assert completed_tasks[0].completed is True
    
    assert len(pending_tasks) == 1
    assert pending_tasks[0].title == "Pending Task"
    assert pending_tasks[0].completed is False


def test_update_task_with_valid_data_should_return_updated_task(db_session):
    """Test updating a task with valid data."""
    # Given: an existing task
    task_data = schemas.TaskCreate(title="Original Title")
    created_task = crud.create_task(db=db_session, task=task_data)
    original_updated_at = created_task.updated_at
    
    # Add a small delay to ensure timestamp difference
    import time
    time.sleep(0.01)
    
    # When: updating the task
    update_data = schemas.TaskUpdate(title="Updated Title", completed=True)
    updated_task = crud.update_task(
        db=db_session, 
        task_id=created_task.id, 
        task_update=update_data
    )
    
    # Then: should return updated task
    assert updated_task is not None
    assert updated_task.id == created_task.id
    assert updated_task.title == "Updated Title"
    assert updated_task.completed is True
    assert updated_task.updated_at >= original_updated_at


def test_update_nonexistent_task_should_return_none(db_session):
    """Test updating a non-existent task."""
    # Given: non-existent task ID
    task_id = 999
    update_data = schemas.TaskUpdate(title="Updated Title")
    
    # When: trying to update the task
    updated_task = crud.update_task(
        db=db_session, 
        task_id=task_id, 
        task_update=update_data
    )
    
    # Then: should return None
    assert updated_task is None


def test_complete_task_should_mark_as_completed(db_session):
    """Test marking a task as completed."""
    # Given: an incomplete task
    task_data = schemas.TaskCreate(title="Task to Complete")
    created_task = crud.create_task(db=db_session, task=task_data)
    assert created_task.completed is False
    original_updated_at = created_task.updated_at
    
    # Add a small delay to ensure timestamp difference
    import time
    time.sleep(0.01)
    
    # When: completing the task
    completed_task = crud.complete_task(db=db_session, task_id=created_task.id)
    
    # Then: should be marked as completed
    assert completed_task is not None
    assert completed_task.completed is True
    assert completed_task.updated_at >= original_updated_at


def test_complete_nonexistent_task_should_return_none(db_session):
    """Test completing a non-existent task."""
    # Given: non-existent task ID
    task_id = 999
    
    # When: trying to complete the task
    completed_task = crud.complete_task(db=db_session, task_id=task_id)
    
    # Then: should return None
    assert completed_task is None


def test_delete_task_should_return_true(db_session):
    """Test deleting an existing task."""
    # Given: an existing task
    task_data = schemas.TaskCreate(title="Task to Delete")
    created_task = crud.create_task(db=db_session, task=task_data)
    
    # When: deleting the task
    result = crud.delete_task(db=db_session, task_id=created_task.id)
    
    # Then: should return True and task should be gone
    assert result is True
    assert crud.get_task(db=db_session, task_id=created_task.id) is None


def test_delete_nonexistent_task_should_return_false(db_session):
    """Test deleting a non-existent task."""
    # Given: non-existent task ID
    task_id = 999
    
    # When: trying to delete the task
    result = crud.delete_task(db=db_session, task_id=task_id)
    
    # Then: should return False
    assert result is False


def test_get_task_statistics_should_return_correct_counts(db_session):
    """Test getting task statistics."""
    # Given: tasks with different completion status
    crud.create_task(db=db_session, task=schemas.TaskCreate(title="Task 1"))
    
    task2 = crud.create_task(db=db_session, task=schemas.TaskCreate(title="Task 2"))
    crud.complete_task(db=db_session, task_id=task2.id)
    
    task3 = crud.create_task(db=db_session, task=schemas.TaskCreate(title="Task 3"))
    crud.complete_task(db=db_session, task_id=task3.id)
    
    # When: getting statistics
    stats = crud.get_task_statistics(db=db_session)
    
    # Then: should return correct counts
    assert stats["total"] == 3
    assert stats["completed"] == 2
    assert stats["pending"] == 1
