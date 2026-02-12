from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str