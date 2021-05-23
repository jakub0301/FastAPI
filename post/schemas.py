from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    body: str

class CreatedPost(Post):
    id: int
    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    password: str

class ShowUser(BaseModel):
    username: str
    class Config():
        orm_mode = True
    
class TokenData(BaseModel):
    username: Optional[str] = None
