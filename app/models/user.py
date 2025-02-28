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
