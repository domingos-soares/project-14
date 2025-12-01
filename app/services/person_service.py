"""Person service layer for business logic."""

from typing import Dict, List, Optional
from uuid import uuid4

from app.models.person import Person, PersonResponse, PersonUpdate


class PersonService:
    """Service class to handle person-related business logic."""
    
    def __init__(self):
        """Initialize the service with in-memory storage."""
        self._persons_db: Dict[str, dict] = {}
    
    def create_person(self, person: Person) -> PersonResponse:
        """Create a new person and return it with an ID.
        
        Args:
            person: Person data to create
            
        Returns:
            PersonResponse: Created person with generated ID
        """
        person_id = str(uuid4())
        person_data = person.model_dump()
        person_data["id"] = person_id
        self._persons_db[person_id] = person_data
        return PersonResponse(**person_data)
    
    def get_all_persons(self) -> List[PersonResponse]:
        """Get all persons from the database.
        
        Returns:
            List[PersonResponse]: List of all persons
        """
        return [PersonResponse(**person) for person in self._persons_db.values()]
    
    def get_person_by_id(self, person_id: str) -> Optional[PersonResponse]:
        """Get a person by their ID.
        
        Args:
            person_id: The unique identifier of the person
            
        Returns:
            Optional[PersonResponse]: The person if found, None otherwise
        """
        person_data = self._persons_db.get(person_id)
        if person_data:
            return PersonResponse(**person_data)
        return None
    
    def update_person(self, person_id: str, person_update: PersonUpdate) -> Optional[PersonResponse]:
        """Update a person's information.
        
        Args:
            person_id: The unique identifier of the person
            person_update: Fields to update
            
        Returns:
            Optional[PersonResponse]: Updated person if found, None otherwise
        """
        if person_id not in self._persons_db:
            return None
        
        stored_person = self._persons_db[person_id]
        update_data = person_update.model_dump(exclude_unset=True)
        
        # Update only the provided fields
        for field, value in update_data.items():
            stored_person[field] = value
        
        self._persons_db[person_id] = stored_person
        return PersonResponse(**stored_person)
    
    def delete_person(self, person_id: str) -> bool:
        """Delete a person by their ID.
        
        Args:
            person_id: The unique identifier of the person
            
        Returns:
            bool: True if person was deleted, False if not found
        """
        if person_id in self._persons_db:
            del self._persons_db[person_id]
            return True
        return False


# Singleton instance
person_service = PersonService()
