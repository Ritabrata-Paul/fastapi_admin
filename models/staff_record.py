from pydantic import BaseModel
from typing import Optional

class StaffRecord(BaseModel):
    staff_id: str
    staff_name: str
    department: str
    role: Optional[str] = None