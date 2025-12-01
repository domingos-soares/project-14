"""Person service layer for business logic."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.person import Person, PersonResponse, PersonUpdate
from app.db.models import PersonDB


class PersonService:
    """Service class to handle person-related business logic."""
    
    async def create_person(self, db: AsyncSession, person: Person) -> PersonResponse:
        """Create a new person and return it with an ID.
        
        Args:
            db: Database session
            person: Person data to create
            
        Returns:
            PersonResponse: Created person with generated ID
        """
        db_person = PersonDB(**person.model_dump())
        db.add(db_person)
        await db.flush()
        await db.refresh(db_person)
        
        return PersonResponse(
            id=str(db_person.id),
            name=db_person.name,
            age=db_person.age,
            email=db_person.email,
            phone=db_person.phone
        )
    
    async def get_all_persons(self, db: AsyncSession) -> List[PersonResponse]:
        """Get all persons from the database.
        
        Args:
            db: Database session
            
        Returns:
            List[PersonResponse]: List of all persons
        """
        result = await db.execute(select(PersonDB))
        persons = result.scalars().all()
        
        return [
            PersonResponse(
                id=str(person.id),
                name=person.name,
                age=person.age,
                email=person.email,
                phone=person.phone
            )
            for person in persons
        ]
    
    async def get_person_by_id(self, db: AsyncSession, person_id: str) -> Optional[PersonResponse]:
        """Get a person by their ID.
        
        Args:
            db: Database session
            person_id: The unique identifier of the person
            
        Returns:
            Optional[PersonResponse]: The person if found, None otherwise
        """
        try:
            person_uuid = UUID(person_id)
        except ValueError:
            return None
        
        result = await db.execute(select(PersonDB).where(PersonDB.id == person_uuid))
        person = result.scalar_one_or_none()
        
        if person:
            return PersonResponse(
                id=str(person.id),
                name=person.name,
                age=person.age,
                email=person.email,
                phone=person.phone
            )
        return None
    
    async def update_person(
        self, db: AsyncSession, person_id: str, person_update: PersonUpdate
    ) -> Optional[PersonResponse]:
        """Update a person's information.
        
        Args:
            db: Database session
            person_id: The unique identifier of the person
            person_update: Fields to update
            
        Returns:
            Optional[PersonResponse]: Updated person if found, None otherwise
        """
        try:
            person_uuid = UUID(person_id)
        except ValueError:
            return None
        
        result = await db.execute(select(PersonDB).where(PersonDB.id == person_uuid))
        person = result.scalar_one_or_none()
        
        if not person:
            return None
        
        update_data = person_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(person, field, value)
        
        await db.flush()
        await db.refresh(person)
        
        return PersonResponse(
            id=str(person.id),
            name=person.name,
            age=person.age,
            email=person.email,
            phone=person.phone
        )
    
    async def delete_person(self, db: AsyncSession, person_id: str) -> bool:
        """Delete a person by their ID.
        
        Args:
            db: Database session
            person_id: The unique identifier of the person
            
        Returns:
            bool: True if person was deleted, False if not found
        """
        try:
            person_uuid = UUID(person_id)
        except ValueError:
            return False
        
        result = await db.execute(select(PersonDB).where(PersonDB.id == person_uuid))
        person = result.scalar_one_or_none()
        
        if person:
            await db.delete(person)
            return True
        return False


# Singleton instance
person_service = PersonService()
