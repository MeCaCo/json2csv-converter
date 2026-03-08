from pydantic import BaseModel
from datetime import datetime

class ConversionBase(BaseModel):
    filename: str
    original_filename: str
    file_id: str
    file_size_mb: float
    status: str

class ConversionCreate(ConversionBase):
    pass

class Conversion(ConversionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True