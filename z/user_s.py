# from datetime import datetime
# from schemas.url import Url
# from pydantic import BaseModel
#
#
# class UserBase(BaseModel):
#     username: str
#     email: str
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class UserUpdate(UserBase):
#     pass
#
#
# class UserInDBBase(UserBase):
#     id: int
#     username: str
#     created_at: datetime
#     urls: list[Url] = []
#
#     class Config:
#         orm_mode = True
#
#
# class User(UserInDBBase):
#     pass
