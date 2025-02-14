from pydantic import BaseModel,EmailStr,conint
from pydantic.types import conint
from typing import Optional,Annotated
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    owner_id: Optional[int] 
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post:Post
    votes:int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]
