from fastapi.routing import APIRouter


router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/")
async def read_messages():
    return []
