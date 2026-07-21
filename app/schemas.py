from pydantic import BaseModel, EmailStr, conint, Field
from typing import Optional
import datetime
from sqlalchemy.orm import relationship

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
  

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    time_created: datetime.datetime
    

class PostResponse(Post):
    id: int
    # title: str
    # content: str
    # published: bool
    time_created: datetime.datetime
    user_id: int
    owner: UserResponse
    


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    



class loginResponse(BaseModel):
    email: EmailStr
    password: str
    

class tokendata(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # ge=0 và le=1 để đảm bảo chỉ nhận giá trị 0 hoặc 1 (Upvote / Downvote)

class PostOut(BaseModel):
    Post: PostResponse
    votes: int