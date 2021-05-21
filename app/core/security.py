from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="Authorization")


def verify_api_key(api_key: str = Depends(API_KEY_HEADER)) -> bool:
    if api_key == settings.API_KEY:
        return True
    # else raise 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )
