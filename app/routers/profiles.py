from typing import Annotated
from fastapi import Depends, HTTPException, Query, status
from fastapi.routing import APIRouter
import sqlalchemy
from sqlmodel import select
from app.dependencies import SessionDep, get_current_active_user
from app.models.user import (
    ProfilePublic,
    ProfileCreate,
    Profile,
    ProfileUpdate,
    UserPublic,
)


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=ProfilePublic)
async def create_profile(
    profile: ProfileCreate,
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    try:
        profile_with_user = Profile(**profile.model_dump(), user_id=user.id)
        db_profile = Profile.model_validate(profile_with_user)
        session.add(db_profile)
        session.commit()
        session.refresh(db_profile)
        return db_profile
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists"
        )


@router.get("/", response_model=list[ProfilePublic])
async def read_profiles(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    return session.exec(select(Profile).offset(offset).limit(limit)).all()


@router.get("/me")
async def read_profile_me(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    return session.get(Profile, current_user.id)


@router.get(
    "/{user_id}",
    response_model=ProfilePublic,
)
async def read_profile(user_id: int, session: SessionDep):
    profile = session.get(Profile, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile


@router.patch(
    "/{user_id}",
    response_model=ProfilePublic,
)
async def update_profile(user_id: int, profile: ProfileUpdate, session: SessionDep):
    profile_db = session.get(Profile, user_id)
    if not profile_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    profile_data = profile.model_dump(exclude_unset=True)
    profile_db.sqlmodel_update(profile_data)
    session.add(profile_db)
    session.commit()
    session.refresh(profile_db)
    return profile_db


@router.delete("/{user_id}")
async def delete_profile(user_id: int, session: SessionDep):
    profile = session.get(Profile, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    session.delete(profile)
    session.commit()
    return {"ok": True}
