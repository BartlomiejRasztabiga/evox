import pytest
from sqlalchemy.orm import Session

from app import services
from app.exceptions.message import (
    EmptyMessageContentException,
    MessageContentTooLongException,
    MessageNotFoundException,
)
from app.schemas import MessageCreateDto
from app.schemas.message import MessageUpdateDto
from app.tests.utils.utils import random_string


def test_given_new_message_when_create_message_then_will_create_one(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content=random_string(32))

    # when
    message = services.messages.create(db, message_create_dto)

    # then
    assert message.id is not None
    assert message.content == message_create_dto.content
    assert message.views_count == 0


def test_given_existing_message_when_increase_view_count_by_id_then_will_return_one_and_increase_view_count(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content=random_string(32))
    message = services.messages.create(db, message_create_dto)

    # when
    existing_message = services.messages.increment_view_count_by_id(db, message.id)

    # then
    assert existing_message is not None
    assert existing_message.id is not None
    assert existing_message.content == message_create_dto.content
    assert existing_message.views_count == 1


def test_given_existing_message_when_multiple_get_by_id_then_will_increase_view_count_accordingly(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content=random_string(32))
    message = services.messages.create(db, message_create_dto)

    # when
    services.messages.increment_view_count_by_id(db, message.id)
    services.messages.increment_view_count_by_id(db, message.id)
    services.messages.increment_view_count_by_id(db, message.id)

    # then
    existing_message = services.messages.get_by_id(db, message.id)
    assert existing_message is not None
    assert existing_message.views_count == 3


def test_no_message__when_get_by_id_then_will_throw_exception(
    db: Session,
) -> None:
    # when
    with pytest.raises(MessageNotFoundException):
        services.messages.get_by_id(db, 99999)


def test_given_new_message_with_empty_content_when_create_new_then_will_throw_exception(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content="")

    # when
    with pytest.raises(EmptyMessageContentException):
        services.messages.create(db, message_create_dto)


def test_given_new_message_with_content_longer_than_160_when_create_new_then_will_throw_exception(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content=random_string(161))

    # when
    with pytest.raises(MessageContentTooLongException):
        services.messages.create(db, message_create_dto)


def test_given_existing_message_when_update_by_id_then_will_update_one_and_reset_view_count(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content=random_string(32))
    existing_message = services.messages.create(db, message_create_dto)

    # increase view count
    services.messages.get_by_id(db, existing_message.id)

    # when
    message_update_dto = MessageUpdateDto(content=random_string(64))
    updated_message = services.messages.update_by_id(
        db, existing_message.id, message_update_dto
    )

    # then
    assert updated_message is not None
    assert updated_message.id is existing_message.id
    assert updated_message.content == message_update_dto.content
    assert updated_message.views_count == 0


def test_given_existing_message_when_delete_by_id_then_will_delete_one(
    db: Session,
) -> None:
    # given
    message_create_dto = MessageCreateDto(content=random_string(32))
    existing_message = services.messages.create(db, message_create_dto)

    # when
    services.messages.delete_by_id(db, existing_message.id)

    # then
    with pytest.raises(MessageNotFoundException):
        services.messages.get_by_id(db, existing_message.id)
