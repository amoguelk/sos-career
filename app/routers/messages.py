from typing import Annotated
from fastapi import Body, Depends, Query, HTTPException, status
from fastapi.routing import APIRouter
from sqlmodel import select
from app.dependencies import SessionDep, get_current_active_user, get_settings
from app.models.message import Message, MessageCreate, MessagePublic
from app.models.user import UserPublic
from app.models.profile import Profile
from openai import OpenAI
from app.config import Settings

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(get_current_active_user)],
)

client = OpenAI(api_key=get_settings().openai_api_key)


def get_profile(user_id, session: SessionDep):
    profile = session.get(Profile, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not created"
        )
    return profile


async def generate_message(
    prompt: str,
):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            n=1,
            stop=None,
        )

        [message] = map(lambda choice: choice.message.content, response.choices)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )

    if not message or not response.usage:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No message generated",
        )

    return message, response.usage.total_tokens


async def save_message(message: MessageCreate, session: SessionDep):
    db_message = Message.model_validate(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


@router.post("/career-paths", response_model=MessagePublic)
async def create_career_path(
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
    user_prompt: Annotated[str | None, Body(embed=True)] = None,
):
    profile = get_profile(user.id, session)
    prompt = f"""
        Based on the following information about a student, suggest potential career paths that align with their interests, skills, and goals. Provide a brief description of each recommended career path, including the types of tasks involved, necessary skills, and how it aligns with the student’s goals. Make sure to focus more on education opportunities rather than jobs. Here is the student's information:

            {f"""Interests: "{profile.interests}" """ if profile.interests else ""}
            {f"""Skills: "{profile.skills}" """ if profile.skills else ""}
            {f"""Career goals: "{profile.goals}" """ if profile.goals else ""}

        Please ensure the career paths are realistic based on the student's profile and provide explanations for each recommendation.
        {f"""Here's some further guidance provided by the student: "{user_prompt}" """ if user_prompt else ""}
        """
    response, tokens = await generate_message(prompt)
    message = MessageCreate(
        msg_type="career-path",
        response=response,
        tokens=tokens,
        user_id=user.id,
        prompt=user_prompt,
    )
    return await save_message(message, session)


@router.post("/job-insights", response_model=MessagePublic)
async def create_job_insights(
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
    user_prompt: Annotated[str | None, Body(embed=True)] = None,
):
    profile = get_profile(user.id, session)
    prompt = f"""
        Based on the following student profile, provide a list of job insights for careers that align with their interests, skills, and goals. For each job, include the following insights:

            1. A brief description of the job.
            2. Key skills and qualifications required.
            3. Typical tasks and responsibilities.
            4. The average salary or compensation range.
            5. Job outlook (growth potential, demand, or future trends).
            6. Any recommended steps or additional education required to enter the field.

        Here is the student profile:

            {f"""Interests: "{profile.interests}" """ if profile.interests else ""}
            {f"""Skills: "{profile.skills}" """ if profile.skills else ""}
            {f"""Career goals: "{profile.goals}" """ if profile.goals else ""}

        Please ensure the job insights are tailored to the student's profile and provide clear, actionable recommendations.
        {f"""Here's some further guidance provided by the student: "{user_prompt}" """ if user_prompt else ""}
        """
    response, tokens = await generate_message(prompt)
    message = MessageCreate(
        msg_type="job-insight",
        response=response,
        tokens=tokens,
        user_id=user.id,
        prompt=user_prompt,
    )
    return await save_message(message, session)


@router.post("/roadmaps", response_model=MessagePublic)
async def create_roadmap(
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_active_user)],
    user_prompt: Annotated[str | None, Body(embed=True)] = None,
):
    profile = get_profile(user.id, session)
    prompt = f"""
        Based on the following student profile, create a detailed career roadmap that outlines the steps needed to achieve their career goals. The roadmap should include milestones, key skills to develop, potential education or certifications, and specific actions the student should take to move towards their desired career. Be sure to consider the student's interests, skills, and career goals when crafting the roadmap.

        Here is the student's profile:

            {f"""Interests: "{profile.interests}" """ if profile.interests else ""}
            {f"""Skills: "{profile.skills}" """ if profile.skills else ""}
            {f"""Career goals: "{profile.goals}" """ if profile.goals else ""}

        Please create a structured, realistic plan that takes the student from their current position to their goal, with actionable steps and recommendations.
        {f"""Here's some further guidance provided by the student: "{user_prompt}" """ if user_prompt else ""}
        """
    response, tokens = await generate_message(prompt)
    message = MessageCreate(
        msg_type="roadmap",
        response=response,
        tokens=tokens,
        user_id=user.id,
        prompt=user_prompt,
    )
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


@router.get(
    "/{message_id}",
    response_model=MessagePublic,
)
async def read_message(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    return message


@router.delete(
    "/{message_id}",
    response_model=MessagePublic,
)
async def delete_message(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    session.delete(message)
    session.commit()
    return message
