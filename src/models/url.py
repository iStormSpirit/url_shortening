from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    urls_list = relationship("ShortUrl")


class ShortUrl(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    short_url = Column(String)
    original_url = Column(String)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_private = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
