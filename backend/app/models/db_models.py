from sqlalchemy import Column, Integer, String, Float, DateTime
from ..database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # Strava Athlete ID
    firstname = Column(String)
    lastname = Column(String)
    profile = Column(String, nullable=True)
    sex = Column(String, default="M")
    birthday = Column(DateTime, nullable=True)
    
    # OAuth Tokens
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(Integer) # Unix timestamp
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
