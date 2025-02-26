from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/users", tags=["users"])

class User(BaseModel):
    id: int
    username: str

fake_usernames = ["aLesPI", "wasp", "mikeW"]
fake_users = [User(id=(i+1),username=username) for i, username in enumerate(fake_usernames)]

@router.get("/")
async def read_users():
    return fake_users

@router.get("/me")
async def read_user_me():
    return fake_users[1]

@router.get("/{user_id}")
async def read_user(user_id: int):
    return [user for user in fake_users if user.id == user_id][0]
