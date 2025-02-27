from pydantic import BaseModel

'''
Users and auth
'''
class User(BaseModel):
    id: int
    email: str
    active: bool = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
