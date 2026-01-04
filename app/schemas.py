from uuid import UUID
from pydantic import BaseModel, EmailStr, Field 

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(gt=18)

class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    age: int
    
    class ConfigDict:
        from_attributes = True 