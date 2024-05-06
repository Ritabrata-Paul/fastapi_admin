from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserIn(UserBase):
    pass

class UserOut(UserBase):
    user_id: str

    class Config:
        orm_mode = True
