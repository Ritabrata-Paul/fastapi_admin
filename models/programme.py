from pydantic import BaseModel
from typing import Optional, List

class Course(BaseModel):
    Cource_id: str
    title: str
    description: Optional[str] = None

class Programme(BaseModel):
    programme_id: str
    title: str
    description: Optional[str] = None
    courses: List[Course]