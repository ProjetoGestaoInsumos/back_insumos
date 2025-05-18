from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal['admin', 'técnico', 'professor']
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        roles = ['admin', 'técnico', 'professor']
        if v not in roles:
            raise ValueError('Role inválida. Escolha entre: admin, técnico ou professor.')
        return v
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