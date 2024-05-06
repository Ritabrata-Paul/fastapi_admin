from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    student_id: str
    name: str
    email: str
    program: str

class ArchiveRecordSummary(BaseModel):
    course_id: Optional[str] = None
    grade: Optional[str] = None