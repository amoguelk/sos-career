from typing import Annotated
from fastapi import Body, Depends, Query
from fastapi.routing import APIRouter
from sqlmodel import select
from app.dependencies import SessionDep, get_current_active_user
from app.models.message import Message, MessageCreate, MessagePublic
from app.models.user import UserPublic


router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(get_current_active_user)],
)

async def save_message(message: MessageCreate, session: SessionDep):
    db_message = Message.model_validate(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

@router.post("/career-paths", response_model=MessagePublic)
async def create_career_path(
    prompt: Annotated[str, Body(embed=True)],
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    message = MessageCreate(msg_type="career-path", response="Learn to code", user_id=user.id)
    return await save_message(message, session)

@router.post("/job-insights", response_model=MessagePublic)
async def create_job_insights(
    prompt: Annotated[str, Body(embed=True)],
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    message = MessageCreate(msg_type="job-insight", response="Learn to code", user_id=user.id)
    return await save_message(message, session)

@router.post("/roadmaps", response_model=MessagePublic)
async def create_roadmap(
    prompt: Annotated[str, Body(embed=True)],
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    message = MessageCreate(msg_type="roadmap", response="Learn to code", user_id=user.id)
    return await save_message(message, session)

@router.get("/", response_model=list[MessagePublic])
async def read_messages(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    return session.exec(select(Message).offset(offset).limit(limit)).all()

@router.get("/me", response_model=list[MessagePublic])
async def read_profile_me(
    session: SessionDep,
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    return session.exec(select(Message).where(Message.user_id == current_user.id)).all()