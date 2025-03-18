from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
)
from app.core.security import get_password_hash
from app.db.base import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Get current user profile"""
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_current_user(
    *,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_in: UserUpdate,
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Update current user profile"""
    # Check if email exists
    if user_in.email:
        user = db.query(User).filter(
            User.email == user_in.email,
            User.id != current_user.id
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user fields
    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password" and value:
            setattr(current_user, "hashed_password", get_password_hash(value))
        else:
            setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user

@router.get("/", response_model=List[UserResponse])
def read_users_list(
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[Session, Depends(get_db)]
) -> List[User]:
    """Get list of users (admin only)"""
    users = db.query(User).all()
    return users

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    """Delete current user"""
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}
