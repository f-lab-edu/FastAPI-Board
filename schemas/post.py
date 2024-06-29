from uuid import uuid4, UUID

from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime, timezone


def _default_time():
    return datetime.now(timezone.utc)


def _change_local_time(time: datetime):
    return time.astimezone()


class PostBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=_default_time)
    updated_at: datetime = Field(default_factory=_default_time)


class Post(PostBase):
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)


class RequestPost(BaseModel):
    author: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=5, max_length=50)
    content: str = Field(min_length=1)


class ResponsePost(Post):
    @field_validator('created_at', 'updated_at')
    def _change_local_time(cls, time: datetime):
        return time.astimezone()
