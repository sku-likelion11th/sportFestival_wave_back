from sqlalchemy import Column, Integer, String, Text, DateTime, TupleType, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    student_num = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    phone_num = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    games = Column(JSON, nullable=True)
    

class Game(Base):
    __tablename__ = 'game'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    result = Column(Boolean, nullable=True)
    video_url = Column(String(255), nullable=False)           
    score_A = Column(Integer)    
    score_B = Column(Integer)  
    place = Column(String(255), nullable=False)
    team_A = Column(String(255), nullable=False)
    team_B = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    
    user = relationship("User", backref="game")
    

class Major(Base):
    __tablename__ = 'major'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    slogan = Column(Text, nullable=False)
    image = Column(Text, nullable=False) # How to show the image(by statics?)