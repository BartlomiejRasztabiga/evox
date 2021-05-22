import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import services
from app.core.config import settings
from app.exceptions.message import MessageNotFoundException
from app.tests.utils.message import create_test_message


def test_create_message(
        client: TestClient, authentication_headers, db: Session
) -> None:
    data = {
        "content": "New message"
    }

    response = client.post(
        f"{settings.API_V1_STR}/messages/", headers=authentication_headers, json=data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["content"] == data["content"]
    assert content["views_count"] == 0
    assert "id" in content

    db.commit()

    created_message = services.messages.get_by_id(db=db, _id=content["id"])
    assert created_message is not None
    assert created_message.id == content["id"]
    assert created_message.views_count == 0
    assert created_message.content == content["content"]


def test_get_message(
        client: TestClient, authentication_headers: dict, db: Session
) -> None:
    message = create_test_message(db)

    response = client.get(
        f"{settings.API_V1_STR}/messages/{message.id}", headers=authentication_headers
    )

    assert response.status_code == 200

    content = response.json()
    assert content["content"] == message.content
    assert content["views_count"] == 1
    assert content["id"] == message.id


def test_update_message(
        client: TestClient, authentication_headers: dict, db: Session
) -> None:
    message = create_test_message(db)

    data = {
        "content": "New content",
    }

    response = client.put(
        f"{settings.API_V1_STR}/messages/{message.id}", headers=authentication_headers, json=data
    )

    assert response.status_code == 200

    content = response.json()
    assert content["content"] == data["content"]
    assert content["views_count"] == 0
    assert content["id"] == message.id

    db.commit()

    updated_message = services.messages.get_by_id(db=db, _id=content["id"])
    assert updated_message is not None
    assert updated_message.id == content["id"]
    assert updated_message.views_count == 0
    assert updated_message.content == content["content"]


def test_delete_message(
        client: TestClient, authentication_headers: dict, db: Session
) -> None:
    message = create_test_message(db)
    _id = message.id

    response = client.delete(
        f"{settings.API_V1_STR}/messages/{_id}", headers=authentication_headers
    )

    assert response.status_code == 200

    db.commit()

    with pytest.raises(MessageNotFoundException):
        services.messages.get_by_id(db=db, _id=_id)
