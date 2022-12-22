from datetime import datetime

from pydantic import BaseModel


class UrlBase(BaseModel):
    pass


class UrlCreate(BaseModel):
    original_url: str


class UrlId(BaseModel):
    id: int


class UrlShort(UrlId):
    short_url: str

    class Config:
        orm_mode = True


class UrlOriginal(UrlId):
    original_url: str

    class Config:
        orm_mode = True

# class UrlInDBase(UrlBase):
#     id: int
#     short_url: str
#     # original_url: str
#     # usage_count: int
#     created_at: datetime
#
#     # public: bool = True
#     # owner: str | None
#
#     class Config:
#         orm_mode = True
#
#
# class Url(UrlInDBase):
#     pass
