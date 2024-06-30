from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field, BaseModel


def _default_time():
    return datetime.now(timezone.utc)


def _change_local_time(time: datetime):
    return time.astimezone()


class BaseDataInfo(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=_default_time)
    updated_at: datetime = Field(default_factory=_default_time)


class AuthMixin(BaseModel):
    token: Annotated[str, Field(exclude=True)]
