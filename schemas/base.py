from datetime import datetime, timezone
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


def _default_time():
    return datetime.now(timezone.utc)


def _change_local_time(time: datetime):
    return time.astimezone()


class ResponseModel(BaseModel, Generic[T]):
    count: int
    items: list[T]


class TimeMixin(BaseModel):
    created_at: datetime = Field(default_factory=_default_time)
    updated_at: datetime = Field(default_factory=_default_time)


class AuthMixin(BaseModel):
    token: Annotated[str, Field(exclude=True)]
