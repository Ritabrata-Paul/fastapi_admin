from pydantic import BaseModel
from typing import Optional

class Teacher(BaseModel):
    teacher_id: str
    teacher_name: str
    email: str
    department: Optional[str] = None