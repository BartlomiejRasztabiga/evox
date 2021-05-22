from fastapi import HTTPException


class MessageNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Message with given id not found.")


class EmptyMessageContentException(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Message content cannot be empty.")


class MessageContentTooLongException(HTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Message content cannot exceed 160 characters.")
