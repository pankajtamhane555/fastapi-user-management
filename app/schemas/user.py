from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base User Schema"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """User Creation Schema"""
    email: EmailStr
    password: str
    admin_token: Optional[str] = None

class UserUpdate(UserBase):
    """User Update Schema"""
    password: Optional[str] = None

class UserResponse(UserBase):
    """User Response Schema"""
    id: int
    email: EmailStr
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class UserInDBBase(UserBase):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: int
    exp: int
