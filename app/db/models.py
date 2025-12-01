"""SQLAlchemy database models."""

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class PersonDB(Base):
    """Person database model."""
    
    __tablename__ = "persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Person(id={self.id}, name={self.name}, email={self.email})>"
