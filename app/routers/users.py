from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, timezone, datetime
import jwt
from passlib.context import CryptContext
from sqlmodel import select
from typing_extensions import Annotated
from app.config import Settings
from app.dependencies import SessionDep, get_current_active_user, get_settings
from app.models.user import User, UserCreate, UserPublic, UserUpdate
from app.schemas.auth import Token

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(pwd):
    return pwd_context.hash(pwd)


def authenticate_user(email: str, password: str, session: SessionDep):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, secret_key: str, algorithm: str, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


@router.post("/auth")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    settings: Annotated[Settings, Depends(get_settings)],
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(settings.token_expire_min),
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/new", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep):
    hashed_user = User(
        **user.model_dump(),
        hashed_password=get_password_hash(user.plain_password),
    )
    db_user = User.model_validate(hashed_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserPublic)
async def read_user_me(
    current_user: Annotated[UserPublic, Depends(get_current_active_user)]
):
    return current_user


@router.get(
    "/",
    response_model=list[UserPublic],
    dependencies=[Depends(get_current_active_user)],
)
async def read_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    return session.exec(select(User).offset(offset).limit(limit)).all()


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
async def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_user)],
)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_user)])
async def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return {"ok": True}
