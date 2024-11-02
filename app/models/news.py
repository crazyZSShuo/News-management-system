# class News(Base):
#     __tablename__ = "news"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), index=True, nullable=False)
#     content = Column(Text, nullable=False)
#     summary = Column(String(500))
#     status = Column(Enum(NewsStatus), default=NewsStatus.DRAFT, nullable=False)
#     category_id = Column(
#         Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
#     )
#     author_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     created_at = Column(DateTime, default=datetime.now, nullable=False)
#     updated_at = Column(
#         DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
#     )
#     published_at = Column(DateTime, nullable=True)
#
#     author = relationship("User", back_populates="news")
#     category = relationship("Category", back_populates="news")
#     tags = relationship(
#         "Tag",
#         secondary=news_tags,
#         back_populates="news",
#         # cascade="all"
#     )
#     comments = relationship(
#         "Comment", back_populates="news", cascade="all, delete-orphan"
#     )