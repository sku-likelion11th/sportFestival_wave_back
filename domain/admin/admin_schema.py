import datetime

from pydantic import BaseModel, validator
from typing import Optional



class Body(BaseModel):
    category: str
    team: str
    score: int
    result: Optional[str] = None