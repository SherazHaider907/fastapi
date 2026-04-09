from fastapi import APIRouter

router = APIRouter()


@router.get("/auth/")
async def auth():
    return {"user": "Authenticated User"}


