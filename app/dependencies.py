from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
from sqlmodel import Session, SQLModel, create_engine, select
from app.config import Settings
from app.models.user import UserPublic, User
from app.schemas.auth import TokenData

@lru_cache
def get_settings():
    return Settings()

# Database configuration
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False} # Use same DB in different threads
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

fake_users_db = {
    "johndoe@example.com": {
        "id": 1,
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "active": True,
    },
    "alice@example.com": {
        "id": 2,
        "email": "alice@example.com",
        "full_name": "Alice",
        "hashed_password": "$2b$12$LT6ZXRITqrh/oYk9r.LqXOgJvmp42AfRtYTr28EvoO71f5LN2Bijq",
        "active": False,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep, settings: Annotated[Settings, Depends(get_settings)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        if email is None: raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.InvalidTokenError: raise credentials_exception
    user = session.exec(select(User).where(User.email == token_data.email)).first()
    if user is None: raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    if (not current_user.active):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
