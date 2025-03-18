# fastapi-user-management

A robust and secure FastAPI microservice implementing comprehensive user management with JWT-based authentication and Role-Based Access Control (RBAC) using the Oso framework. This service provides a production-ready foundation for managing user accounts, authentication, and authorization in modern web applications.

## System Requirements

- Python 3.10 or higher
- Docker 24.0 or higher (for containerized deployment)
- Docker Compose v2.0 or higher (for local development)
- PostgreSQL 15.0 or higher (if running without Docker)

## Quick Start with Docker (Recommended)

### Using Docker Compose

1. Clone the repository:

```bash
git clone https://github.com/pankajtamhane555/fastapi-user-management.git
cd fastapi-user-management
```

1. Copy the environment file and update the variables:

```bash
cp .env.example .env
```

1. Build and start the containers:

```bash
docker-compose up --build
```

### Alternative: Using Docker Without Compose

If docker-compose is not available, you can use these Docker commands:

1. Create a Docker network:

```bash
docker network create user-management-network
```

1. Start PostgreSQL container:

```bash
docker run -d \
  --name user-management-db \
  --network user-management-network \
  -p 5433:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=user_management \
  postgres:15-alpine
```

1. Build and start the FastAPI application:

```bash
# Build the image
docker build -t user-management-app .

# Run the container
docker run -d \
  --name user-management-app \
  --network user-management-network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@user-management-db:5432/user_management \
  -e SECRET_KEY=your-secret-key-here \
  -e ADMIN_REGISTRATION_TOKEN=admin-token \
  -e BACKEND_CORS_ORIGINS='["http://localhost:8000","http://localhost:3000"]' \
  user-management-app
```

1. Check container logs:

```bash
# Check database logs
docker logs user-management-db

# Check application logs
docker logs user-management-app
```

1. Stop and remove containers:

```bash
# Stop containers
docker stop user-management-app user-management-db

# Remove containers
docker rm user-management-app user-management-db

# Remove network
docker network rm user-management-network
```

The API will be available at:

- Swagger Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Environment Variables

Required environment variables in `.env`:

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

## Common Issues and Solutions

### Database Connection Issues

1. **Port Conflict with Local PostgreSQL**
   - **Symptom**: Error message about port 5432 being in use
   - **Solution**: The docker-compose.yml is configured to use port 5433 instead of 5432 to avoid conflicts with local PostgreSQL installations

2. **Database Connection Failures**
   - **Symptom**: Connection refused or similar database errors
   - **Solution**:  
     - Ensure POSTGRES_SERVER is set to 'db' when using Docker Compose  
     - Use 'user-management-db' as the host when using plain Docker  
     - For local development, set it to 'localhost'  
     - Check that database credentials match in both DATABASE_URL and POSTGRES_* variables

### Docker Issues

1. **Docker Compose Not Available**
   - **Symptom**: 'docker-compose' command not found
   - **Solution**:  
     - Use the alternative Docker commands provided above  
     - Install Docker Compose if possible: `pip install docker-compose`  
     - On Linux, you can also install via package manager: `sudo apt-get install docker-compose`

2. **Container Build Failures**
   - **Symptom**: Build errors or missing dependencies
   - **Solution**:  
     - Run docker-compose build --no-cache to force rebuild  
     - For plain Docker: docker build --no-cache -t user-management-app .  
     - Check Dockerfile for any system dependencies  
     - Verify requirements.txt is up to date

3. **Container Startup Issues**
   - **Symptom**: Containers exit immediately or fail to start
   - **Solution**:  
     - Check container logs with `docker logs <container-name>`  
     - Ensure entrypoint.sh has execute permissions (chmod +x)  
     - Verify environment variables are properly set  
     - Check network connectivity between containers

4. **Network Issues**
   - **Symptom**: Containers can't communicate
   - **Solution**:  
     - Ensure containers are on the same network  
     - Check network exists: docker network ls  
     - Inspect network: docker network inspect user-management-network  
     - Try recreating the network if issues persist

## Development Best Practices

1. **Local Development**
   - Use the --reload flag with uvicorn (enabled by default in Docker)
   - Keep .env.example updated with new variables
   - Run tests before committing changes

2. **Database Migrations**
   - Create new migrations: `alembic revision --autogenerate -m "description"`
   - Apply migrations: `alembic upgrade head`
   - Rollback migrations: `alembic downgrade -1`

3. **Code Quality**
   - Run linters before committing
   - Keep dependencies updated
   - Follow FastAPI best practices for route organization

## Security Notes

1. **Environment Variables**
   - Never commit .env file
   - Use strong passwords in production
   - Rotate JWT secrets regularly

2. **Database**
   - Use strong PostgreSQL passwords
   - Regularly backup database
   - Keep PostgreSQL updated

3. **API Security**
   - Use HTTPS in production
   - Implement rate limiting
   - Keep dependencies updated

## Maintenance

1. **Logging**
   - Check container logs: `docker-compose logs -f`
   - Monitor API endpoints
   - Track database performance

2. **Updates**
   - Regularly update dependencies
   - Check for security advisories
   - Keep Docker images updated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License
