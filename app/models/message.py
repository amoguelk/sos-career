from sqlmodel import Field, SQLModel


"""
Database message models
"""


class MessageBase(SQLModel):
    msg_type: str
    response: str
    tokens: int
    prompt: str | None = None


class Message(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")


class MessageCreate(MessageBase):
    user_id: int


class MessagePublic(MessageBase):
    id: int
    user_id: int
