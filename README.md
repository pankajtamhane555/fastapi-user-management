# FastAPI User Management

A robust and secure FastAPI microservice implementing comprehensive user management with JWT-based authentication and Role-Based Access Control (RBAC). This service provides a production-ready foundation for managing user accounts, authentication, and authorization in modern web applications.

## Test Coverage

The project maintains high test coverage across all modules:

| Module                      | Coverage |
|----------------------------|----------|
| app/api/v1/dependencies.py | 100%     |
| app/api/v1/endpoints/auth.py| 97%      |
| app/api/v1/endpoints/users.py| 95%      |
| app/api/v1/router.py       | 100%     |
| app/core/config.py         | 93%      |
| app/core/security.py       | 96%      |
| app/db/base.py            | 94%      |
| app/main.py               | 93%      |
| app/models/user.py        | 100%     |
| app/schemas/user.py       | 100%     |
| **Total Coverage**        | **96%**  |

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Docker 24.0 or higher
- Docker Compose v2.0 or higher
- PostgreSQL 15.0 or higher (if running without Docker)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/pankajtamhane555/fastapi-user-management.git
cd fastapi-user-management
```
2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configurations
```
3. Build and start the containers:
```bash
docker-compose up --build
```

### Running Tests
```bash
# Run all tests
docker exec -it pocprojects-web-1 pytest

# Run tests with coverage
docker exec -it pocprojects-web-1 bash -c "COVERAGE_FILE=/tmp/.coverage pytest --cov=app --cov-report=term-missing"
```
The coverage report will show:
- Percentage of code covered by tests for each module
- Lines that are missing test coverage
- Overall project coverage statistics

## API Documentation

The API documentation is available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

#### Authentication

- `POST /api/v1/auth/login`
  - Login with email/password to get access token
  - Request body: `{ "username": "email@example.com", "password": "yourpassword" }`
  - Response: `{ "access_token": "token", "token_type": "bearer" }`

- `POST /api/v1/auth/register`
  - Register a new user
  - Request body: `{ "email": "email@example.com", "password": "password", "full_name": "User Name" }`
  - Optional admin registration with token: Include `"admin_token": "your-admin-token"`

#### Users

- `GET /api/v1/users/me`
  - Get current user details
  - Requires authentication

- `GET /api/v1/users/{user_id}`
  - Get user by ID
  - Requires admin role

## Project Structure
```plaintext
fastapi-user-management/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py      # Authentication endpoints
│   │       │   └── users.py     # User management endpoints
│   │       └── dependencies.py   # API dependencies
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   └── security.py          # Security utilities
│   ├── db/
│   │   └── base.py              # Database setup
│   ├── models/                  # SQLAlchemy models
│   └── schemas/                 # Pydantic schemas
├── tests/                      # Test suite
├── docker-compose.yml          # Docker compose configuration
├── Dockerfile                  # Docker build instructions
├── requirements.txt            # Python dependencies
└── .env.example               # Example environment variables
```

## Environment Variables

Required variables in `.env`:
```bash
# Project Settings
PROJECT_NAME=User Management API
VERSION=1.0.0
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-secret-key-here  # Generate using: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin
ADMIN_REGISTRATION_TOKEN=your-admin-token-here

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:8000","http://localhost:3000"]

# Database
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=user_management
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:5432/${POSTGRES_DB}
```

## License

MIT License
