"""
Integration tests for TaskTracker API endpoints.

These tests validate the complete API workflow including
HTTP requests, database interactions, and response formatting.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint_should_return_welcome_message(test_db):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to TaskTracker API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"


def test_health_endpoint_should_return_healthy_status(test_db):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_create_task_with_valid_data_should_return_201(test_db):
    """Test creating a new task."""
    task_data = {"title": "Test Task for Integration"}
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["id"] is not None
    assert data["completed"] is False
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_with_invalid_data_should_return_422(test_db):
    """Test creating a task with invalid data."""
    task_data = {"title": ""}  # Empty title should fail validation
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 422


def test_get_tasks_should_return_task_list(test_db):
    """Test getting all tasks."""
    # Create some test tasks
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    
    data = response.json()
    assert "tasks" in data
    assert "total" in data
    assert "completed" in data
    assert "pending" in data
    assert len(data["tasks"]) == 2
    assert data["total"] == 2
    assert data["completed"] == 0
    assert data["pending"] == 2


def test_get_task_by_id_should_return_task(test_db):
    """Test getting a specific task by ID."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Specific Task"})
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Get the task by ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


def test_get_nonexistent_task_should_return_404(test_db):
    """Test getting a non-existent task."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "TASK_NOT_FOUND"


def test_update_task_should_return_updated_task(test_db):
    """Test updating an existing task."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Original Title"})
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Update the task
    update_data = {"title": "Updated Title", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["completed"] is True


def test_update_nonexistent_task_should_return_404(test_db):
    """Test updating a non-existent task."""
    update_data = {"title": "Updated Title"}
    response = client.put("/tasks/999", json=update_data)
    assert response.status_code == 404


def test_complete_task_should_mark_as_completed(test_db):
    """Test marking a task as completed."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Task to Complete"})
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Complete the task
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["completed"] is True


def test_complete_nonexistent_task_should_return_404(test_db):
    """Test completing a non-existent task."""
    response = client.post("/tasks/999/complete")
    assert response.status_code == 404


def test_delete_task_should_return_204(test_db):
    """Test deleting a task."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Task to Delete"})
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify task is gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_task_should_return_404(test_db):
    """Test deleting a non-existent task."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404


def test_get_task_statistics_should_return_correct_counts(test_db):
    """Test getting task statistics."""
    # Create tasks with different statuses
    client.post("/tasks", json={"title": "Task 1"})
    
    create_response = client.post("/tasks", json={"title": "Task 2"})
    task_id = create_response.json()["id"]
    client.post(f"/tasks/{task_id}/complete")
    
    # Get statistics
    response = client.get("/tasks/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1


def test_filter_tasks_by_completion_status(test_db):
    """Test filtering tasks by completion status."""
    # Create tasks
    client.post("/tasks", json={"title": "Pending Task"})
    
    create_response = client.post("/tasks", json={"title": "Completed Task"})
    task_id = create_response.json()["id"]
    client.post(f"/tasks/{task_id}/complete")
    
    # Test filtering completed tasks
    response = client.get("/tasks?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Completed Task"
    
    # Test filtering pending tasks
    response = client.get("/tasks?completed=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Pending Task"


def test_pagination_should_work_correctly(test_db):
    """Test task pagination."""
    # Create multiple tasks
    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i+1}"})
    
    # Test pagination
    response = client.get("/tasks?skip=1&limit=2")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["tasks"]) == 2
    assert data["total"] == 5
    
    # Verify pagination is working (we should get a subset)
    all_response = client.get("/tasks")
    all_data = all_response.json()
    assert len(all_data["tasks"]) == 5


def test_api_workflow_complete_scenario(test_db):
    """Test a complete API workflow scenario."""
    # 1. Create a task
    create_response = client.post("/tasks", json={"title": "Complete Workflow Task"})
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    
    # 2. Get the task
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Complete Workflow Task"
    
    # 3. Update the task
    update_response = client.put(
        f"/tasks/{task_id}", 
        json={"title": "Updated Workflow Task"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Workflow Task"
    
    # 4. Complete the task
    complete_response = client.post(f"/tasks/{task_id}/complete")
    assert complete_response.status_code == 200
    assert complete_response.json()["completed"] is True
    
    # 5. Check statistics
    stats_response = client.get("/tasks/stats")
    assert stats_response.status_code == 200
    stats = stats_response.json()
    assert stats["total"] >= 1
    assert stats["completed"] >= 1
    
    # 6. Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # 7. Verify deletion
    final_get_response = client.get(f"/tasks/{task_id}")
    assert final_get_response.status_code == 404
