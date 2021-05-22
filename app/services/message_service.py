from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.exceptions.message import MessageNotFoundException
from app.models import Message
from app.schemas import MessageCreateDto
from app.schemas.message import MessageUpdateDto
from app.validators.message import validate_message_content_length


class MessageService:
    def get_by_id(self, db: Session, _id: int) -> Message:
        message = db.query(Message).get(_id)

        # throw 404 if there is no message with given id
        if message is None:
            raise MessageNotFoundException()

        return message

    def create(self, db: Session, message_create_dto: MessageCreateDto) -> Message:
        # validate message content length (not empty, not > 160 chars)
        validate_message_content_length(message_create_dto.content)

        # create model object from message_create_dto
        message_obj = jsonable_encoder(message_create_dto)
        message = Message(**message_obj)

        # save object to db, commit session and refresh object with set id
        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def update_by_id(
        self, db: Session, _id: int, message_update_dto: MessageUpdateDto
    ) -> Message:
        # get existing message, will throw 404 if there is not message with given id
        message = self.get_by_id(db, _id)

        # validate new message content length (not empty, not > 160 chars)
        validate_message_content_length(message_update_dto.content)

        # update existing message fields, reset views count
        message_update_obj = jsonable_encoder(message_update_dto)
        message.content = message_update_obj["content"]
        message.views_count = 0

        # save object to db, commit session and refresh object with updated content
        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def delete_by_id(self, db: Session, _id: int) -> Message:
        # get existing message, will throw 404 if there is not message with given id
        message = self.get_by_id(db, _id)

        # delete object from db, commit session
        db.delete(message)
        db.commit()

        return message

    def increase_view_count_by_id(self, db: Session, _id: int) -> Message:
        # get existing message, will throw 404 if there is not message with given id
        message = self.get_by_id(db, _id)

        # increment views count
        message.views_count += 1

        # save object to db, commit session and refresh object with updated content
        db.add(message)
        db.commit()
        db.refresh(message)

        return message


messages = MessageService()
