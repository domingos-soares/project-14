# Person REST API

A RESTful API built with FastAPI for managing Person objects with full CRUD operations.

## Features

- **CREATE** - Add new persons
- **READ** - Get all persons or a specific person by ID
- **UPDATE** - Update person details
- **DELETE** - Remove persons from the database
- In-memory storage for quick development and testing
- Auto-generated interactive API documentation (Swagger UI)
- Data validation with Pydantic

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone this repository or navigate to the project directory

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the FastAPI server with:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`

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
- **Response**: Service health status with timestamp (200)

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
  "timestamp": "2025-12-01T12:05:30.123456"
}
```

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
│   ├── models/
│   │   ├── __init__.py
│   │   └── person.py        # Pydantic models for Person
│   ├── routes/
│   │   ├── __init__.py
│   │   └── person.py        # Person API endpoints
│   └── services/
│       ├── __init__.py
│       └── person_service.py # Business logic layer
├── requirements.txt         # Python dependencies
├── main.py.old             # Original monolithic file (backup)
└── README.md               # This file
```

### Architecture

The application follows a **layered architecture**:

- **Models** (`app/models/`) - Pydantic models for data validation and serialization
- **Services** (`app/services/`) - Business logic and data management
- **Routes** (`app/routes/`) - API endpoints that use services
- **Config** (`app/config.py`) - Centralized configuration management

## Development

The application uses in-memory storage, so all data will be lost when the server restarts. For production use, consider integrating a database like PostgreSQL, MongoDB, or SQLite.

## Testing

You can test the API using:
- The built-in Swagger UI at `/docs`
- cURL commands (examples above)
- Postman or similar API testing tools
- Python requests library

## License

MIT
small windsurf experiment
