import datetime
from typing import Dict, Any
from pydantic import BaseModel


class User(BaseModel):
    id: int 
    email: str 
    student_num: int 
    name: str 
    phone_num: str 
    is_admin: bool 
    game: Dict
    
    class Config:
        from_attribute = True