from app.exceptions.message import (
    EmptyMessageContentException,
    MessageContentTooLongException,
)


def validate_message_content_length(content: str) -> None:
    """
    Raises EmptyMessageContentException if given message content is empty.
    Raises MessageContentTooLongException if given message content is too long (> 160 chars).
    """
    if not content:
        raise EmptyMessageContentException()
    if len(content) > 160:
        raise MessageContentTooLongException()
