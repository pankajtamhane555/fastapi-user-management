from typing import Dict
import pytest
from fastapi import HTTPException
from app.api.v1.dependencies import get_current_user, get_current_active_user, get_current_admin_user
from app.core.security import create_access_token
from app.models.user import User

def test_get_current_user_invalid_token(db):
    """Test get_current_user with invalid token"""
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalid_token", db=db)
    assert exc_info.value.status_code == 401

def test_get_current_user_nonexistent(db, normal_user):
    """Test get_current_user with token for nonexistent user"""
    # Create token for a user that doesn't exist
    token = create_access_token(subject="nonexistent@example.com")
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, db=db)
    assert exc_info.value.status_code == 404

def test_get_current_active_user_inactive(db, normal_user):
    """Test get_current_active_user with inactive user"""
    # Get the user and set them as inactive
    user = db.query(User).filter(User.email == normal_user["email"]).first()
    user.is_active = False
    db.commit()
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(current_user=user)
    assert exc_info.value.status_code == 400

def test_get_current_admin_user_not_admin(db, normal_user):
    """Test get_current_admin_user with non-admin user"""
    # Get the user
    user = db.query(User).filter(User.email == normal_user["email"]).first()
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(current_user=user)
    assert exc_info.value.status_code == 403
