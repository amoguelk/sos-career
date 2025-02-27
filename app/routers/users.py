from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, timezone, datetime
import jwt
from passlib.context import CryptContext
from typing_extensions import Annotated
from app.dependencies import get_current_active_user, get_user
from app.models import User, Token

# ! HIDE IN PROD
SECRET_KEY = "740cf38d7db3ccd56bb12547460bb0ced2d79e4f03805461eeac4e5db4f09577"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MIN = 30

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe@example.com": {
        "id": 1,
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "active": True,
    },
    "alice@example.com": {
        "id": 2,
        "email": "alice@example.com",
        "hashed_password": "$2b$12$LT6ZXRITqrh/oYk9r.LqXOgJvmp42AfRtYTr28EvoO71f5LN2Bijq",
        "active": False,
    },
}

def get_password_hash(pwd):
    return pwd_context.hash(pwd)

def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user: return False
    if not pwd_context.verify(password, user.hashed_password): return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/auth")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(TOKEN_EXPIRE_MIN))
    return Token(access_token=access_token, token_type="bearer")

# @router.get("/")
# async def read_users():
#     return fake_users

@router.get("/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# @router.get("/{user_id}")
# async def read_user(user_id: int):
#     return [user for user in fake_users if user.id == user_id][0]
