from pydantic import BaseModel
from typing import Optional

class AccessRecord(BaseModel):
    user_id: str
    resource_id: str
    access_status: bool