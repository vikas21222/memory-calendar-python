from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)