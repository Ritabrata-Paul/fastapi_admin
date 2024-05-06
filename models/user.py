from pydantic import BaseModel
from typing import Optional
import bcrypt


# class User:
#     def __init__(self, username: str, email: str, password: str, user_id: Optional[str] = None):
#         self.username = username
#         self.email = email
#         self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # Hash password
#         self.user_id = user_id
# from pydantic import BaseModel
# from typing import Optional

class UserAccount(BaseModel):
    user_id: str
    user_name: str
    email: str
    password: str