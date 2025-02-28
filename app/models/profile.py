from sqlmodel import Field, SQLModel

"""
Database models for profiles
"""


class ProfileBase(SQLModel):
    interests: str | None = Field(default=None)
    skills: str | None = Field(default=None)
    education_level: str | None = Field(default=None)
    goals: str | None = Field(default=None)


class Profile(ProfileBase, table=True):
    user_id: int = Field(foreign_key="user.id", unique=True, primary_key=True)


class ProfilePublic(ProfileBase):
    user_id: int


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(SQLModel):
    interests: str | None = None
    skills: str | None = None
    education_level: str | None = None
    goals: str | None = None