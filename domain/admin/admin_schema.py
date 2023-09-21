import datetime

from pydantic import BaseModel, validator
from typing import Optional



class Body(BaseModel):
    category: str
    predict_team: int
    score: int
    
