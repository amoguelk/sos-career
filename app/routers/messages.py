from fastapi import Depends
from fastapi.routing import APIRouter
from app.dependencies import get_current_active_user


router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/")
async def read_messages():
    return []
