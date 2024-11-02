# from sqlalchemy import (
#     Boolean,
#     Column,
#     ForeignKey,
#     Integer,
#     String,
#     Text,
#     DateTime,
#     Table,
#     Enum,
# )
# from sqlalchemy.orm import relationship, declarative_base
# from datetime import datetime
# import enum
#
# Base = declarative_base()
#
#
# # 多对多关联表：新闻-标签
# news_tags = Table(
#     "news_tags",
#     Base.metadata,
#     Column("news_id", Integer, ForeignKey("news.id", ondelete="CASCADE")),
#     Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
# )
#
#
# # 修改1：使用enum.Enum而不是str, enum.Enum
# class NewsStatus(enum.Enum):
#     DRAFT = "draft"
#     PUBLISHED = "published"
#     ARCHIVED = "archived"
#
#
# class Role(enum.Enum):
#     ADMIN = "admin"
#     EDITOR = "editor"
#     WRITER = "writer"
#     USER = "user"
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(100), unique=True, index=True, nullable=False)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     hashed_password = Column(String(100), nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     # 修改2：移除.value，直接使用Role.USER
#     role = Column(Enum(Role), default=Role.USER, nullable=False)
#     created_at = Column(DateTime, default=datetime.now, nullable=False)
#
#     news = relationship("News", back_populates="author", cascade="all, delete-orphan")
#     comments = relationship(
#         "Comment", back_populates="author", cascade="all, delete-orphan"
#     )
#
#
# class Category(Base):
#     __tablename__ = "categories"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), unique=True, index=True, nullable=False)
#     description = Column(String(200))
#
#     # 修改3：添加cascade配置
#     news = relationship("News", back_populates="category", cascade="all, delete-orphan")
#
#
# class Tag(Base):
#     __tablename__ = "tags"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(30), unique=True, index=True, nullable=False)
#
#     # 修改4：修复多对多关系的back_populates配置
#     news = relationship(
#         "News",
#         secondary=news_tags,
#         back_populates="tags",
#         # cascade="all"
#     )
#
#
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
#
#
# class Comment(Base):
#     __tablename__ = "comments"
#
#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(Text, nullable=False)
#     news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
#     author_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     parent_id = Column(
#         Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
#     )
#     created_at = Column(DateTime, default=datetime.now, nullable=False)
#     updated_at = Column(
#         DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
#     )
#     is_deleted = Column(Boolean, default=False, nullable=False)
#
#     news = relationship("News", back_populates="comments")
#     author = relationship("User", back_populates="comments")
#     # 修改5：修复自引用关系的定义
#     parent = relationship("Comment", remote_side=[id], backref="replies")
