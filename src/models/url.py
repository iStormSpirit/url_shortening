from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from db.db import Base


class ShortUrl(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    # title = Column(String(50))
    short_url = Column(String)
    original_url = Column(String)
    usage_count = Column(Integer, default=0)
    # public = Column(Boolean, default=True)
    # archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # private = Column(Boolean, default=False)
