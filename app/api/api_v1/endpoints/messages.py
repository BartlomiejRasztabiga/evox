from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, services
from app.api import deps
from app.core.security import verify_api_key
from app.models import Message

router = APIRouter()


@router.get("/{id}", response_model=schemas.Message)
async def get_message(id: int, db: Session = Depends(deps.get_db)) -> Message:
    """
    Retrieves message by ID. Increments message's views count.
    """

    # increment view count
    services.messages.increment_view_count_by_id(db=db, _id=id)

    return services.messages.get_by_id(db=db, _id=id)


@router.post("/", response_model=schemas.Message)
async def create_message(
    *,
    db: Session = Depends(deps.get_db),
    message_create_dto: schemas.MessageCreateDto,
    _: bool = Depends(verify_api_key)
) -> Message:
    """
    Creates new message.
    """
    return services.messages.create(db=db, message_create_dto=message_create_dto)


@router.put("/{id}", response_model=schemas.Message)
async def update_message(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    message_update_dto: schemas.MessageUpdateDto,
    _: bool = Depends(verify_api_key)
) -> Message:
    """
    Updates existing message with given ID.
    """
    return services.messages.update_by_id(
        db=db, _id=id, message_update_dto=message_update_dto
    )


@router.delete("/{id}", response_model=schemas.Message)
async def delete_message(
    *, db: Session = Depends(deps.get_db), id: int, _: bool = Depends(verify_api_key)
) -> Message:
    """
    Deletes existing message with given ID.
    """
    return services.messages.delete_by_id(db=db, _id=id)
