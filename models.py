from sqlalchemy import Column, Integer, String, Text, DateTime, TupleType, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    student_num = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    phone_num = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    games = Column(JSON, nullable=True)
    

class Game(Base):
    __tablename__ = 'game'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    result = Column(Boolean, nullable=True)
    video_url = Column(String, nullable=False)           
    score_A = Column(Integer, primary_key=True)    
    score_B = Column(Integer, primary_key=True)  
    place = Column(String, nullable=False)
    team_A = Column(String, nullable=False)
    team_B = Column(String, nullable=False)
    category = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    
    user = relationship("User", backref="game")
    

class Major(Base):
    name = Column(String, primary_key=True, nullable=False)
    slogan = Column(Text, nullable=False)
    image = Column(Text, nullable=False) # How to show the image(by statics?)