from pydantic import BaseModel


class Major(BaseModel):
    id: int 
    name: str 
    slogan: str 
    image: str 
    
    class Config:
        from_attribute = True