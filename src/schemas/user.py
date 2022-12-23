from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    username: str
    # created_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


# class UserInDB(UserInDBBase):
#     password: str
