"""Person routes/endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person, PersonResponse, PersonUpdate
from app.services.person_service import person_service
from app.db import get_db

router = APIRouter(prefix="/persons", tags=["Persons"])


@router.post(
    "",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new person"
)
async def create_person(person: Person, db: AsyncSession = Depends(get_db)):
    """Create a new person.
    
    Args:
        person: Person data to create
        db: Database session
        
    Returns:
        PersonResponse: Created person with generated ID
    """
    return await person_service.create_person(db, person)


@router.get(
    "",
    response_model=List[PersonResponse],
    summary="Get all persons"
)
async def get_all_persons(db: AsyncSession = Depends(get_db)):
    """Get all persons from the database.
    
    Args:
        db: Database session
        
    Returns:
        List[PersonResponse]: List of all persons
    """
    return await person_service.get_all_persons(db)


@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Get a specific person"
)
async def get_person(person_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific person by their ID.
    
    Args:
        person_id: The unique identifier of the person
        db: Database session
        
    Returns:
        PersonResponse: The requested person
        
    Raises:
        HTTPException: 404 if person not found
    """
    person = await person_service.get_person_by_id(db, person_id)
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
async def update_person(person_id: str, person_update: PersonUpdate, db: AsyncSession = Depends(get_db)):
    """Update a person's information.
    
    Args:
        person_id: The unique identifier of the person
        person_update: Fields to update
        db: Database session
        
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
    
    updated_person = await person_service.update_person(db, person_id, person_update)
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
async def delete_person(person_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a person by their ID.
    
    Args:
        person_id: The unique identifier of the person
        db: Database session
        
    Raises:
        HTTPException: 404 if person not found
    """
    success = await person_service.delete_person(db, person_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with ID {person_id} not found"
        )
    return None
