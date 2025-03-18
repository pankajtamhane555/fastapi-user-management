from typing import Dict
import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from app.models.user import User

def test_read_current_user(client: TestClient, user_token_headers: Dict[str, str]):
    """Test reading current user profile"""
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["role"] == "user"

def test_read_current_user_no_auth(client: TestClient):
    """Test reading current user profile without authentication"""
    response = client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == 401

def test_update_current_user(client: TestClient, user_token_headers: Dict[str, str]):
    """Test updating current user profile"""
    data = {"full_name": "Updated Name"}
    response = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
        json=data
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["full_name"] == data["full_name"]

def test_update_user_email_exists(client: TestClient, user_token_headers: Dict[str, str], admin_user: Dict[str, str]):
    """Test updating user email to an existing one"""
    data = {"email": admin_user["email"]}
    response = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
        json=data
    )
    assert response.status_code == 400

def test_read_user_by_id_admin(client: TestClient, admin_token_headers: Dict[str, str], normal_user: Dict[str, str]):
    """Test reading user by ID as admin"""
    response = client.get(
        f"{settings.API_V1_STR}/users/{normal_user['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == normal_user["email"]

def test_read_user_by_id_normal_user(client: TestClient, user_token_headers: Dict[str, str], admin_user: Dict[str, str]):
    """Test reading user by ID as normal user"""
    response = client.get(
        f"{settings.API_V1_STR}/users/{admin_user['id']}",
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_read_users_list_admin(client: TestClient, admin_token_headers: Dict[str, str], normal_user: Dict[str, str]):
    """Test reading users list as admin"""
    response = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=admin_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # At least admin and normal user
    assert any(user["email"] == "admin@example.com" for user in data)
    assert any(user["email"] == "test@example.com" for user in data)

def test_read_users_list_normal_user(client: TestClient, user_token_headers: Dict[str, str]):
    """Test reading users list as normal user"""
    response = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=user_token_headers
    )
    assert response.status_code == 403

def test_delete_current_user(client: TestClient, user_token_headers: Dict[str, str], db):
    """Test deleting current user"""
    response = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers
    )
    assert response.status_code == 200
    
    # Verify user is deleted from database
    user = db.query(User).filter(User.email == "test@example.com").first()
    assert user is None
