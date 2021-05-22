from sqlalchemy.orm import Session

from app import models, services
from app.schemas import MessageCreateDto
from app.tests.utils import random_string


def get_test_message_create_dto() -> MessageCreateDto:
    message_create_dto = MessageCreateDto(
        content=random_string(32)
    )
    return message_create_dto


def create_test_message(db: Session) -> models.Message:
    message_create_dto = get_test_message_create_dto()
    return services.messages.create(db=db, message_create_dto=message_create_dto)
