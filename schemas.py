from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    is_active: bool
    role: str

    class Config:
        orm_mode = True
