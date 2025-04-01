from pydantic import BaseModel, ConfigDict, EmailStr
from sqlmodel import Field, SQLModel
from typing import Optional


class UserBase(SQLModel):
    email: str = Field(index=True)
    first_name: str
    last_name: str
    job_title: str
    avatar: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    job_title: str
    avatar: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(SQLModel):
    data: User


class UserDelete(SQLModel):
    id: int = Field(default=None, primary_key=True)
