from fastapi.testclient import TestClient
from app.main import app

def test_app_startup():
    """Test FastAPI app startup and configuration"""
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200

    # Test health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    # Test OpenAPI schema
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200

def test_app_exception_handlers():
    """Test custom exception handlers"""
    client = TestClient(app)

    # Test 404 Not Found
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert "detail" in response.json()

    # Test method not allowed
    response = client.post("/health")
    assert response.status_code == 405
    assert "detail" in response.json()
