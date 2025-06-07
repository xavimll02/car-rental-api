# Car Rental API

A RESTful API service for managing car rentals, built with FastAPI.

## Overview

This project implements a car rental service API that allows users to:
- List available cars for specific dates (I've also added the possibility to create cars)
- Create bookings for cars across multiple days
- Manage car rental data through a simple file-based storage system

## Architecture

The application follows a layered architecture pattern to ensure separation of concerns and maintainability:

- **Presentation Layer**: FastAPI routers handling HTTP requests and responses
- **Service Layer**: Business logic implementation
- **Repository Layer**: Data access and persistence using JSON files
- **Domain Layer**: Core business entities and models

This architectural approach allows for:
- Easy testing of individual components
- Simple future modifications (e.g., switching to a database)
- Clear separation of responsibilities
- Better code organization and maintainability

## Technical Stack

- **Framework**: FastAPI
- **Language**: Python 3.13
- **Storage**: JSON files (temporary solution, planned migration to PostgreSQL)
- **Testing**: pytest for both unit and integration tests
- **Documentation**: OpenAPI/Swagger
- **Containerization**: Docker
- **Logging**: Python's built-in logging module

## Getting Started

### Running with Docker

1. Build the Docker image:
```bash
docker build -t car-rental-api .
```

2. Run the container mounting your local data directory:
```bash
# For Windows (PowerShell)
docker run -p 8000:8000 -v "${PWD}/data:/app/data" car-rental-api

# For Linux/macOS
docker run -p 8000:8000 -v "$(pwd)/data:/app/data" car-rental-api
```

This setup mounts your local `data` directory into the container, so all data will be stored directly in your local filesystem. This makes it easy to:
- Access and backup your data files directly from your local machine
- Persist data between container restarts
- Share the same data between local development and Docker environments

### Running Locally

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Testing

The project includes both unit and integration tests covering the main services:
- Car availability service
- Booking service

Tests cover various scenarios including:
- Successful car bookings
- Booking conflicts
- Date validation
- Car availability checks

To run the tests (includes coverage report):
```bash
pytest
```

## API Documentation

The API documentation is available through Swagger UI when the application is running:
- Access the interactive OpenAPI documentation at: `http://localhost:8000/docs`
- The OpenAPI specification file is available in the `docs` directory

## Design Decisions

1. **Multi-day Bookings**: The system allows booking cars for multiple days to provide more flexibility to users.

2. **File-based Storage**: Currently using JSON files for data persistence as a simple solution. This makes the application easy to set up and test, though it's not suitable for production.

3. **Comprehensive Testing**: Both integration and unit tests are implemented to ensure reliability and catch potential issues early.

## Future Improvements

1. **Enhanced Logging**:
   - Implement more detailed and structured logging
   - Add log rotation and better formatting

2. **Exception Handling**:
   - Create a centralized exception handler
   - Implement custom JSON error responses
   - Move error handling from routers to dedicated middleware

3. **Database Integration**:
   - Migrate from JSON files to PostgreSQL
   - Implement database migrations
   - Add Docker Compose for easy database deployment

4. Additional potential improvements:
   - Implement user authentication and authorization
   - Add rate limiting for API endpoints
   - Implement caching for frequently accessed data
   - Add input validation middleware
   - Implement booking cancellation functionality