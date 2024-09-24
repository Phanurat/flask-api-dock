from sqlalchemy import Column, Integer, String
from database import Base

class Content(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
