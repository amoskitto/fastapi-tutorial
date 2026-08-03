from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic import conint


#schema is used to ensure consistent info or validating the information provided by the user 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
        
                
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
#schema for the token
class Token(BaseModel):
    access_token: str
    token_type: str
    
#shcema for the token data
class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]