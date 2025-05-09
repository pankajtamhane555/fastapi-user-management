from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash
from app.db.base import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, Token

# Create router without dependencies (no auth required for these endpoints)
router = APIRouter()

@router.post("/login", 
    response_model=Token, 
    status_code=status.HTTP_200_OK,
    description="Login with email and password to get access token",
    tags=["authentication"]
)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", 
    response_model=UserSchema, 
    status_code=status.HTTP_201_CREATED,
    description="Register a new user",
    tags=["authentication"]
)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    
    if user_in.admin_token and user_in.admin_token != "string" and user_in.admin_token != settings.ADMIN_REGISTRATION_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid admin registration token",
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role="admin" if user_in.admin_token == settings.ADMIN_REGISTRATION_TOKEN else "user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
