from datetime import datetime
from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    login: str
    password: str
    created_at: datetime

class UserCreate(BaseModel):
    login: str
    password: str

class UserCredentials(BaseModel):
    login: str
    password: str
