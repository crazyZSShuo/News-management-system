# from pydantic import BaseModel, EmailStr, Field, field_validator
# from datetime import datetime
# from typing import Optional, Generic, TypeVar, Any, List
# from app.models import NewsStatus, Role
#
# T = TypeVar("T")
#
#
# class UserBase(BaseModel):
#     email: EmailStr
#     username: str = Field(..., min_length=3, max_length=50)
#
#
# class UserCreate(UserBase):
#     password: str = Field(..., min_length=6, max_length=50)
#     role: Optional[Role] = Field(default=Role.USER.value)
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     role: Role
#     created_at: datetime
#
#     class Config:
#         from_attributes = True
#
#
# class CategoryBase(BaseModel):
#     name: str = Field(..., min_length=1, max_length=50)
#     description: Optional[str] = Field(None, max_length=200)
#
#
# class CategoryCreate(CategoryBase):
#     pass
#
#
# class Category(CategoryBase):
#     id: int
#
#     class Config:
#         from_attributes = True
#
#
# class TagBase(BaseModel):
#     name: str = Field(..., min_length=1, max_length=30)
#
#
# class TagCreate(TagBase):
#     pass
#
#
# class Tag(TagBase):
#     id: int
#
#     class Config:
#         from_attributes = True
#
#
# class CommentBase(BaseModel):
#     content: str = Field(..., min_length=1)
#     parent_id: Optional[int] = None
#
#
# class CommentCreate(CommentBase):
#     news_id: int
#
#
# class Comment(CommentBase):
#     id: int
#     author_id: int
#     news_id: int
#     created_at: datetime
#     updated_at: datetime
#     is_deleted: bool
#
#     class Config:
#         from_attributes = True
#
#
# class NewsBase(BaseModel):
#     title: str = Field(..., min_length=1, max_length=200)
#     content: str = Field(..., min_length=1)
#     summary: Optional[str] = Field(None, max_length=500)
#     category_id: int
#     status: NewsStatus = Field(default=NewsStatus.DRAFT)
#
#     @field_validator("title")
#     @classmethod
#     def title_must_not_contain_html(cls, v):
#         if "<" in v or ">" in v:
#             raise ValueError("Title must not contain HTML tags")
#         return v
#
#     @field_validator("content")
#     @classmethod
#     def content_must_not_be_empty(cls, v):
#         if not v.strip():
#             raise ValueError("Content must not be empty")
#         return v
#
#
# class NewsCreate(NewsBase):
#     tags: List[int] = []
#
#
# class NewsUpdate(NewsBase):
#     title: Optional[str] = None
#     content: Optional[str] = None
#     category_id: Optional[int] = None
#     tags: Optional[List[int]] = None
#     status: Optional[NewsStatus] = None
#
#
# class News(NewsBase):
#     id: int
#     author_id: int
#     created_at: datetime
#     updated_at: datetime
#     published_at: Optional[datetime]
#     category: Category
#     tags: List[Tag]
#     author: User
#
#     class Config:
#         from_attributes = True
#
#
# class NewsSearchParams(BaseModel):
#     keyword: Optional[str] = None
#     category_id: Optional[int] = None
#     tag_ids: Optional[List[int]] = None
#     status: Optional[NewsStatus] = None
#     author_id: Optional[int] = None
#     start_date: Optional[datetime] = None
#     end_date: Optional[datetime] = None
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     email: Optional[str] = None
#
#
# class ResponseBase(BaseModel, Generic[T]):
#     code: int = Field(default=200, description="业务状态码")
#     message: str = Field(default="Success", description="响应信息")
#     data: Optional[T] = Field(default=None, description="响应数据")
#
#     class Config:
#         json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}
