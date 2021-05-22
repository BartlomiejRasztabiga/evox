from typing import Optional

from pydantic.main import BaseModel


# Shared properties
class MessageBase(BaseModel):
    content: str
    views_count: int


# Properties to receive via API on creation
class MessageBaseCreateDto:
    content: str


# Properties to receive via API on update
class MessageBaseUpdateDto:
    content: str


class MessageBaseInDBBase(MessageBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Message(MessageBaseInDBBase):
    pass


# Additional properties stored in DB
class MessageInDB(MessageBaseInDBBase):
    pass
