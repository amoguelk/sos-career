from sqlmodel import Field, SQLModel

"""
Database models for users
"""


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    full_name: str | None = Field(default=None, index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    active: bool = Field(default=True)


class UserPublic(UserBase):
    id: int
    active: bool


class UserCreate(UserBase):
    plain_password: str


class UserUpdate(SQLModel):
    email: str | None = None
    full_name: str | None = None
    active: bool | None = None


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
    goals: str | None
