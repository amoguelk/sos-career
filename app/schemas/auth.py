from pydantic import BaseModel

'''
Pydantic schemas for users and auth
'''

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
