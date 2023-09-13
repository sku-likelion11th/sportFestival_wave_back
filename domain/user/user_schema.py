import datetime
from typing import Dict, Any
from pydantic import BaseModel, validator


class User(BaseModel):
    id: int 
    email: str 
    student_num: int 
    name: str 
    phone_num: str 
    is_admin: bool 
    games: Dict[str, Any] = {}
    
    class Config:
        from_attribute = True
        
@validator('users', pre=True, always=True, check_fields=False)
def validate_users(cls, value):
    if value is None:
        return []  # Return an empty list if games is None
    return value