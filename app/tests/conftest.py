from typing import Generator, Dict

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.tests.utils import get_authentication_header


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def authentication_headers() -> Dict[str, str]:
    return get_authentication_header()
