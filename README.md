# fastapi-user-management

A robust and secure FastAPI microservice implementing comprehensive user management with JWT-based authentication and Role-Based Access Control (RBAC) using the Oso framework. This service provides a production-ready foundation for managing user accounts, authentication, and authorization in modern web applications.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/pankajtamhane555/fastapi-user-management.git
cd fastapi-user-management

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Key Features

- 🔐 Secure JWT-based Authentication
- 👥 Complete User Profile Management (CRUD)
- 🛡️ Dynamic Role-Based Access Control (RBAC) with Oso
- 📝 Interactive API Documentation with Swagger UI
- ✅ Comprehensive Test Coverage
- 🔄 Database Migrations with Alembic
- 🎯 Input Validation with Pydantic
- 🔍 SQLAlchemy ORM for Database Operations

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs
- SQLAlchemy: Powerful SQL toolkit and ORM
- PostgreSQL: Advanced open-source database
- Oso: Battery-included authorization framework
- JWT: JSON Web Tokens for secure authentication
- Pydantic: Data validation using Python type annotations
- Alembic: Database migration tool
- Pytest: Feature-rich testing framework

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   ├── dependencies.py
│   │   │   └── router.py
│   ├── core/
│   │   ├── auth.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   └── main.py
├── tests/
├── alembic/
├── alembic.ini
├── .env
└── requirements.txt
```

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/pankajtamhane555/fastapi-user-management.git
cd fastapi-user-management
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and update the variables:

```bash
cp .env.example .env
```

Required environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate using `openssl rand -hex 32`)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiry (default: 30)
- `ADMIN_REGISTRATION_TOKEN`: Token required to register admin users
- `API_V1_STR`: API version prefix (default: /api/v1)
- `PROJECT_NAME`: Project name for documentation
- `VERSION`: API version
- `BACKEND_CORS_ORIGINS`: List of allowed CORS origins

### Starting the Application

Initialize the database:

```bash
alembic upgrade head
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- POST `/api/v1/auth/login` - User login
- POST `/api/v1/auth/register` - User registration

### User Management

- GET `/api/v1/users/me` - Get current user profile
- GET `/api/v1/users/{user_id}` - Get user by ID (Admin only)
- PATCH `/api/v1/users/me` - Update current user profile
- DELETE `/api/v1/users/me` - Delete current user
- GET `/api/v1/users` - List all users (Admin only)

## Running Tests

### Prerequisites

- Python 3.9 or higher
- Virtual environment activated
- All dependencies installed

### Test Configuration

The test suite uses SQLite as the test database for faster execution and isolation. No additional database setup is required for testing.

### Running the Test Suite

1. Run all tests with coverage report:

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

2. Run specific test files:

```bash
pytest tests/test_auth.py -v  # Run auth tests
pytest tests/test_users.py -v  # Run user tests
```

3. Run specific test functions:

```bash
pytest tests/test_auth.py::test_login_success -v
```

### Test Structure

1. Authentication Tests (`test_auth.py`):
   - Login functionality
   - User registration
   - Admin registration
   - Error handling

2. User Management Tests (`test_users.py`):
   - CRUD operations on user profiles
   - Admin-only operations
   - Authorization checks
   - Input validation

3. Database Tests (`test_db.py`):
   - Connection handling
   - Session management
   - Model operations

4. Core Tests (`test_main.py`):
   - Application startup
   - Exception handlers
   - Middleware

### Test Coverage

Current test coverage: 96%

- Core functionality: 100%
- API endpoints: 95%
- Database operations: 94%
- Error handlers: 88%

## License

MIT License
