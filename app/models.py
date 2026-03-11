from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
import datetime

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    file_id = Column(String, unique=True, index=True)
    file_size_mb = Column(Float)
    status = Column(String, default="uploaded")
    csv_filename = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)