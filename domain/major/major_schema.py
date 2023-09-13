from pydantic import BaseModel, validator


class Major(BaseModel):
    id: int 
    name: str 
    slogan: str 
    image: str 
    
    class Config:
        from_attribute = True
        
@validator('majors', pre=True, always=True, check_fields=False)
def validate_majors(cls, value):
    if value is None:
        return []  # Return an empty list if games is None
    return value