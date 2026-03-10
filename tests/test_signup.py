"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""

from fastapi.testclient import TestClient
from src.app import app


def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_nonexistent_activity():
    """Test signup for a non-existent activity"""
    # Arrange
    client = TestClient(app)
    activity_name = "NonExistent Club"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate():
    """Test duplicate signup prevention"""
    # Arrange
    client = TestClient(app)
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" in data["detail"]