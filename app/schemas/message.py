from typing import Optional

from pydantic.main import BaseModel


# Shared properties
class MessageBase(BaseModel):
    content: str


# Properties to receive via API on creation
class MessageBaseCreateDto(MessageBase):
    pass


class MessageBaseUpdateDto(MessageBase):
    pass


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
