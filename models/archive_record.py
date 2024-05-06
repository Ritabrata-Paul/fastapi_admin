from pydantic import BaseModel
from typing import Optional

class ArchiveRecord(BaseModel):
    student_id: str
    archive_date: str
    reason: Optional[str] = None
    record_id: str
    course_id: Optional[str] = None
    grade: Optional[str] = None
    academic_year: str