"""
Tests for the DELETE /activities/{activity_name}/signup endpoint
"""

from fastapi.testclient import TestClient
from src.app import app


def test_unregister_success():
    """Test successful unregister from an activity"""
    # Arrange
    client = TestClient(app)
    activity_name = "Gym Class"
    email = "john@mergington.edu"  # Already signed up

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_nonexistent_activity():
    """Test unregister from a non-existent activity"""
    # Arrange
    client = TestClient(app)
    activity_name = "NonExistent Club"
    email = "test@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_participant():
    """Test unregister when student is not signed up"""
    # Arrange
    client = TestClient(app)
    activity_name = "Tennis Club"
    email = "notsignedup@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Student not found in this activity" in data["detail"]