from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from app.core.security import verify_api_key

router = APIRouter()


@router.get("/test")
async def test(api_key: APIKey = Depends(verify_api_key)) -> str:
    return "test"
