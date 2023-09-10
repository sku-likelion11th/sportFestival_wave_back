import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int 
    email: str 
    student_num: int 
    name: str 
    phone_num: str 
    is_admin: bool 
    # game은 어떻게 할지 몰라서 안넣음
    
    class Config:
        from_attribute = True