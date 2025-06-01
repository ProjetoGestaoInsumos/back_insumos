from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal
from enum import Enum

class UserRole(str, Enum):
    admin = 'admin'
    tecnico = 'tecnico'
    professor = 'professor'
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True