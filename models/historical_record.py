from pydantic import BaseModel
from typing import Optional

class HistoricalRecord(BaseModel):
    student_id: str
    academic_year: str
    gpa: float
    achievements: Optional[str]