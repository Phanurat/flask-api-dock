from typing import Optional
from pydantic import BaseModel

class ContentCreate(BaseModel):
    content: str
    
class ContentUpdate(BaseModel):
    content: Optional[str] = None

class Contents(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True
