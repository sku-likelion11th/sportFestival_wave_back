import datetime

from pydantic import BaseModel, validator
from typing import Optional


class Game(BaseModel):
    category: str
    start_time: datetime.datetime
    result: bool 
    video_url: str         
    score_A: int  
    score_B: int 
    place: str 
    team_A: str
    team_B: str

    
    class Config:
        from_attribute = True  # 'orm_mode' has been renamed to 'from_attributes'
        
@validator('games', pre=True, always=True, check_fields=False)
def validate_games(cls, value):
    if value is None:
        return []  # Return an empty list if games is None
    return value



class Game_score(BaseModel):
    result: Optional[bool] = None      
    score_A: int  
    score_B: int 


class Body(BaseModel):
    category: str
    predict: int

