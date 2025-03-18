from typing import Dict
from fastapi.testclient import TestClient
from app.core.config import settings

def test_login_success(client: TestClient, normal_user: Dict[str, str]):
    """Test successful login"""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": normal_user["email"],
            "password": normal_user["password"]
        }
    )
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

def test_login_incorrect_password(client: TestClient, normal_user: Dict[str, str]):
    """Test login with incorrect password"""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": normal_user["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_login_nonexistent_user(client: TestClient):
    """Test login with non-existent user"""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 401

def test_register_success(client: TestClient):
    """Test successful user registration"""
    user_data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "full_name": "New User"
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data

def test_register_existing_email(client: TestClient, normal_user: Dict[str, str]):
    """Test registration with existing email"""
    user_data = {
        "email": normal_user["email"],
        "password": "newpassword",
        "full_name": "New User"
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    assert response.status_code == 400

def test_register_admin_success(client: TestClient):
    """Test successful admin registration"""
    user_data = {
        "email": "newadmin@example.com",
        "password": "adminpassword",
        "full_name": "New Admin",
        "admin_token": settings.ADMIN_REGISTRATION_TOKEN
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["role"] == "admin"

def test_register_admin_invalid_token(client: TestClient):
    """Test admin registration with invalid token"""
    user_data = {
        "email": "newadmin@example.com",
        "password": "adminpassword",
        "full_name": "New Admin",
        "admin_token": "invalid_token"
    }
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    assert response.status_code == 400
