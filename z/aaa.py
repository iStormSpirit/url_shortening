# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True)
#     password = Column(String(100))
#     email = Column(String(50), unique=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     urls = Column(ForeignKey("urls.id", ondelete='CASCADE'))

# urls = relationship("ShortUrl", back_populates="owner")


# owner = Column(ForeignKey('user.id'))

# owner_id = Column(Integer, ForeignKey('users.id'))
# owner = relationship("User", back_populates="urls")