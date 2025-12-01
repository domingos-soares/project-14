"""Person data models."""

from pydantic import BaseModel, Field
from typing import Optional


class Person(BaseModel):
    """Person base model for creating persons."""
    
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
    """Person response model with ID."""
    
    id: str = Field(..., description="Unique identifier for the person")


class PersonUpdate(BaseModel):
    """Person update model for partial updates."""
    
    name: Optional[str] = Field(None, min_length=1, description="Person's name")
    age: Optional[int] = Field(None, ge=0, le=150, description="Person's age")
    email: Optional[str] = Field(None, description="Person's email address")
    phone: Optional[str] = Field(None, description="Person's phone number")
