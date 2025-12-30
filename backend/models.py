from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    department = Column(String(100))
    district = Column(String(100))
    state = Column(String(100))
    email_sent_to = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
