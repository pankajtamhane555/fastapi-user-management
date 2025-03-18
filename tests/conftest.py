from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db) -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

@pytest.fixture
def admin_user(db) -> Dict[str, str]:
    user_data = {
        "email": "admin@example.com",
        "password": "adminpassword",
        "full_name": "Admin User"
    }
    db_user = User(
        email=user_data["email"],
        hashed_password=get_password_hash(user_data["password"]),
        full_name=user_data["full_name"],
        role="admin",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_data["id"] = db_user.id
    return user_data

@pytest.fixture
def normal_user(db, admin_user) -> Dict[str, str]:
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User"
    }
    db_user = User(
        email=user_data["email"],
        hashed_password=get_password_hash(user_data["password"]),
        full_name=user_data["full_name"],
        role="user",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_data["id"] = db_user.id
    return user_data

@pytest.fixture
def user_token_headers(client: TestClient, normal_user: Dict[str, str]) -> Dict[str, str]:
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": normal_user["email"],
            "password": normal_user["password"]
        }
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

@pytest.fixture
def admin_token_headers(client: TestClient, admin_user: Dict[str, str]) -> Dict[str, str]:
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": admin_user["email"],
            "password": admin_user["password"]
        }
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
