def test_get_activities(client):
    # Arrange: client fixture is provided

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v and 'participants' in v for v in data.values())

def test_signup_success(client):
    # Arrange
    email = "testuser@example.com"
    activity = next(iter(client.get("/activities").json().keys()))

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()

def test_signup_duplicate(client):
    # Arrange
    email = "dupeuser@example.com"
    activity = next(iter(client.get("/activities").json().keys()))
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()

def test_signup_nonexistent_activity(client):
    # Arrange
    email = "ghost@example.com"
    activity = "nonexistent-activity"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "detail" in response.json()
