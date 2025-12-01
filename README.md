# Person REST API

A RESTful API built with FastAPI for managing Person objects with full CRUD operations.

## Features

- **CREATE** - Add new persons
- **READ** - Get all persons or a specific person by ID
- **UPDATE** - Update person details
- **DELETE** - Remove persons from the database
- **PostgreSQL database** for persistent data storage
- **Database healthcheck** endpoint for monitoring
- **Async operations** with SQLAlchemy 2.0 and asyncpg
- Auto-generated interactive API documentation (Swagger UI)
- Data validation with Pydantic
- Docker support for easy database setup

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL 12+ (or Docker to run PostgreSQL in a container)
- Docker and Docker Compose (optional, for easy database setup)

## Installation

### Option 1: Using Docker (Recommended)

1. Clone this repository or navigate to the project directory

2. Start PostgreSQL using Docker Compose:
```bash
docker-compose up -d
```

3. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. (Optional) Copy the environment file and customize:
```bash
cp .env.example .env
```

### Option 2: Using Local PostgreSQL

1. Install PostgreSQL on your system

2. Create a database:
```bash
createdb person_db
```

3. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Configure database connection:
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your PostgreSQL credentials:
   ```
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/person_db
   ```

## Running the Server

1. Ensure PostgreSQL is running (via Docker or locally)

2. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The server will:
- Start at `http://127.0.0.1:8000`
- Automatically create database tables on startup
- Verify database connectivity

**Note**: The database tables are created automatically when the application starts. You don't need to run migrations manually.

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Person Model
```json
{
  "name": "string",
  "age": 0,
  "email": "string",
  "phone": "string (optional)"
}
```

### Available Routes

#### 0. Healthcheck
- **GET** `/health`
- **Response**: Service health status with database connectivity (200)

Example:
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

Response:
```json
{
  "status": "healthy",
  "service": "Person REST API",
  "version": "1.0.0",
  "timestamp": "2025-12-01T12:05:30.123456",
  "database": {
    "status": "healthy",
    "database": "connected"
  }
}
```

**Note**: If the database is unavailable, the overall status will be "unhealthy" and database details will include error information.

#### 1. Create a Person
- **POST** `/persons`
- **Body**: Person object (without ID)
- **Response**: Created person with generated ID (201)

Example:
```bash
curl -X POST "http://127.0.0.1:8000/persons" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "phone": "+1234567890"
  }'
```

#### 2. Get All Persons
- **GET** `/persons`
- **Response**: Array of all persons (200)

Example:
```bash
curl -X GET "http://127.0.0.1:8000/persons"
```

#### 3. Get a Specific Person
- **GET** `/persons/{person_id}`
- **Response**: Person object (200) or 404 if not found

Example:
```bash
curl -X GET "http://127.0.0.1:8000/persons/{person_id}"
```

#### 4. Update a Person
- **PUT** `/persons/{person_id}`
- **Body**: Fields to update (partial update supported)
- **Response**: Updated person object (200) or 404 if not found

Example:
```bash
curl -X PUT "http://127.0.0.1:8000/persons/{person_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "phone": "+9876543210"
  }'
```

#### 5. Delete a Person
- **DELETE** `/persons/{person_id}`
- **Response**: 204 No Content or 404 if not found

Example:
```bash
curl -X DELETE "http://127.0.0.1:8000/persons/{person_id}"
```

## Project Structure

```
project-14/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application setup
│   ├── config.py            # Application configuration
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy declarative base
│   │   ├── database.py      # Database connection & session
│   │   └── models.py        # SQLAlchemy database models
│   ├── models/
│   │   ├── __init__.py
│   │   └── person.py        # Pydantic models for validation
│   ├── routes/
│   │   ├── __init__.py
│   │   └── person.py        # Person API endpoints
│   └── services/
│       ├── __init__.py
│       └── person_service.py # Business logic layer
├── docker-compose.yml       # Docker setup for PostgreSQL
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── main.py.old            # Original monolithic file (backup)
└── README.md              # This file
```

### Architecture

The application follows a **layered architecture** with async database support:

- **Database** (`app/db/`) - SQLAlchemy models, async engine, and session management
- **Models** (`app/models/`) - Pydantic models for data validation and serialization
- **Services** (`app/services/`) - Business logic with async database operations
- **Routes** (`app/routes/`) - API endpoints with dependency injection
- **Config** (`app/config.py`) - Centralized configuration with environment variables

## Development

### Database

The application uses **PostgreSQL** for data persistence with the following features:
- **Async operations** using SQLAlchemy 2.0 and asyncpg
- **Automatic table creation** on application startup
- **UUID-based primary keys** for better scalability
- **Database health monitoring** through the `/health` endpoint

### Environment Variables

Configure the application using environment variables in `.env`:
- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_ECHO` - Enable SQL query logging (default: False)
- `DEBUG` - Enable debug mode (default: False)

### Docker Commands

```bash
# Start PostgreSQL
docker-compose up -d

# Stop PostgreSQL
docker-compose down

# View logs
docker-compose logs -f

# Remove all data (destructive!)
docker-compose down -v
```

## Testing

You can test the API using:
- The built-in Swagger UI at `/docs`
- cURL commands (examples above)
- Postman or similar API testing tools
- Python requests library

## License

MIT
small windsurf experiment
