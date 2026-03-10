"""
Integration tests for multi-step workflows and edge cases
"""

from fastapi.testclient import TestClient
from src.app import app


def test_signup_then_unregister():
    """Test full signup and unregister cycle"""
    # Arrange
    client = TestClient(app)
    activity_name = "Art Studio"
    email = "newstudent@example.com"

    # Act: Signup
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    # Act: Unregister
    unregister_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert unregister_response.status_code == 200

    # Assert: Check activities reflect the changes
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_multiple_signups():
    """Test signing up multiple students and verify participant count"""
    # Arrange
    client = TestClient(app)
    activity_name = "Debate Team"
    emails = ["student1@example.com", "student2@example.com", "student3@example.com"]

    # Act: Signup multiple students
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200

    # Assert: Check activities reflect the additions
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    participants = activities[activity_name]["participants"]
    for email in emails:
        assert email in participants
    # Original participant should still be there
    assert "ryan@mergington.edu" in participants


def test_activities_persistence():
    """Test that activities data persists across requests"""
    # Arrange
    client = TestClient(app)

    # Act: Get activities twice
    response1 = client.get("/activities")
    response2 = client.get("/activities")

    # Assert: Both responses are identical
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()