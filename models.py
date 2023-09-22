from sqlalchemy import Column, Integer, String, Text, DateTime, TupleType, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'
    
    email = Column(String(255), primary_key=True)
    student_num = Column(String(8), nullable=True)
    name = Column(String(255), nullable=True)
    phone_num = Column(String(255), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    games = Column(JSON, nullable=True)

    # session = Column(Text, nullable=True)
    

class Game(Base):
    __tablename__ = 'game'
    
    category = Column(String(255), primary_key=True)
    is_start = Column(Boolean, nullable=False, default=False)
    start_time = Column(DateTime, nullable=True)
    result = Column(Integer, nullable=True)
    video_url = Column(String(255), nullable=True)           
    score_A = Column(Integer)    
    score_B = Column(Integer)  
    place = Column(String(255), nullable=True)
    team_A = Column(String(255), nullable=False)
    team_B = Column(String(255), nullable=False)

