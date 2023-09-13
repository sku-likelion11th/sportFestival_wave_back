import datetime

from pydantic import BaseModel, validator


class Game(BaseModel):
    id: int 
    start_time: datetime.datetime
    result: bool 
    video_url: str         
    score_A: int  
    score_B: int 
    place: str 
    team_A: str
    team_B: str
    category: str 
    user_id: int 
    
    class Config:
        from_attribute = True  # 'orm_mode' has been renamed to 'from_attributes'
        
@validator('games', pre=True, always=True, check_fields=False)
def validate_games(cls, value):
    if value is None:
        return []  # Return an empty list if games is None
    return value
