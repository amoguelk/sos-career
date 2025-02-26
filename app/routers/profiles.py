from fastapi.routing import APIRouter


router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/")
async def read_profiles():
    return []
