from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from schemas.base import BaseDataInfo, AuthMixin


class Post(BaseDataInfo, AuthMixin):
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
