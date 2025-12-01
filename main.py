from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Optional
from uuid import uuid4, UUID

app = FastAPI(title="Person API", version="1.0.0")

# In-memory storage for persons
persons_db: Dict[str, dict] = {}


# Pydantic models
class Person(BaseModel):
    name: str = Field(..., min_length=1, description="Person's name")
    age: int = Field(..., ge=0, le=150, description="Person's age")
    email: str = Field(..., description="Person's email address")
    phone: Optional[str] = Field(None, description="Person's phone number")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "age": 30,
                    "email": "john.doe@example.com",
                    "phone": "+1234567890"
                }
            ]
        }
    }


class PersonResponse(Person):
    id: str = Field(..., description="Unique identifier for the person")


class PersonUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Person's name")
    age: Optional[int] = Field(None, ge=0, le=150, description="Person's age")
    email: Optional[str] = Field(None, description="Person's email address")
    phone: Optional[str] = Field(None, description="Person's phone number")


# Routes
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to the Person API",
        "endpoints": {
            "GET /persons": "Get all persons",
            "GET /persons/{id}": "Get a specific person",
            "POST /persons": "Create a new person",
            "PUT /persons/{id}": "Update a person",
            "DELETE /persons/{id}": "Delete a person"
        }
    }


@app.post("/persons", response_model=PersonResponse, status_code=status.HTTP_201_CREATED, tags=["Persons"])
async def create_person(person: Person):
    """Create a new person"""
    person_id = str(uuid4())
    person_data = person.model_dump()
    person_data["id"] = person_id
    persons_db[person_id] = person_data
    return person_data


@app.get("/persons", response_model=list[PersonResponse], tags=["Persons"])
async def get_all_persons():
    """Get all persons"""
    return list(persons_db.values())


@app.get("/persons/{person_id}", response_model=PersonResponse, tags=["Persons"])
async def get_person(person_id: str):
    """Get a specific person by ID"""
    if person_id not in persons_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    return persons_db[person_id]


@app.put("/persons/{person_id}", response_model=PersonResponse, tags=["Persons"])
async def update_person(person_id: str, person_update: PersonUpdate):
    """Update a person by ID"""
    if person_id not in persons_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    
    stored_person = persons_db[person_id]
    update_data = person_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    for field, value in update_data.items():
        stored_person[field] = value
    
    persons_db[person_id] = stored_person
    return stored_person


@app.delete("/persons/{person_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Persons"])
async def delete_person(person_id: str):
    """Delete a person by ID"""
    if person_id not in persons_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    del persons_db[person_id]
    return None
