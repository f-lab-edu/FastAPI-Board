from uuid import uuid4, UUID

from pydantic import BaseModel, Field
from datetime import datetime


class PostBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


class Post(PostBase):
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)


class RequestPost(BaseModel):
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)


class ResponsePost(Post):
    pass
