import uuid
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field 

class User(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(gt=18)
    
