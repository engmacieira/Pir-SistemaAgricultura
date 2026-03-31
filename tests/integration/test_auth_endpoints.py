def test_register_and_login_success(client):
    # Register
    register_data = {
        "email": "testint@example.com",
        "password": "strongpassword",
        "full_name": "Integration Test User",
        "phone": "999999999"
    }

    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["email"] == "testint@example.com"
    assert user_data["full_name"] == "Integration Test User"
    assert "id" in user_data

    # Try to register again with same email
    response_dup = client.post("/auth/register", json=register_data)
    assert response_dup.status_code == 400

    # Login
    login_data = {
        "email": "testint@example.com",
        "password": "strongpassword"
    }

    response_login = client.post("/auth/login", json=login_data)
    assert response_login.status_code == 200
    token_data = response_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas."
