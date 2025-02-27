from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
from app.models import TokenData, User, UserInDB

# ! HIDE IN PROD
SECRET_KEY = "740cf38d7db3ccd56bb12547460bb0ced2d79e4f03805461eeac4e5db4f09577"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MIN = 30

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")

def get_user(db, email: str | None):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None: raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.InvalidTokenError: raise credentials_exception
    user = get_user(fake_users_db, email=token_data.email)
    if user is None: raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if (not current_user.active):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
