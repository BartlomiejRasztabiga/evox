import random
import string
from typing import Dict

from app.core.config import settings


def random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def get_authentication_header() -> Dict[str, str]:
    return {"Authorization": settings.API_KEY}
