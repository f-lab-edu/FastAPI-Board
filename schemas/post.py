from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from schemas.base import AuthMixin, TimeMixin


class Post(AuthMixin, TimeMixin):
    id: UUID = Field(default_factory=uuid4)
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)


class CreatePost(BaseModel):
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)


class UpdatePost(BaseModel):
    author: Optional[str] = Field(min_length=1, max_length=20, default=None)
    title: Optional[str] = Field(min_length=5, max_length=50, default=None)
    content: Optional[str] = Field(min_length=1, default=None)


class ResponsePost(Post):
    @field_validator('created_at', 'updated_at')
    def _change_local_time(cls, time: datetime):
        return time.astimezone()
