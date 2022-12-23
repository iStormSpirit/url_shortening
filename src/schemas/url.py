from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UrlBase(BaseModel):
    pass


class UrlCreate(BaseModel):
    original_url: HttpUrl


class UrlId(BaseModel):
    id: int


class UrlShort(UrlId):
    short_url: HttpUrl

    class Config:
        orm_mode = True


class UrlOriginal(UrlId):
    original_url: HttpUrl

    class Config:
        orm_mode = True


class UrlStatus(UrlId):
    short_url: HttpUrl
    original_url: HttpUrl
    usage_count: int

    class Config:
        orm_mode = True


class UrlInDBase(UrlBase):
    id: int
    short_url: HttpUrl
    original_url: HttpUrl
    usage_count: int
    created_at: datetime
    is_archived: bool

    # is_private: bool
    # owner: str | None

    class Config:
        orm_mode = True


# class UrlByUser(UrlInDBase):
#     id: int
#     short_url: HttpUrl
#     original_url: HttpUrl
#     usage_count: int
#     created_at: datetime
#     is_private: bool
#
#     class Config:
#         orm_mode = True
