"""Person routes/endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, status

from app.models.person import Person, PersonResponse, PersonUpdate
from app.services.person_service import person_service

router = APIRouter(prefix="/persons", tags=["Persons"])


@router.post(
    "",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new person"
)
async def create_person(person: Person):
    """Create a new person.
    
    Args:
        person: Person data to create
        
    Returns:
        PersonResponse: Created person with generated ID
    """
    return person_service.create_person(person)


@router.get(
    "",
    response_model=List[PersonResponse],
    summary="Get all persons"
)
async def get_all_persons():
    """Get all persons from the database.
    
    Returns:
        List[PersonResponse]: List of all persons
    """
    return person_service.get_all_persons()


@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Get a specific person"
)
async def get_person(person_id: str):
    """Get a specific person by their ID.
    
    Args:
        person_id: The unique identifier of the person
        
    Returns:
        PersonResponse: The requested person
        
    Raises:
        HTTPException: 404 if person not found
    """
    person = person_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    return person


@router.put(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Update a person"
)
async def update_person(person_id: str, person_update: PersonUpdate):
    """Update a person's information.
    
    Args:
        person_id: The unique identifier of the person
        person_update: Fields to update
        
    Returns:
        PersonResponse: Updated person
        
    Raises:
        HTTPException: 404 if person not found, 400 if no fields to update
    """
    update_data = person_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    updated_person = person_service.update_person(person_id, person_update)
    if not updated_person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    return updated_person


@router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a person"
)
async def delete_person(person_id: str):
    """Delete a person by their ID.
    
    Args:
        person_id: The unique identifier of the person
        
    Raises:
        HTTPException: 404 if person not found
    """
    success = person_service.delete_person(person_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    return None
