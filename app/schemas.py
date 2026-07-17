from pydantic import BaseModel, EmailStr 
from typing import Optional
import datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
  

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    

class PostResponse(Post):
    id: int
    # title: str
    # content: str
    # published: bool
    time_created: datetime.datetime

    # class Config:
    #     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    time_created: datetime.datetime

class loginResponse(BaseModel):
    email: EmailStr
    password: str