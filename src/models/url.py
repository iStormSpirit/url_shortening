from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from db.db import Base


class ShortUrl(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    short_url = Column(String)
    original_url = Column(String)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    # is_private = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(50), primary_key=True)
#     password = Column(String(100))
