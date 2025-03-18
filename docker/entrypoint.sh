#!/bin/bash

# Exit on error
set -e

# Function to check if PostgreSQL is ready
wait_for_postgres() {
    echo "Waiting for PostgreSQL..."
    while ! nc -z db 5432; do
        sleep 0.1
    done
    echo "PostgreSQL started"
}

# Function to run migrations
run_migrations() {
    echo "Running database migrations..."
    alembic upgrade head || {
        echo "Migration failed!"
        return 1
    }
    echo "Migrations completed successfully"
}

# Main execution
wait_for_postgres

# Try to run migrations
if ! run_migrations; then
    echo "Failed to run migrations. Check the database configuration and try again."
    exit 1
fi

# Start the application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
